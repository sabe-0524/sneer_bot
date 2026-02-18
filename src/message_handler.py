from __future__ import annotations

import re
import unicodedata


_SMALL_TO_REGULAR = str.maketrans(
    {
        "ぁ": "あ",
        "ぃ": "い",
        "ぅ": "う",
        "ぇ": "え",
        "ぉ": "お",
        "ゃ": "や",
        "ゅ": "ゆ",
        "ょ": "よ",
        "ゎ": "わ",
        "ゕ": "か",
        "ゖ": "け",
        "っ": "つ",
        "を": "お",
    }
)

_WO_PATTERN = re.compile(r"wo", re.IGNORECASE)

_LATIN_TO_HIRAGANA = str.maketrans(
    {
        "u": "う",
        "U": "う",
        "o": "お",
        "O": "お",
    }
)


def _to_hiragana(text: str) -> str:
    chars: list[str] = []
    for char in text:
        code_point = ord(char)
        if 0x30A1 <= code_point <= 0x30F6:
            chars.append(chr(code_point - 0x60))
            continue
        chars.append(char)
    return "".join(chars)


def normalize_uo_text(content: str) -> str:
    normalized = unicodedata.normalize("NFKC", content).strip()
    normalized = re.sub(r"\s+", "", normalized)
    normalized = _to_hiragana(normalized)
    normalized = normalized.translate(_SMALL_TO_REGULAR)
    normalized = _WO_PATTERN.sub("お", normalized)
    return normalized.translate(_LATIN_TO_HIRAGANA)


def is_uo_message(content: str) -> bool:
    return "うお" in normalize_uo_text(content)


def should_count_message(*, is_bot: bool, guild_id: int | None, content: str) -> bool:
    if is_bot:
        return False
    if guild_id is None:
        return False
    return is_uo_message(content)


def build_count_report(user_mention: str, count: int) -> str:
    return f"{user_mention} うお回数: {count}回"
