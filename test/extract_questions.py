#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 15:03:02 2019

@author: domonique_hodge
"""
import pickle
import json
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from summa.summarizer import summarize

import pynlp
from pynlp import StanfordCoreNLP

#Extract questions from papers
papers = json.load( open( "/Users/domonique_hodge/Documents/External Clients/DARPA/cleanedArticles-03042019.json", "rb" ) )

all_questions = []
        
        
for i in papers.keys():
    print(i)
    
    
    all_text = papers[i]['text']
    
    try:
        sentence = sent_tokenize(all_text)
        sentence_index = [i for i, x in enumerate(sentence) if x[-1:] == "?"]
    
        num_quest = len(sentence_index)
    
        if num_quest >0:
            for j in range(0,num_quest):
                question = sentence[[i for i, x in enumerate(sentence) if x[-1:] == "?"][j]]
                all_questions.append(question)
    except:
        print('Error occured with tokenizing article')
        
no_duplicate_quest = list(dict.fromkeys(all_questions))

#write to txt file
       
with open('/Users/domonique_hodge/Documents/External Clients/DARPA/QG Net update/questions_v2.txt', 'w') as f:
    for item in no_duplicate_quest:
        f.write("%s\n" % item)
        
