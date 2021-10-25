import discord
from discord.ext import tasks
from discord.ext import commands
import os
import random
import requests
import json
from replit import db
from flask import Flask
from threading import Thread
import itertools

description = '''A personal bot made for 5WOG.'''

bot = commands.Bot(command_prefix='.', description=description)

# data
ex_list = [
    'kate', 'emrose', 'bea', 'therese', 'rhen', 'maricar', 'marose', 'kayla',
    'hya', 'eljane'
]

ex_response = [
    'We dont talk about trash here.', 'She belongs to the street.','We dont have time for shit talk.', 'Um, irrelevant.', '1/10, disgusting.', 'Ew.'
]

#message_delete_responses = ['Why did you do that!', 'HEY!', 'Whats that for', 'Dont do that', 'Oh that poor message :sob:', ':neutral_face:']

status = itertools.cycle(['with Python', '5WOG'])


# get a random quote online without author
def get_zenqoute():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q']
  return (quote)


# 5wog wise words
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


# connect to uptime robot
app = Flask('')

@app.route('/')
def main():
  return "Your Bot Is Ready"

def run():
  app.run(host="0.0.0.0", port=8000)

def keep_alive():
  server = Thread(target=run)
  server.start()

# bot startup function
@bot.event
async def on_ready():
  keep_alive()
  change_status.start()
  print('Logged in as')
  print(bot.user.name)
  print(bot.user.id)
  print('------')

# message responses
@bot.event
async def on_message(message):
  # prevent bot to respond to itself
  if message.author.id == bot.user.id:
    return

  # responds  if ex is mentioned
  if any(word in message.content for word in ex_list):
    await message.reply(random.choice(ex_response), mention_author=True)

  # replies zenquote
  if message.content.startswith('.quote'):
    quote = get_zenqoute()
    await message.reply(quote)
  
  # adds wise words to database
  if message.content.startswith('.addq'):
    words = message.content.split(".addq ", 1)[1]
    new_quote(words)
    await message.channel.send('Successfully added.')

  # deletes wise words to database
  if message.content.startswith('.delq'):
    wisewords = []
    if "wisewords" in db.keys():
      index = int(message.content.split(".delq ", 1)[1])
      del_quote(index)
      wisewords = db["wisewords"]
    await message.channel.send(wisewords)

  # gets wisewords from repl database
  if "wisewords" in db.keys():
    wisewords = db["wisewords"]
  
  await bot.process_commands(message)

# bot commands
@bot.command()
async def add(ctx, left: float, right: float):
  """Adds two numbers together."""
  await ctx.send(left + right)


@bot.command()
async def subtract(ctx, left: float, right: float):
  """Subtracts two numbers together."""
  await ctx.send(left - right)


@bot.command()
async def multiply(ctx, left: float, right: float):
  """Multiplies two numbers together."""
  await ctx.send(left * right)


@bot.command()
async def divide(ctx, left: float, right: float):
  """Divides two numbers together."""
  await ctx.send(left / right)


@bot.command()
async def roll(ctx, dice: str):
  """Rolls a dice in NdN format."""
  try:
    rolls, limit = map(int, dice.split('d'))
  except Exception:
    await ctx.send('Format has to be in NdN!')
    return

  result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
  await ctx.send(result)


@bot.command()
async def choose(ctx, *choices: str):
  """Chooses between multiple choices."""
  await ctx.send(random.choice(choices))

@bot.command()
async def server(ctx):
  """Displays the server profile."""
  serverembed = discord.Embed(title='5WOG', description='A personal server made by 5wog', color=0x00ff00)
  await ctx.message.reply(embed=serverembed)

@bot.command()
async def wise(ctx):
  """Displays random wise words."""
  await ctx.message.channel.send(random.choice(db["wisewords"]))

@bot.command()
async def tprint(ctx, *words: str):
  """a test command"""
  print(words)

# discord presence
@tasks.loop(seconds=10)
async def change_status():
  await bot.change_presence(activity=discord.Game(next(status)))

# run bot
my_secret = os.environ['token']
bot.run(my_secret)
