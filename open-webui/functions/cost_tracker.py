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
            description="Number of seconds to wait before request attempts.",
        )

    def __init__(self):
        self.valves = self.Valves()
        self._url: Optional[str] = None
        self._key: Optional[str] = None
        self._request_id: Optional[str] = None

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
            self._request_id = None
        except Exception as e:
            logger.error(f"Inlet setup error: {e}")

        return body

    async def stream(self, event: dict, __event_emitter__: Callable = None) -> dict:
        if not self._request_id and event.get("id"):
            self._request_id = event["id"]
            await self._emit_status(
                __event_emitter__,
                f"Captured Request ID: {self._request_id}",
                done=False,
            )
        return event

    async def outlet(
        self,
        body: dict,
        __request__: Request = None,
        __event_emitter__: Callable = None,
    ) -> dict:
        if not self._request_id or not self._url:
            await self._emit_status(
                __event_emitter__,
                "Usage data unavailable (Missing URL or Request ID).",
                done=True,
            )
            return body

        await self._emit_status(
            __event_emitter__,
            f"Waiting for {self.valves.initial_delay}s before calling "
            f"LiteLLM usage endpoint with Request ID: {self._request_id}",
            done=False,
        )

        await asyncio.sleep(self.valves.initial_delay)

        log_record = await self._poll_usage_data(
            self._request_id,
            self._url,
            self._key,
            __event_emitter__,
        )

        if log_record:
            cost_message = self._format_usage_message(log_record)
            await self._emit_status(
                __event_emitter__,
                cost_message,
                done=True,
            )
        else:
            await self._emit_status(
                __event_emitter__,
                "Failed to retrieve usage data after retries.",
                done=True,
            )

        return body

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

    async def _poll_usage_data(
        self,
        request_id: str,
        url: str,
        key: str,
        emitter: Optional[Callable],
    ) -> Optional[dict]:
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

        async with aiohttp.ClientSession() as session:
            for attempt in range(self.valves.max_retries):
                await self._emit_status(
                    emitter,
                    f"Polling LiteLLM (Attempt {attempt + 1}/{self.valves.max_retries})...",
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
                    logger.debug(f"Polling Exception: {e}")

                if attempt < self.valves.max_retries - 1:
                    await asyncio.sleep(self.valves.retry_interval)

        return None

    def _format_usage_message(self, log: dict) -> str:
        prompt_tokens = log.get("prompt_tokens", 0)
        completion_tokens = log.get("completion_tokens", 0)
        total_tokens = log.get("total_tokens", 0)
        total_cost = log.get("spend") or 0.0

        return (
            f"💸 Cost: ${total_cost:.5f} | "
            f"🎰 Tokens: ⬆️ {prompt_tokens:,} · ⬇️ {completion_tokens:,} · 🙈 {total_tokens:,} "
        )
