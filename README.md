# sneer_bot

Discordサーバー内でユーザーが `うお` と発言/リアクションした回数を、ユーザー単位でカウントして即時返信するBotです。

## 仕様
- 監視範囲: サーバー全体（DMは対象外）
- トリガー:
  - メッセージ本文が `うお` に一致（前後空白は無視、ひらがな/カタカナ/小文字かなは正規化）
  - リアクションのスタンプ名が `うお` に一致（同じ正規化ルール）
- 集計単位: `guild_id + user_id`
- 返信形式: `@ユーザー うお回数: N回`

## セットアップ
1. Python 3.11+ を用意
2. 依存をインストール

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. 環境変数を設定

```bash
cp .env.example .env
# .env の DISCORD_BOT_TOKEN を設定
```

4. Botを起動

```bash
python -m src.main
```

## テスト
```bash
pytest -q
```

## ファイル構成
- `/Users/abesouichirou/Documents/sneer_bot/src/main.py`: Bot起動・イベント処理
- `/Users/abesouichirou/Documents/sneer_bot/src/counter_store.py`: カウント永続化（JSON）
- `/Users/abesouichirou/Documents/sneer_bot/src/message_handler.py`: 判定/返信メッセージ生成
- `/Users/abesouichirou/Documents/sneer_bot/tests/`: 単体テスト
