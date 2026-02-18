from src.message_handler import build_count_report, is_uo_message, should_count_message


def test_is_uo_message_exact_match() -> None:
    assert is_uo_message("うお") is True
    assert is_uo_message(" うお ") is True
    assert is_uo_message("ウオ") is True
    assert is_uo_message("ぅぉ") is True
    assert is_uo_message("ｳｫ") is True


def test_is_uo_message_non_match() -> None:
    assert is_uo_message("うお!") is False
    assert is_uo_message("うおう") is False
    assert is_uo_message("") is False


def test_should_count_message() -> None:
    assert should_count_message(is_bot=False, guild_id=123, content="うお") is True
    assert should_count_message(is_bot=True, guild_id=123, content="うお") is False
    assert should_count_message(is_bot=False, guild_id=None, content="うお") is False
    assert should_count_message(is_bot=False, guild_id=123, content="hello") is False


def test_build_count_report() -> None:
    assert build_count_report("@alice", 3) == "@alice うお回数: 3回"
