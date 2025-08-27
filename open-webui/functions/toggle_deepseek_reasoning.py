"""
https://github.com/open-webui/open-webui/issues/13314#issuecomment-2887581867
https://openrouter.ai/docs/use-cases/reasoning-tokens#controlling-reasoning-tokens
"""

from collections.abc import Awaitable, Callable

from pydantic import BaseModel


class Filter:
    class Valves(BaseModel):
        pass

    def __init__(self) -> None:
        self.valves = self.Valves()
        self.toggle = True
        self.icon = """data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMjgiIGhlaWdodD0iMTI4IiB4bWw6c3BhY2U9InByZXNlcnZlIj48cGF0aCBmaWxsPSIjMjgyRDMzIiBkPSJNMTA4Ljk0OCAxMjhoLTRWODIuOTUzbC41OTQtLjU4N2M4Ljc2Ny04LjY2OSAxMy41OTUtMjAuMTg4IDEzLjU5NS0zMi40MzNDMTE5LjEzNyAyNC42MDUgOTguMjQ3IDQgNzIuNTcgNCA0Ni44ODkgNCAyNS45OTUgMjQuNjA1IDI1Ljk5NSA0OS45MzNjMCAuNjk4LjAyNiAxLjM4OC4wNTYgMi4wODJsLjAyNS41ODgtMTQuMjM3IDI0LjMzNmg5Ljc5N3YyMC45MjZjMCA2LjAyNCA0Ljk3NyAxMC45MjYgMTEuMDk1IDEwLjkyNmgyMi43NDFWMTI4aC00di0xNS4yMDlIMzIuNzMxYy04LjMyMyAwLTE1LjA5NS02LjY5NS0xNS4wOTUtMTQuOTI2VjgwLjkzOUg0Ljg2M0wyMi4wMyA1MS41OTdhNDMuNzYgNDMuNzYgMCAwIDEtLjAzNi0xLjY2NEMyMS45OTUgMjIuNCA0NC42ODMgMCA3Mi41NyAwYzI3Ljg4MyAwIDUwLjU2NiAyMi40IDUwLjU2NiA0OS45MzMgMCAxMy4wNDMtNS4wMzEgMjUuMzI1LTE0LjE4OCAzNC42OFYxMjh6Ii8+PHBhdGggZmlsbD0iIzI4MkQzMyIgZD0iTTEwMS44NTcgNTUuMDE4Yy0xLjE3OCA1LjgxNC00LjA3OSAxMS4xOTMtOC4zOTYgMTUuNDU3LTUuODEyIDUuNzMyLTEzLjU0MyA4Ljg5MS0yMS43NjkgOC44OTEtNi4wNCAwLTExLjg5Ni0xLjc0LTE2Ljg3Mi00Ljk2MWwxOS42NDItMTkuMzg2aDI3LjM5NW00LjQ3MS0zLjkzOWgtMzMuNDhMNDguODE0IDc0LjgwMmM2LjMzMSA1LjQ5NiAxNC4zNzQgOC41IDIyLjg4IDguNSA5LjI2OCAwIDE3Ljk4MS0zLjU2MiAyNC41MzItMTAuMDI0IDYuMDc1LTUuOTk5IDkuNjE0LTEzLjgwNyAxMC4xMDItMjIuMTk4ek03Ny44OTMgMTkuMzY1YzExLjc0NiAyLjMxMyAyMC45NjcgMTEuMDk5IDIzLjcxMSAyMi41NzFINzcuODkzVjE5LjM2NW0tMy45MzgtNC40Njh2MzAuOTc3aDMyLjI3NWMtMS41NDgtMTYuODUtMTUuMTU2LTI5LjkxNC0zMi4yNzUtMzAuOTc3ek02NC42NTEgMTkuMzM4djI2LjgzNUw0NS4zMTMgNjUuMjU0YTMwLjE3NiAzMC4xNzYgMCAwIDEtNC43MjQtMTYuMTljLjAwMi0xNC4yNTkgMTAuMjcyLTI2LjU4MiAyNC4wNjItMjkuNzI2bTMuOTM5LTQuNTg3Yy0xNy44MSAxLjUwNy0zMS45MzYgMTYuNDQ0LTMxLjkzOCAzNC4zMTIgMCA4LjE3OSAyLjg5OCAxNS45NyA4LjIwMiAyMi4xNzZsMjMuNzM2LTIzLjQyVjE0Ljc1MXoiLz48L3N2Zz4="""

    async def inlet(
        self,
        body: dict,
        __event_emitter__: Callable[[dict], Awaitable[None]],
        __user__: dict | None = None,
    ) -> dict:
        body["extra_body"] = {
            "chat_template_kwargs": {
                "thinking": self.toggle,
            },
        }

        await __event_emitter__(
            {
                "type": "status",
                "data": {
                    "description": f"Thinking: {self.toggle}",
                    "done": True,
                    "hidden": False,
                },
            }
        )

        return body
