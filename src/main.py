from __future__ import annotations

import os
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

from src.counter_store import CounterStore
from src.message_handler import (
    build_count_report,
    build_ramen_announce,
    should_count_message,
    should_count_reaction,
)


BASE_DIR = Path(__file__).resolve().parent.parent
COUNTS_PATH = BASE_DIR / "data" / "counts.json"


def _reaction_name(emoji: str | discord.Emoji | discord.PartialEmoji) -> str:
    if isinstance(emoji, str):
        return emoji
    return emoji.name or ""


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

    async def send_count_report(
        *, guild_id: int, user: discord.abc.User, channel: discord.abc.Messageable
    ) -> None:
        count = store.increment(guild_id, user.id)
        reply = build_count_report(user.mention, count)
        await channel.send(reply)
        if count % 10 == 0:
            ramen = build_ramen_announce(user.mention, count)
            await channel.send(ramen)

    @bot.event
    async def on_message(message: discord.Message) -> None:
        if should_count_message(
            is_bot=message.author.bot,
            guild_id=message.guild.id if message.guild else None,
            content=message.content,
        ):
            assert message.guild is not None
            await send_count_report(
                guild_id=message.guild.id,
                user=message.author,
                channel=message.channel,
            )

        await bot.process_commands(message)

    @bot.event
    async def on_reaction_add(
        reaction: discord.Reaction, user: discord.User | discord.Member
    ) -> None:
        guild = reaction.message.guild
        if should_count_reaction(
            is_bot=user.bot,
            guild_id=guild.id if guild else None,
            reaction_name=_reaction_name(reaction.emoji),
        ):
            assert guild is not None
            await send_count_report(
                guild_id=guild.id,
                user=user,
                channel=reaction.message.channel,
            )

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
