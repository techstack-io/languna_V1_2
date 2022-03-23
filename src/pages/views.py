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
    # wordlist = fulltext.split()
    # return render(request, 'pages/count.html', {'fulltext':fulltext, 'count':len(wordlist)})

    if len(fulltext) != 0 and len(fulltext) > 1000:
        time.sleep(2)
        # ---
        ease = textstat.flesch_reading_ease(fulltext)
        return render(request, 'pages/count.html', {'fulltext':fulltext, 'ease':ease})

        if ease < 0:
            warning = "Extremely complex texts could have a negative score. Lower and negative scores represent a text with more complexity. Typically, though, most texts will fit within a range of 10 to 100. A score between 60 and 70 would be average."
            return render(request, 'pages/count.html', {'fulltext':fulltext, 'warning':warning})
        
        elif 30 <= ease <= 50:
            score = "This text is difficult to read, and best understood by university graduates. View the complete readability table under Readability Models."
            return render(request, 'pages/count.html', {'ease':score})
                             
        else:
            err = 'ERROR'
            return render(request, 'pages/count.html', {'fulltext':'Please enter a minimum of 1,000 characters', 'err':err})


    
