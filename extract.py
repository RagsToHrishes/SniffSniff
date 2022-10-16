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


cohereMovieExtractor = cohereExtractor([e[1] for e in movie_examples], 
                                       [e[0] for e in movie_examples], [],
                                       "", 
                                       "extract the movie title from the post:")



