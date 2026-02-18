from __future__ import annotations


def is_uo_message(content: str) -> bool:
    return content.strip() == "うお"


def should_count_message(*, is_bot: bool, guild_id: int | None, content: str) -> bool:
    if is_bot:
        return False
    if guild_id is None:
        return False
    return is_uo_message(content)


def build_count_report(user_mention: str, count: int) -> str:
    return f"{user_mention} うお回数: {count}回"
