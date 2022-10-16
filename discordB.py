from dotenv import load_dotenv
load_dotenv()
import discord
import os
from extract import cohereExtractor
from datetime import datetime
from profanity_filter import ProfanityFilter


pf = ProfanityFilter()

ExampleDict = {}
#Get Prompt Examples for NLP


def updateDictionary():
    global ExampleDict
    ExampleDict = {}
    #Get Prompt Examples for NLP
    with open('./examples/ExamDates.txt') as f:
        temp = "Exam Dates"
        exampletemp = None
        for line in f.readlines():
            line = line.replace("\n","")
            if len(line) > 0:
                if line[0] == "$":
                    ExampleDict[temp] = {}
                if(line[0:7]) == "Example":
                    exampletemp = line[8:]
                if(line[0:5]) == "Label":
                    ExampleDict[temp][exampletemp] = line[6:]

    with open('./examples/CourseStaff.txt') as f:
        temp = "Course Staff"
        exampletemp = None
        for line in f.readlines():
            line = line.replace("\n","")
            if len(line) > 0:
                if line[0] == "$":
                    ExampleDict[temp] = {}
                if(line[0:7]) == "Example":
                    exampletemp = line[8:]
                if(line[0:5]) == "Label":
                    ExampleDict[temp][exampletemp] = line[6:]

    with open('./examples/Summary.txt') as f:
        temp = "Summary"
        exampletemp = None
        for line in f.readlines():
            line = line.replace("\n","")
            if len(line) > 0:
                if line[0] == "$":
                    ExampleDict[temp] = {}
                if(line[0:7]) == "Example":
                    exampletemp = line[8:]
                if(line[0:5]) == "Label":
                    ExampleDict[temp][exampletemp] = line[6:]

updateDictionary()


DateExtractor = cohereExtractor([desc for desc in ExampleDict["Exam Dates"].keys()], 
                                [ExampleDict["Exam Dates"][key] for key in ExampleDict["Exam Dates"].keys()], [],
                                       "", 
                                       "extract the exam dates from the post:")

CourseStaffExtractor = cohereExtractor([desc for desc in ExampleDict["Course Staff"].keys()], 
                                [ExampleDict["Course Staff"][key] for key in ExampleDict["Course Staff"].keys()], [],
                                       "", 
                                       "extract the course staff from the post:")

SummaryExtractor = cohereExtractor([desc for desc in ExampleDict["Summary"].keys()], 
                                [ExampleDict["Summary"][key] for key in ExampleDict["Summary"].keys()], [],
                                       "", 
                                       "extract the summary from the post:")

async def sniffExamDates(msg):
    ExamandDates = []
    msgs = []
    async for mes in msg.channel.history(limit=10000): # As an example, I've set the limit to 10000
            if mes.author != client.user:                        # meaning it'll read 10000 messages instead of           
                if not is_command(mes.content):  
                    mes.content = pf.censor(mes.content)
                    mes.content.replace("*", "@")
                    label = DateExtractor.extract(mes.content)
                    if label != "None" and ("MainMidterm" in label or "Midterm1" in label or "Midterm2" in label):
                        ExamandDates.append(label)
                        print(mes.content, label)
                        msgs.append(mes)
                        tocheck = ""
                        for i in ExamandDates:
                            tocheck += i
                        print(tocheck)
                        if ("MainMidterm" in tocheck and "Final" in tocheck) or ("Midterm1" in tocheck and "Midterm2" in tocheck) or ("Midterm1" in tocheck and "Midterm2" in tocheck and "Final" in tocheck):
                            print("done")
                            break

    return (ExamandDates,msgs)

async def sniffCourseStaff(msg):
    CourseStaff = []
    msgs = []
    async for mes in msg.channel.history(limit=10): # As an example, I've set the limit to 10000
            if mes.author != client.user:                        # meaning it'll read 10000 messages instead of           
                if not is_command(mes.content):  
                    mes.content = pf.censor(mes.content)
                    mes.content.replace("*", "@")
                    label = CourseStaffExtractor.extract(mes.content)
                    print(label)
                    if label != "None" and ("professor" in label or "GSI" in label) and all([label not in s for s in CourseStaff]):
                        CourseStaff.append(label)
                        print(mes.content, label)
                        msgs.append(mes)
    return (CourseStaff,msgs)

    

