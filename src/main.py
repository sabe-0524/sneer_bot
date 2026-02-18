from __future__ import annotations

import os
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

from src.counter_store import CounterStore
from src.message_handler import build_count_report, build_ramen_announce, should_count_message


BASE_DIR = Path(__file__).resolve().parent.parent
COUNTS_PATH = BASE_DIR / "data" / "counts.json"


def create_bot() -> commands.Bot:
    intents = discord.Intents.default()
    intents.guilds = True
    intents.messages = True
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)
    store = CounterStore(COUNTS_PATH)

    @bot.event
    async def on_ready() -> None:
        if bot.user:
            print(f"Logged in as {bot.user} ({bot.user.id})")

    @bot.event
    async def on_message(message: discord.Message) -> None:
        if should_count_message(
            is_bot=message.author.bot,
            guild_id=message.guild.id if message.guild else None,
            content=message.content,
        ):
            assert message.guild is not None
            count = store.increment(message.guild.id, message.author.id)
            reply = build_count_report(message.author.mention, count)
            await message.channel.send(reply)
            if count % 10 == 0:
                ramen = build_ramen_announce(message.author.mention, count)
                await message.channel.send(ramen)

        await bot.process_commands(message)

    return bot


def main() -> None:
    load_dotenv()
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        raise RuntimeError("DISCORD_BOT_TOKEN is not set")

    bot = create_bot()
    bot.run(token)


if __name__ == "__main__":
    main()
