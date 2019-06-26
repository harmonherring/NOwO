import discord
from discord.ext import commands
import string
import threading
import asyncio
from config import ALLOWED_WORDS, DISALLOWED_WORDS, TOKEN, TIME_TO_SILENCE, OWNER_ID

print("Version " + str(discord.__version__))
bot = commands.Bot(command_prefix='!')


@bot.event
async def on_message(message):
    # apparently commands dont fucking work???
    # i'm lazy and will make this reasonable later (especially saving lmfao im a dumbass)
    if message.author.id == OWNER_ID:
        if message.content.startswith("$illegal"):
            illegal_phrase = message.content.split(" ")[1]
            DISALLOWED_WORDS.append(illegal_phrase)
            return
        elif message.content.startswith("$legal"):
            legal_phrase = message.content.split(" ")[1]
            ALLOWED_WORDS.append(legal_phrase)
            return
        elif message.content.startswith("$remove_illegal"):
            illegal_phrase = message.content.split(" ")[1]
            DISALLOWED_WORDS.remove(illegal_phrase)
            return
        elif message.content.startswith("$remove_legal"):
            legal_phrase = message.content.split(" ")[1]
            ALLOWED_WORDS.remove(legal_phrase)
            return
        elif message.content.startswith("$save"):
            file = open("config.py", "w+")
            file.write('TOKEN = "%s"\n' % TOKEN)
            file.write('TIME_TO_SILENCE = %d\n' % TIME_TO_SILENCE)
            file.write('OWNER_ID = %d\n' % OWNER_ID)
            file.write("ALLOWED_WORDS = [")
            for word in ALLOWED_WORDS:
                file.write('"' + word + '", ')
            file.write("]\n")
            file.write("DISALLOWED_WORDS = [")
            for word in DISALLOWED_WORDS:
                file.write('"' + word + '", ')
            file.write("]\n")
            return
    spaced_text = message.content.translate(str.maketrans('', '', string.punctuation)).lower()
    text = spaced_text.replace(' ', '')
    for word in ALLOWED_WORDS:
        text = text.replace(word, '')
    for banned_word in DISALLOWED_WORDS:
        if banned_word in text:
            if check_space_exception(spaced_text, banned_word):
                member = message.author
                role = discord.utils.get(member.guild.roles, name="UwU Timeout")
                if role:
                    await message.channel.send(
                        "oopsies pwease dun use that wanguage hewe. now u have to sit in timeout"
                    )

                    loop = asyncio.get_event_loop()
                    asyncio.run_coroutine_threadsafe(uwu_penalty(message), loop)
                    return


def check_space_exception(spaced_text, banned_word):
    """
    Replace inner parts of the word with a space and check if that exists in the text
    :param text:
    :param banned_word:
    :return:
    """
    print("checking space extension")
    for i in range(1, len(banned_word)):
        new_phrase = banned_word[:i] + " " + banned_word[i:]
        print(new_phrase)
        if new_phrase in spaced_text:
            return False
    return True


async def uwu_penalty(message):
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
    global bot
    await bot.start(TOKEN, bot=True)


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
