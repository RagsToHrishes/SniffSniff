from dotenv import load_dotenv
load_dotenv()
import discord
import os
from extract import cohereExtractor


ExampleDict = {}
#Get Prompt Examples for NLP
with open('examples.txt') as f:
    temp = None
    exampletemp = None
    for line in f.readlines():
        line = line.replace("\n","")
        if(line[0] == "$"):
            ExampleDict[line[1:]] = {}
            temp = line[1:]
        if(line[0:7]) == "Example":
            exampletemp = line[8:]
        if(line[0:5]) == "Label":
            ExampleDict[temp][exampletemp] = line[6:]

DateExtractor = cohereExtractor([desc for desc in ExampleDict["Exam Dates"].keys()], 
                                [ExampleDict["Exam Dates"][key] for key in ExampleDict["Exam Dates"].keys()], [],
                                       "", 
                                       "extract the exam dates from the post:")


client = discord.Client()

@client.event
async def on_ready():
    print("Logged In")

def is_command(msg):
    return msg[0] == "$"

@client.event
async def on_message(msg):
    print(msg)
    if msg.author == client.user:
        return
    if msg.content.startswith("$sniff examdates"):
        async for mes in msg.channel.history(limit=10000): # As an example, I've set the limit to 10000
            if mes.author != client.user:                        # meaning it'll read 10000 messages instead of           
                if not is_command(mes.content):  
                    label = DateExtractor.extract(mes.content)
                                           # the default amount of 100        
                    if label != "None":
                        await msg.channel.send(label)
                        break
    if msg.content.startswith("$sniff improve"):
        async for mes in msg.channel.history(limit=10000): # As an example, I've set the limit to 10000
            if mes.author != client.user:                        # meaning it'll read 10000 messages instead of           
                if not is_command(mes.content):  
                    label = DateExtractor.extract(mes.content)
                                           # the default amount of 100        
                    if label != "None":
                        await msg.channel.send(labldsf + " From: msg:" + " mes.")
                        break


client.run(os.getenv("TOKEN"))


