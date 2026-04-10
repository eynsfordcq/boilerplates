import asyncio
import logging
from datetime import datetime, timedelta, timezone
from typing import Callable, Optional

import aiohttp
from fastapi import Request
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class Filter:
    class Valves(BaseModel):
        max_retries: int = Field(
            default=10,
            description="Maximum number of polling attempts to retrieve LiteLLM cost data.",
        )
        retry_interval: int = Field(
            default=2,
            description="Number of seconds to wait between polling attempts.",
        )
        initial_delay: int = Field(
            default=5,
            description="Number of seconds to wait before polling attempts.",
        )

    def __init__(self):
        self.valves = self.Valves()
        self._url: Optional[str] = None
        self._key: Optional[str] = None
        self._request_ids: set[str] = set()

    def inlet(
        self,
        body: dict,
        __request__: Request = None,
        __model__: dict = None,
    ) -> dict:
        try:
            idx = (__model__ or {}).get("urlIdx", 0)
            config = __request__.app.state.config
            self._url = config.OPENAI_API_BASE_URLS[idx].rstrip("/")
            self._key = config.OPENAI_API_KEYS[idx]
            self._request_ids = set()
        except Exception as e:
            logger.error(f"Inlet setup error: {e}")
        return body

    async def stream(self, event: dict, __event_emitter__: Callable = None) -> dict:
        rid = event.get("id")
        if rid and rid not in self._request_ids:
            self._request_ids.add(rid)
            await self._emit_status(
                __event_emitter__,
                f"Captured request ID: {rid} (total: {len(self._request_ids)})",
                done=False,
            )
        return event

    async def outlet(
        self,
        body: dict,
        __request__: Request = None,
        __event_emitter__: Callable = None,
    ) -> dict:
        if not self._request_ids or not self._url:
            await self._emit_status(
                __event_emitter__,
                "Usage data unavailable (missing URL or request IDs).",
                done=True,
            )
            return body

        asyncio.create_task(
            self._background_usage_task(
                set(
                    self._request_ids
                ),  # snapshot — avoid mutation after outlet returns
                self._url,
                self._key,
                __event_emitter__,
            )
        )
        return body

    async def _background_usage_task(
        self,
        request_ids: set[str],
        url: str,
        key: str,
        emitter: Optional[Callable],
    ):
        try:
            await self._emit_status(
                emitter,
                f"Waiting {self.valves.initial_delay}s before polling "
                f"{len(request_ids)} request(s)...",
                done=False,
            )
            await asyncio.sleep(self.valves.initial_delay)

            # Share one session across all concurrent polls.
            async with aiohttp.ClientSession() as session:
                results = await asyncio.gather(
                    *(
                        self._poll_single_request(
                            rid, url, key, session, emitter, idx, len(request_ids)
                        )
                        for idx, rid in enumerate(request_ids, 1)
                    ),
                    return_exceptions=True,
                )

            records = [r for r in results if isinstance(r, dict)]

            if records:
                aggregated = self._aggregate_records(records)
                await self._emit_status(
                    emitter,
                    self._format_usage_message(
                        aggregated, len(records), len(request_ids)
                    ),
                    done=True,
                )
            else:
                await self._emit_status(
                    emitter,
                    "Failed to retrieve usage data after retries.",
                    done=True,
                )
        except Exception as e:
            logger.error(f"Error in background usage task: {e}")

    async def _poll_single_request(
        self,
        request_id: str,
        url: str,
        key: str,
        session: aiohttp.ClientSession,
        emitter: Optional[Callable],
        index: int,
        total: int,
    ) -> Optional[dict]:
        """Poll LiteLLM for a single request ID with retries."""
        now = datetime.now(timezone.utc)
        start_date = (now - timedelta(days=1)).strftime("%Y-%m-%d")
        end_date = (now + timedelta(days=1)).strftime("%Y-%m-%d")
        endpoint = (
            f"{url}/spend/logs/v2"
            f"?request_id={request_id}"
            f"&start_date={start_date}"
            f"&end_date={end_date}"
            f"&page=1&page_size=1"
        )
        headers = {
            "accept": "application/json",
            "x-litellm-api-key": key,
        }
        label = f"[{index}/{total}] {request_id[:8]}…"

        for attempt in range(self.valves.max_retries):
            await self._emit_status(
                emitter,
                f"Polling {label} (attempt {attempt + 1}/{self.valves.max_retries})",
                done=False,
            )
            try:
                async with session.get(endpoint, headers=headers) as r:
                    if r.status == 200:
                        data = await r.json()
                        records = data.get("data", [])
                        if records:
                            return records[0]
            except Exception as e:
                logger.debug(f"Polling exception for {request_id}: {e}")

            if attempt < self.valves.max_retries - 1:
                await asyncio.sleep(self.valves.retry_interval)

        return None

    def _aggregate_records(self, records: list[dict]) -> dict:
        return {
            "prompt_tokens": sum(r.get("prompt_tokens", 0) for r in records),
            "completion_tokens": sum(r.get("completion_tokens", 0) for r in records),
            "total_tokens": sum(r.get("total_tokens", 0) for r in records),
            "spend": sum(r.get("spend") or 0.0 for r in records),
        }

    async def _emit_status(
        self,
        emitter: Optional[Callable],
        description: str,
        done: bool = False,
    ):
        if not emitter:
            return
        await emitter(
            {
                "type": "status",
                "data": {
                    "description": description,
                    "done": done,
                    "hidden": False,
                },
            }
        )

    def _format_usage_message(self, log: dict, retrieved: int, total: int) -> str:
        prompt_tokens = log.get("prompt_tokens", 0)
        completion_tokens = log.get("completion_tokens", 0)
        total_tokens = log.get("total_tokens", 0)
        total_cost = log.get("spend") or 0.0

        msg = (
            f"💸 Cost: ${total_cost:.5f} | "
            f"🎰 Tokens: ⬆️ {prompt_tokens:,} · ⬇️ {completion_tokens:,} · 🙈 {total_tokens:,}"
        )
        if total > 1:
            missing = total - retrieved
            note = f"{retrieved}/{total} requests"
            if missing:
                note += f", {missing} failed"
            msg += f" ({note})"

        return msg
