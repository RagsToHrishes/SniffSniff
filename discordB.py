from dotenv import load_dotenv
load_dotenv()
import discord
import os

client = discord.Client()

@client.event
async def on_ready():
    print("Logged In")

@client.event
async def on_message(msg):
    if msg.author == client.user:
        print("hey1")
        return
    if msg.content.startswith("$summarize"):
        print("hey")
        await msg.channel.send("Summary: ")

client.run(os.getenv("TOKEN"))


