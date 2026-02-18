from pathlib import Path

from src.counter_store import CounterStore


def test_increment_for_new_user(tmp_path: Path) -> None:
    store = CounterStore(tmp_path / "counts.json")
    assert store.increment(1, 10) == 1


def test_increment_accumulates_for_same_user(tmp_path: Path) -> None:
    store = CounterStore(tmp_path / "counts.json")
    assert store.increment(1, 10) == 1
    assert store.increment(1, 10) == 2
    assert store.get(1, 10) == 2


def test_counts_are_isolated_by_guild_and_user(tmp_path: Path) -> None:
    store = CounterStore(tmp_path / "counts.json")

    assert store.increment(1, 10) == 1
    assert store.increment(1, 11) == 1
    assert store.increment(2, 10) == 1
    assert store.get(1, 10) == 1
    assert store.get(1, 11) == 1
    assert store.get(2, 10) == 1


def test_counts_persist_after_reload(tmp_path: Path) -> None:
    path = tmp_path / "counts.json"
    store = CounterStore(path)
    store.increment(1, 10)
    store.increment(1, 10)

    reloaded = CounterStore(path)
    assert reloaded.get(1, 10) == 2
