import discord
from discord.ext import tasks
import os
import random
from discord.ext.commands.core import command
import requests
import json
from replit import db
from flask import Flask
from threading import Thread
import itertools
from discord.ext import commands

bot = commands.Bot(command_prefix='$')

exes = [
    'kate', 'emrose', 'bea', 'therese', 'rhen', 'maricar', 'marose', 'kayla',
    'hya', 'eljane'
]
ex_response = [
    'Do not mention that name!', 'Oh, alright. Mention her. I dare you',
    'Nani dafuq', 'Tsk Tsk Tsk', 'EX ALERT!!! STFU', 'We dont know that girl'
]


app = Flask('')

@app.route('/')
def main():
  return "Your Bot Is Ready"

def run():
  app.run(host="0.0.0.0", port=8000)

def keep_alive():
  server = Thread(target=run)
  server.start()

def new_quote(words):
    if "wisewords" in db.keys():
        wisewords = db["wisewords"]
        wisewords.append(words)
        db["wisewords"] = wisewords
    else:
        db["wisewords"] = [words]


def del_quote(index):
    wisewords = db["wisewords"]
    if len(wisewords) > index:
        del wisewords[index]
        db["wisewords"] = wisewords


def get_qoute():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q']
    return (quote)

@bot.event
async def on_ready():
  keep_alive()
  change_status.start()
  print("Your bot is ready")

@tasks.loop(seconds=10)
async def change_status():
  await bot.change_presence(activity=discord.Game(next(status)))

status = itertools.cycle(['with Python', '5wog'])

@bot.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = message.content
    channel = str(message.channel.name)
    print(f'{username}: {user_message} [{channel}]')

    if message.author == bot.user:
        return

    if "wisewords" in db.keys():
        wisewords = db["wisewords"]

    if user_message.startswith('addq'):
        words = user_message.split("addq ", 1)[1]
        new_quote(words)
        await message.channel.send('Nabutang na')

    if user_message.startswith('delq'):
        wisewords = []
        if "wisewords" in db.keys():
            index = int(user_message.split("delq ", 1)[1])
            del_quote(index)
            wisewords = db["wisewords"]
        await message.channel.send(wisewords)

    if user_message.startswith('hoy'):
        await message.channel.send('Unsa man bai')

    if user_message.startswith('5wog'):
        await message.channel.send(random.choice(db["wisewords"]))

    if any(word in user_message for word in exes):
        await message.channel.send(random.choice(ex_response))

    if user_message.startswith('tabang'):
        quote = get_qoute()
        await message.channel.send(quote)


my_secret = os.environ['token']
bot.run(my_secret)
