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


def test_reset_clears_count(tmp_path: Path) -> None:
    store = CounterStore(tmp_path / "counts.json")
    store.increment(1, 10)
    store.increment(1, 10)
    store.reset(1, 10)
    assert store.get(1, 10) == 0


def test_reset_only_affects_target_user(tmp_path: Path) -> None:
    store = CounterStore(tmp_path / "counts.json")
    store.increment(1, 10)
    store.increment(1, 11)
    store.reset(1, 10)
    assert store.get(1, 10) == 0
    assert store.get(1, 11) == 1


def test_reset_persists_after_reload(tmp_path: Path) -> None:
    path = tmp_path / "counts.json"
    store = CounterStore(path)
    store.increment(1, 10)
    store.reset(1, 10)

    reloaded = CounterStore(path)
    assert reloaded.get(1, 10) == 0


def test_reset_all_clears_all_counts(tmp_path: Path) -> None:
    store = CounterStore(tmp_path / "counts.json")
    store.increment(1, 10)
    store.increment(1, 11)
    store.increment(2, 10)
    store.reset_all()
    assert store.get(1, 10) == 0
    assert store.get(1, 11) == 0
    assert store.get(2, 10) == 0


def test_reset_all_persists_after_reload(tmp_path: Path) -> None:
    path = tmp_path / "counts.json"
    store = CounterStore(path)
    store.increment(1, 10)
    store.increment(1, 11)
    store.reset_all()

    reloaded = CounterStore(path)
    assert reloaded.get(1, 10) == 0
    assert reloaded.get(1, 11) == 0
