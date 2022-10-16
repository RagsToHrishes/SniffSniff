"""

Student Needs to Extract:

- Midterm Final Dates
- Homeworks Due Dates
- Names of GSI, Prof, Office Hours
- Cheatsheets
- Summary of what people missed in class
- Grading Analystics (Midterm Average and so on) (dropped quiz scores, etc)
- 

"""

import cohere
import pandas as pd
import requests
import datetime
from tqdm import tqdm

api_key = 'fVYh2kByOseZVbkvSQWneb9chpcPE7oG1tlIl0Ij'
co = cohere.Client(api_key)

movie_examples = [
("Deadpool 2", "Deadpool 2 | Official HD Deadpool's \"Wet on Wet\" Teaser | 2018"),
("none", "Jordan Peele Just Became the First Black Writer-Director With a $100M Movie Debut"),
("Joker", "Joker Officially Rated “R”"),
("Free Guy", "Ryan Reynolds’ 'Free Guy' Receives July 3, 2020 Release Date - About a bank teller stuck in his routine that discovers he’s an NPC character in brutal open world game."),
("none", "James Cameron congratulates Kevin Feige and Marvel!"),
("Guardians of the Galaxy", "The Cast of Guardians of the Galaxy release statement on James Gunn"),
]

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

