import base64
import os

import requests as _requests

_PROMPT = (
    "Look at this Pokémon trading card image. "
    "Is the card text printed in English? "
    "Reply with exactly one word: YES or NO."
)

_MODEL = "claude-haiku-4-5"


def check_card_is_english(image_url: str, session: _requests.Session | None = None) -> bool:
    """Download image_url and ask Claude Haiku whether the card is in English.

    Returns True when the card appears to be English, or when the check
    cannot be completed (fail-open so valid listings are never silently dropped).
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return True

    try:
        import anthropic
    except ImportError:
        return True

    try:
        getter = session if session is not None else _requests.Session()
        resp = getter.get(image_url, timeout=10)
        resp.raise_for_status()
        image_b64 = base64.standard_b64encode(resp.content).decode()
        media_type = resp.headers.get("Content-Type", "image/jpeg").split(";")[0].strip()
    except Exception:
        return True

    try:
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model=_MODEL,
            max_tokens=8,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_b64,
                            },
                        },
                        {"type": "text", "text": _PROMPT},
                    ],
                }
            ],
        )
        answer = message.content[0].text.strip().upper()
        return answer.startswith("YES")
    except Exception:
        return True
