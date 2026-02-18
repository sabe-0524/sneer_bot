"""全ユーザーのうお回数をリセットするCLIスクリプト。

使い方:
    python scripts/reset_counts.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.counter_store import CounterStore

COUNTS_PATH = Path(__file__).resolve().parent.parent / "data" / "counts.json"


def main() -> None:
    store = CounterStore(COUNTS_PATH)
    answer = input("全員のうお回数をリセットします。よろしいですか？ [y/N]: ").strip().lower()
    if answer != "y":
        print("キャンセルしました。")
        return
    store.reset_all()
    print("リセットしました。")


if __name__ == "__main__":
    main()
