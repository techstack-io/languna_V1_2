from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

import textstat
import bs4 as bs
import urllib.request
import numpy as np
import pandas as pd
import requests
import string
import heapq
import time
import nltk
import re

def index(request):
    return render(request, 'pages/index.html')

def models(request):
    return render(request, 'pages/models.html')

def count(request):

    fulltext = request.GET['fulltext']
    # ------------------------------ #
    summary = nltk.download('punkt')
    nltk.download('stopwords')
    # Raw Text
    text = re.sub(r'\[[0-9]*\]', ' ', fulltext)
    text = re.sub(r'\s+', ' ', fulltext)
    # Clean Text
    clean_text = text.lower()
    clean_text = re.sub(r'\W', ' ', clean_text)
    clean_text = re.sub(r'\d', ' ', clean_text)
    clean_text = re.sub(r'\s+', ' ', clean_text)
    stopwords = nltk.corpus.stopwords.words('english')
    word_frequency = nltk.FreqDist(nltk.word_tokenize
                                    (clean_text))
    # ---------- Word Dictionary ------------ #
    word2count = {}
    for word in nltk.word_tokenize(clean_text):
        if word not in stopwords:
            if word not in word2count.keys():
                word2count[word] = 1
            else:
                word2count[word] += 1
                # Convert word2count dict to a list
                dict2list=list(word2count.items())
                # Sort list in descending order
                dict2list = sorted(word2count.items(), key=lambda x:x[1], reverse=True)
                # First 7 words in sorted list of weighted words in descending order
                weighted_words_des = dict2list[:7]
                # --- Dicts 
                # Covert sorted list back to dict (this is the complete dict)
                sortdict = dict(dict2list)
                # Sorted dict
                d=dict(weighted_words_des)
                # Separate keys and values
                keys = d.keys()
                val = d.values()
                # Convert keys and values into a list
                # This will be our x and y axis for our chart
                lkeys = list(keys)
                new_lkeys = str(lkeys)[1:-1]
 
                vkeys = list(val)

    highest_frequency = max(word2count.values())
    wfhigh = max(word_frequency.keys())

    # Weighted Words
    for word in word2count.keys():
        word2count[word] = (word2count[word] / highest_frequency)

    # Tokenize sentences
    sentences = nltk.sent_tokenize(text)

    # Sentence Dictionary
    sent2score = {}
    for sentence in sentences:
        for word in nltk.word_tokenize(sentence.lower()):
            if word in word2count.keys():
                if len(sentence.split(' ')) < 25:
                    if sentence not in sent2score.keys():
                        sent2score[sentence] = word2count[word]
                    else:
                        sent2score[sentence] += word2count[word]

    best_sentences = heapq.nlargest(10, sent2score, key=sent2score.get)
    summary = ' '.join(best_sentences)
    summary
    highest_frequency
    wordlist = fulltext.split()
    wfhigh
    new_lkeys
    ease = textstat.flesch_reading_ease(fulltext)
    rtime = textstat.reading_time(fulltext, ms_per_char=14.69)
    err = 'ERROR'



    if len(fulltext) == 0 and len(fulltext) < 1000:
        return render(request, 'pages/count.html', {'fulltext':'Please enter a minimum of 1,000 characters', 'err':err})
    
    elif ease < 0:
        warning = "Extremely complex texts could have a negative score. Lower and negative scores represent a text with more complexity. Typically, though, most texts will fit within a range of 10 to 100. A score between 60 and 70 would be average."
        return render(request, 'pages/count.html', {'fulltext':fulltext, 'warning':warning})
    elif 0 <= ease <= 10:
        desc1 = "this text is extremely difficult to read, and is considered a scholarly article. View the complete readability table under 'Readability Models'."
        return render(request, 'pages/count.html', {'fulltext':fulltext, 'desc2':desc2, 'ease':ease, 'rtime':rtime, 'summary':summary, 'highest_frequency':highest_frequency, 'no_of_words':len(wordlist), 'new_lkeys':new_lkeysy})
    elif 10 <= ease <= 30:
        desc2 = "this text is very difficult to read, and best understood by college students. View the complete readability table under 'Readability Models'."
        return render(request, 'pages/count.html', {'fulltext':fulltext, 'desc2':desc2, 'ease':ease, 'rtime':rtime, 'summary':summary, 'highest_frequency':highest_frequency, 'no_of_words':len(wordlist), 'new_lkeys':new_lkeys})
    elif 30 <= ease <= 50:
        desc3 = "this text is difficult to read, and best understood by university graduates. View the complete readability table under Readability Models."
        return render(request, 'pages/count.html', {'fulltext':fulltext,'desc3':desc3, 'ease':ease, 'rtime':rtime, 'summary':summary, 'highest_frequency':highest_frequency, 'no_of_words':len(wordlist), 'new_lkeys':new_lkeys})
    elif 50 <= ease <= 60:
        desc4 = "this text is fairly difficult to read. View the complete readability table under 'Readability Models'."
        return render(request, 'pages/count.html', {'fulltext':fulltext,'desc4':desc4, 'ease':ease, 'rtime':rtime, 'summary':summary, 'highest_frequency':highest_frequency, 'no_of_words':len(wordlist), 'new_lkeys':new_lkeys})
    elif 60 <= ease <= 70:
        desc6 = "this text is easily understood by 13 to 15 year old students. If you're a content writer, this is your sweet spot. View the complete readability table under 'Readability Models'."
        return render(request, 'pages/count.html', {'fulltext':fulltext,'desc6':desc6, 'ease':ease, 'rtime':rtime, 'summary':summary, 'highest_frequency':highest_frequency, 'no_of_words':len(wordlist), 'new_lkeys':new_lkeys})
    elif 70 <= ease <= 80:
        desc7 = "this text is easily understood by 13 to 15 year old students. If you're a content writer, this is your sweet spot. View the complete readability table under 'Readability Models'."
        return render(request, 'pages/count.html', {'fulltext':fulltext,'desc7':desc7, 'ease':ease, 'rtime':rtime, 'summary':summary, 'highest_frequency':highest_frequency, 'no_of_words':len(wordlist), 'new_lkeys':new_lkeys})
    elif 80 <= ease <= 100:
        desc8 = "this text is very easily understood by 10 to 12 year old students, or a 5th grade reading level."
        return render(request, 'pages/count.html', {'fulltext':fulltext,'desc8':desc8, 'ease':ease, 'rtime':rtime, 'summary':summary, 'highest_frequency':highest_frequency, 'no_of_words':len(wordlist), 'new_lkeys':new_lkeys})
