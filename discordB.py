from dotenv import load_dotenv
load_dotenv()
import discord
import os
from extract import cohereExtractor
from datetime import datetime
from profanity_filter import ProfanityFilter
import cohere

api_key = 'fVYh2kByOseZVbkvSQWneb9chpcPE7oG1tlIl0Ij'

co = cohere.Client(api_key)

pf = ProfanityFilter()

ExampleDict = {}
#Get Prompt Examples for NLP

prompt = ""

def updateDictionary():
    global ExampleDict
    global prompt
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

    prompt=""
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
                    prompt += "Passage: " + exampletemp + "\n\n"
                if(line[0:5]) == "Label":
                    ExampleDict[temp][exampletemp] = line[6:]
                    prompt += "TLDR: "+line[6:] + "\n--\n"

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



async def sniffExamDates(msg, maxCount=10):
    ExamandDates = []
    msgs = []
    count = 0
    async for mes in msg.channel.history(limit=100): # As an example, I've set the limit to 10000
            if count >= maxCount:
                break
            if mes.author != client.user:                        # meaning it'll read 10000 messages instead of           
                if not is_command(mes.content):  
                    count += 1
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

async def sniffCourseStaff(msg, maxCount=10):
    CourseStaff = []
    msgs = []
    count = 0
    async for mes in msg.channel.history(limit=100): # As an example, I've set the limit to 10000
            if count >= maxCount:
                break
            if mes.author != client.user:                        # meaning it'll read 10000 messages instead of           
                if not is_command(mes.content):  
                    count += 1
                    mes.content = pf.censor(mes.content)
                    mes.content.replace("*", "@")
                    label = CourseStaffExtractor.extract(mes.content)
                    print(label)
                    if label != "None" and ("professor" in label or "GSI" in label) and all([label not in s for s in CourseStaff]):
                        CourseStaff.append(label)
                        print(mes.content, label)
                        msgs.append(mes)
    return (CourseStaff,msgs)

    

async def sniffSummary(msg, maxCount=10):
    global prompt
    msgContent = ""

    count = 0
    async for mes in msg.channel.history(limit=100): # As an example, I've set the limit to 10000
            if count >= maxCount:
                break
            if mes.author != client.user:                        # meaning it'll read 10000 messages instead of           
                if not is_command(mes.content):  
                    count += 1
                    mes.content = pf.censor(mes.content)
                    mes.content.replace("*", "@")
                    msgContent += mes.content + " "
                    
    newPrompt = prompt + "Passage: " + msgContent + "\n\n"+ "TLDR:"

    print(newPrompt)
    #summary = SummaryExtractor.extract(msgContent)
    Summarizer = co.generate( 
        model='large', 
        prompt = newPrompt,
        max_tokens=1000, 
        temperature=0.9,
        stop_sequences=["--"])
    summary = Summarizer.generations[0].text


    return (summary[:len(summary)-2], msgContent)
                    
                        
   

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
        if len(msg.content.split(" ")) > 2:
            maxCount = int(msg.content.split(" ")[2])
            sols = await sniffExamDates(msg,maxCount)
        else:
            sols = await sniffExamDates(msg)
        sols = await sniffExamDates(msg, limit)
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
        if len(msg.content.split(" ")) > 2:
            maxCount = int(msg.content.split(" ")[2])
            sols = await sniffCourseStaff(msg,maxCount)
        else:
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
        if len(msg.content.split(" ")) > 2:
            maxCount = int(msg.content.split(" ")[2])
            summ = await sniffSummary(msg, maxCount)
        else:
            summ = await sniffSummary(msg)
        summ = summ[0]

        if summ == "None":
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
                if categoryOfExtract == "Channel Summary":
                    content = None
                    async for mes in msg.channel.history(limit=10000):
                        if mes.author != client.user:
                            if is_command(mes.content):
                                if mes.content.split(" ")[1] == "summary":
                                    lim = None
                                    if len(mes.content.split(" ")) > 2:
                                        lim = int(mes.content.split(" ")[2])
                                    content = await sniffSummary(mes,lim)
                                    content = content[1]
                                    break

                                
                    if content != None:
                        with open('./examples/Summary.txt', "a") as f:
                            f.write("\n---\nExample:"+content+"\nLabel:"+msgLabelToPut)                   
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


