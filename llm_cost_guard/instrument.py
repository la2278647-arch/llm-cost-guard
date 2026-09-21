"""Optional SDK wrappers: auto-log OpenAI-compatible chat completions.

Usage:
    from llm_cost_guard.instrument import wrap_openai
    client = wrap_openai(OpenAI())          # openai>=1.0 style client
    client.chat.completions.create(...)     # usage is logged automatically

Only activates if the provider SDK is installed; core stays stdlib-only.
"""

from __future__ import annotations

from .tracker import Tracker


def wrap_openai(client, tracker: Tracker | None = None, tag: str = "openai"):
    """Wrap an OpenAI-compatible client so each chat completion is logged."""
    t = tracker or Tracker()
    original = client.chat.completions.create

    def logged_create(*args, **kwargs):
        resp = original(*args, **kwargs)
        usage = getattr(resp, "usage", None)
        if usage is not None:
            t.log(
                model=getattr(resp, "model", kwargs.get("model", "unknown")),
                input_tokens=getattr(usage, "prompt_tokens", 0) or 0,
                output_tokens=getattr(usage, "completion_tokens", 0) or 0,
                tag=tag,
            )
        return resp

    client.chat.completions.create = logged_create
    return client
