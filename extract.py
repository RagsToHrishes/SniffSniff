import cohere
import pandas as pd
import requests
import datetime
from tqdm import tqdm

api_key = 'fVYh2kByOseZVbkvSQWneb9chpcPE7oG1tlIl0Ij'

co = cohere.Client(api_key)

ExampleDict = {}
#Get Prompt Examples for NLP
with open('examples.txt') as f:
    temp = None
    exampletemp = None
    for line in f.readlines():
        line = line.replace("\n","");
        if(len(line) > 0):
            if(line[0] == "$"):
                ExampleDict[line[1:]] = {}
                temp = line[1:]
            if(line[0:7]) == "Example":
                exampletemp = line[8:]
            if(line[0:5]) == "Label":
                ExampleDict[temp][exampletemp] = line[6:]


class cohereExtractor():
    def __init__(self, examples, example_labels, labels, task_desciption, example_prompt):
        self.examples = examples
        self.example_labels = example_labels
        self.labels = labels
        self.task_desciption = task_desciption
        self.example_prompt = example_prompt

    def make_prompt(self, example):
        examples = self.examples + [example]
        labels = self.example_labels + [""]
        return (self.task_desciption +
                "\n---\n".join( [examples[i] + "\n" +
                                self.example_prompt + 
                                 labels[i] for i in range(len(examples))]))

    def extract(self, example):
      extraction = co.generate(
          model='large',
          prompt=self.make_prompt(example),
          max_tokens=10,
          temperature=0.1,
          stop_sequences=["\n"])
      return(extraction.generations[0].text[:-1])


DateExtractor = cohereExtractor([desc for desc in ExampleDict["Exam Dates"].keys()], 
                                [ExampleDict["Exam Dates"][key] for key in ExampleDict["Exam Dates"].keys()], [],
                                       "", 
                                       "extract the exam dates from the post:")

"""                  
examp = "bruh the midtern is oct 13 and i cant make it bbbbb"

try:
    extracted_text = DateExtractor.extract(examp)
    print(extracted_text)
except Exception as e:
    print('ERROR: ', e)
"""