async def sniffSummary(msg, limit=10):
    msgContent = ""

    async for mes in msg.channel.history(limit=limit): # As an example, I've set the limit to 10000
            if mes.author != client.user:                        # meaning it'll read 10000 messages instead of           
                if not is_command(mes.content):  
                    mes.content = pf.censor(mes.content)
                    mes.content.replace("*", "@")
                    msgContent += mes.content + " "
                    
    summary = SummaryExtractor.extract(msgContent)

    return summary
                    
                        
   

client = discord.Client()

@client.event
async def on_ready():
    print("Logged In")

def is_command(msg):
    return msg[0] == "$"

@client.event
async def on_message(msg):
    global DateExtractor
    global CourseStaffExtractor
    global SummaryExtractor
    if msg.author == client.user:
        return
    if msg.content.startswith("$sniff examdates"):
        sols = await sniffExamDates(msg)
        if len(sols[0]) == 0:
            await msg.channel.send("No useful information found")
        else:
            labelToSend = ""
            for i in sols[0]:
                labelToSend += i + " "
            msgToSend = "Category: Exam Dates\n"+labelToSend
            for i in sols[1]:
                msgToSend += "\nFrom: msg: \"" + i.content + "\" By: " + str(i.author) + " At: " + i.created_at.strftime("%m/%d/%Y, %H:%M:%S")
            await msg.channel.send(msgToSend)

    if msg.content.startswith("$sniff coursestaff"):
        sols = await sniffCourseStaff(msg)
        if len(sols[0]) == 0:
            await msg.channel.send("No useful information found")
        else:
            labelToSend = ""
            for i in sols[0]:
                labelToSend += i + " "
            msgToSend = "Category: Course Staff\n"+labelToSend
            for i in sols[1]:
                msgToSend += "\nFrom: msg: \"" + i.content + "\" By: " + str(i.author) + " At: " + i.created_at.strftime("%m/%d/%Y, %H:%M:%S")
            await msg.channel.send(msgToSend)

    if msg.content.startswith("$sniff summary"):
        msgparams = msg.content.split(" ")
        summ = await sniffSummary(msg)

        if len(summ) == 0:
            await msg.channel.send("No useful information found")
        else:
            msgToSend = "Category: Channel Summary\n"+summ
            await msg.channel.send(msgToSend)


    if msg.content.startswith("$sniff improve"):
        msgLabelToPut = msg.content[15:]
        async for mes in msg.channel.history(limit=10000):
            if mes.author == client.user:   
                categoryOfExtract = mes.content.split("\n")[0]
                categoryOfExtract = categoryOfExtract[10:]
                msgDataExample = ""
                for example in mes.content.split("\n")[2:]:
                    temp = example.split(":")[2]
                    temp = temp[2:len(temp)-4]
                    msgDataExample += temp + " "
                if categoryOfExtract == "Exam Dates":
                    with open('./examples/ExamDates.txt', "a") as f:
                        f.write("\n---\nExample:"+msgDataExample+"\nLabel:"+msgLabelToPut)
                if categoryOfExtract == "Course Staff":
                    with open('./examples/CourseStaff.txt', "a") as f:
                        f.write("\n---\nExample:"+msgDataExample+"\nLabel:"+msgLabelToPut)
                if categoryOfExtract == "Summary":
                    with open('./examples/Summary.txt', "a") as f:
                        f.write("\n---\nExample:"+msgDataExample+"\nLabel:"+msgLabelToPut)                   
                updateDictionary()
                DateExtractor = cohereExtractor([desc for desc in ExampleDict["Exam Dates"].keys()], 
                                [ExampleDict["Exam Dates"][key] for key in ExampleDict["Exam Dates"].keys()], [],
                                       "", 
                                       "extract the exam dates from the post:")

                CourseStaffExtractor = cohereExtractor([desc for desc in ExampleDict["Course Staff"].keys()], 
                                [ExampleDict["Course Staff"][key] for key in ExampleDict["Course Staff"].keys()], [],
                                       "", 
                                       "extract the course staff from the post:")

                SummaryExtractor = cohereExtractor([desc for desc in ExampleDict["Summary"].keys()], 
                                [ExampleDict["Summary"][key] for key in ExampleDict["Summary"].keys()], [],
                                       "", 
                                       "extract the summary from the post:")
                
                break
                


                


                
                
                    

                
                

client.run(os.getenv("TOKEN"))


