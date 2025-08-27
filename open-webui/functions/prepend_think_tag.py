"""
title: Prepend Think Tag
author: eynsfordcq
github_url: https://github.com/eynsfordcq
version: 1.0.0
"""

from typing import Optional

from pydantic import BaseModel


class Filter:
    class Valves(BaseModel):
        pass

    def __init__(self):
        self.is_first_content_chunk = True
        print("[Prepend Think Tag] Filter initialized.")

    def inlet(self, body: dict, user: Optional[dict] = None) -> dict:
        self.is_first_content_chunk = True
        return body

    def stream(self, event: dict):
        if not self.is_first_content_chunk:
            return event

        try:
            delta = event.get("choices", [{}])[0].get("delta", {})
            content = delta.get("content")
            if content:
                if not content.startswith("<think>"):
                    # Modify the content in-place.
                    delta["content"] = f"<think>{content}"

                # We've now handled the first content chunk.
                # Set the flag to False to ignore subsequent chunks in this stream.
                self.is_first_content_chunk = False
        except (IndexError, KeyError):
            pass

        return event
