# Discord-related Imports
import discord
from discord import Webhook, RequestsWebhookAdapter, File
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

#Python-related Imports
import asyncio
import json
import datetime
import time
from bs4 import BeautifulSoup as bs
import urllib
from urllib.request import urlopen, Request
import re
import requests

bot = commands.Bot(command_prefix="!")

global currentStats
global lastStats 

async def _save(data):
        with open('data.json', 'w') as f:
            json.dump(data, f)

async def getStats():
    r = requests.get('https://api.covid.stream/latest/numbers')
    j = r.json()
    print(j)
    i = j["data"]["totalConfirmedNumbers"]
    d = j["data"]["totalDeathNumbers"]
    r = j["data"]["totalRecoveredNumbers"]
    return i, d, r



@bot.event
async def on_ready():
    print("Username: " + bot.user.name)
    print("User ID: ", bot.user.id)
    await bot.change_presence(activity=discord.Streaming(name="stats on the virus", url="https://twitter.com/whojcks"))


@bot.command(pass_context=True)
async def stats(ctx):

    infections, deaths, recovered = await getStats()
    embed = discord.Embed(color=discord.Color(0xfffffe),
                          title="Global Coronavirus Statistics")
    embed.add_field(name="Infections", value=infections, inline=True)
    embed.add_field(name="Deaths", value=deaths, inline=True)
    embed.add_field(name="Recoveries", value=recovered, inline=True)

    embed.set_footer(
        text=f"Brought to you by covid.stream's API | Data from JHU CSSE")

    await ctx.send(embed=embed)

bot.run('')
