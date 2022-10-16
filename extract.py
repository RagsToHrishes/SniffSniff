import cohere
import pandas as pd
import requests
import datetime
from tqdm import tqdm

api_key = 'fVYh2kByOseZVbkvSQWneb9chpcPE7oG1tlIl0Ij'

co = cohere.Client(api_key)



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
          max_tokens=100,
          temperature=0.1,
          stop_sequences=["\n"])
      return(extraction.generations[0].text[:-1])



"""                  
examp = "bruh the midtern is oct 13 and i cant make it bbbbb"

try:
    extracted_text = DateExtractor.extract(examp)
    print(extracted_text)
except Exception as e:
    print('ERROR: ', e)
"""

