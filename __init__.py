import discord
import string
import threading
from time import sleep, time
import asyncio
import queue
from multiprocessing import Process, Queue
import concurrent.futures

TOKEN = ""
PERMITTED_WORDS = [
    "microworld",
    "autoworker",
    "stuccowork",
    "coworker",
    "blowoff",
    "showoff",
    "blowout",
    "doowop"
]
DISALLOWED_WORDS = [
    "uwu",
    "owo",
    "rawr",
    "x3"
]

q = queue.Queue()
print("Version " + str(discord.__version__))
TIME_TO_SILENCE = 60


class MyClient(discord.Client):
    async def on_message(self, message):
        text = message.content.translate(str.maketrans('', '', string.punctuation)).replace(' ', '').lower()
        for word in PERMITTED_WORDS:
            text.replace(word, '')
        if "uwu" in text or "owo" in text:
            member = message.author
            role = discord.utils.get(member.guild.roles, name="UwU Timeout")
            if role:
                await message.channel.send(
                    "oopsies pwease dun use that wanguage hewe. now u have to sit in timeout"
                )

                loop = asyncio.get_event_loop()
                asyncio.run_coroutine_threadsafe(uwu_penalty(message), loop)


async def uwu_penalty(message):
    print(message)
    print("hi")
    roles = message.author.roles
    for role in roles:
        if role.name != "@everyone":
            await message.author.remove_roles(role, reason="uwuing")
            print("Removed role: " + role.name)
    uwu_role = discord.utils.get(message.author.guild.roles, name="UwU Timeout")
    await message.author.add_roles(uwu_role, reason="uwuing")
    await asyncio.sleep(TIME_TO_SILENCE)
    print("added uwu role")
    await message.author.remove_roles(uwu_role, reason="uwuing")
    print("removed uwu role")
    for role in roles:
        print(role)
        if role.name != "@everyone":
            await message.author.add_roles(role, reason="uwuing")


async def start():
    client = MyClient()
    await client.start("")


def run_it_forever(loop):
    loop.run_forever()


def start_client():
    loop = asyncio.get_event_loop()
    loop.create_task(start())
    thread = threading.Thread(target=run_it_forever, args=(loop,))
    thread.start()


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


def start_banner():
    new_loop = asyncio.new_event_loop()
    t = threading.Thread(target=start_loop, args=(new_loop,))
    t.start()


start_client()
start_banner()
