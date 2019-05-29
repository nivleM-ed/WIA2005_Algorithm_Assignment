import copy
import json
import os
import ssl
import sys
import urllib.request
from threading import Thread

import nltk
import plotly
import plotly.graph_objs as go
import plotly.plotly as py
from bs4 import BeautifulSoup
from bs4.element import Comment
from nltk.corpus import stopwords
from plotly import tools

from Map import airport_dict, airports, newspapers


class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

def readNegPos():
    text_file = open("assets/negative.txt", "r")
    negative_array = text_file.read().split(',')
    text_file2 = open("assets/positive.txt", "r")
    positive_array = text_file2.read().split(',')
    stopWord_file = open("assets/stopwords.txt", "r")
    stopWord_list = stopWord_file.read().lower().split("\n")
    return negative_array, positive_array, stopWord_list


positive_freq = []
negative_freq = []
wordAll = []
freqAll = []
negative_array, positive_array, stopWord_list = readNegPos()
stopWordList = {}
probability = {}
items = list(range(0, 13))

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

def printProgressBarWord (iteration, total, prefix = '', decimals = 1, length = 100, fill = '█'):
    
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%%' % (prefix, bar, percent), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)


def removeNone(arr): #remove empty spaces in array
    while("" in arr):
        arr.remove("")

    x = 0
    while x < len(arr):
        arr[x] = arr[x].lower().strip()
        x += 1
    return arr

# remove stopwords using nltk library
def removeStopWord(arr): 
    stop_words = stopwords.words('english')
    arr = [x.lower() for x in arr]
    return [word for word in arr if word not in stop_words]

# calculate the percentage of positive, negative and neutral words
def calculatePercentage(str_split): 
    totalWord = len(str_split)
    positiveWord = 0
    negativeWord = 0
    neutralWord = 0

    removeNone(negative_array)
    removeNone(positive_array)

    for word in str_split:
        if word.lower() in positive_array:
            positiveWord += 1
        elif word.lower() in negative_array:
            negativeWord += 1
        else:
            neutralWord += 1

    positive = round((positiveWord/totalWord)*100)
    negative = round((negativeWord/totalWord)*100)
    neutral = round((neutralWord/totalWord)*100)

    positive_freq.append(positive)
    negative_freq.append(negative)

    return positive, negative, neutral


#calculate the frequency of stopwords in array
def stopWord_freq(str_split, freq): 
    wordFreq = []
    wordList = []
    temp = {}
    for w in str_split:
        if w in stopWord_list:
            wordList.append(w)
            wordFreq.append(str_split.count(w))
    stopWordList[freq] = copy.deepcopy(wordFreq)
    temp['wordFreq'] = wordFreq
    temp['wordList'] = wordList
    stopWordList[freq] = copy.deepcopy(temp)


def Analysis():
    airport_array = airport_dict
    result = {}
    probability = {}
    bil = 0
    print("Analysing political status...\r")
    # printProgressBarWord(0, len(items), prefix='Progress:',
    #                  suffix='Complete', length=50)

    for i in airports:
        printProgressBarWord(bil + 1, len(items), prefix='Analysis:', length=50)
        # print("Words:",bil)
        try:
            # airport_url = airport_array[i]["link"]
            airport_url = newspapers[bil]
            opener = AppURLopener()
            response = opener.open(airport_url)
            html = response.read()
        except Exception as e:
            print(e)
            Analysis()
            
        str = text_from_html(html)
        str_split = str.split(" ")
        str_split = removeNone(str_split)
        stopWord_freq(str_split,bil)

        str_split = removeStopWord(str_split)
        wordAll.append(str_split)
        freqAll.append(wordFreq(str_split))

        positive, negative, neutral = calculatePercentage(str_split)

        result["name"] = airports[bil]
        result["wordFreq"] = wordFreq_set(str_split, wordFreq(str_split))
        result["positive"] = positive
        result["negative"] = negative
        result["neutral"] = neutral

        probability[bil] = copy.deepcopy(result)

        bil += 1

    try:
        with open('assets/positive_freq.txt', 'w', encoding='utf-8')as outfile:
            json.dump(positive_freq, outfile, ensure_ascii=False)
    except Exception as e:
        print(e)

    try:
        with open('assets/negative_freq.txt', 'w', encoding='utf-8')as outfile:
            json.dump(negative_freq, outfile, ensure_ascii=False)
    except Exception as e:
        print(e)

    try:
        with open('assets/political_probability.txt', 'w', encoding='utf-8')as outfile:
            json.dump(probability, outfile, ensure_ascii=False)
    except Exception as e:
        print(e)

    try:
        with open('assets/stopwords_list.txt', 'w', encoding='utf-8')as outfile:
            json.dump(stopWordList, outfile, ensure_ascii=False)
    except Exception as e:
        print(e)

    try:
        with open('assets/wordAll.txt', 'w', encoding='utf-8')as outfile:
            json.dump(wordAll, outfile, ensure_ascii=False)
    except Exception as e:
        print(e)

    try:
        with open('assets/freqAll.txt', 'w', encoding='utf-8')as outfile:
            json.dump(freqAll, outfile, ensure_ascii=False)
    except Exception as e:
        print(e)

    return probability

def getNegFreq():
    with open('assets/negative_freq.txt','r',encoding="utf8") as f:
        neg_freq = json.loads(f.read())
    return neg_freq

def getPosFreq():
    with open('assets/positive_freq.txt','r',encoding="utf8") as f:
        pos_freq = json.loads(f.read())
    return pos_freq

def getStopwordsAll():
    with open('assets/stopwords_list.txt','r',encoding="utf8") as f:
        stopWordList = json.loads(f.read())
    return stopWordList

def getwordAll():
    with open('assets/wordAll.txt','r',encoding="utf8") as f:
        wordAll = json.loads(f.read())
    return wordAll

def getfreqAll():
    with open('assets/freqAll.txt','r',encoding="utf8") as f:
        freqAll = json.loads(f.read())
    return freqAll

def getProb():
    with open('assets/political_probability.txt','r',encoding="utf8") as f:
        probability = json.loads(f.read())
    return probability

def wordFreq(str_split):
    wordfreq = []
    for w in str_split:
        wordfreq.append(str_split.count(w))
    return wordfreq


def wordFreq_set(str_split, wordfreq):
    result = zip(str_split, wordfreq)
    resultSet = list(set(result))
    return resultSet


def readNegPos():
    text_file = open("assets/negative.txt", "r")
    negative_array = text_file.read().split(',')
    text_file2 = open("assets/positive.txt", "r")
    positive_array = text_file2.read().split(',')
    stopWord_file = open("assets/stopwords.txt", "r")
    stopWord_list = stopWord_file.read().lower().split("\n")
    return negative_array, positive_array, stopWord_list


def plotNegVPos(positive_freq, negative_freq):
    city = ["Kuala Lumpur", "Changi", "Abu Dhabi", "Mumbai", "Moscow", "Tokyo", "BeiJing",
            "Shanghai", "Seoul", "Jakarta", "London", "Paris", "Sweeden", "Zimbabwe", "Rio de Janeiro"]
    y0 = positive_freq
    y1 = negative_freq

    data = [
        go.Histogram(
            histfunc="sum",
            y=y0,
            x=city,
            name="positive words"
        ),
        go.Histogram(
            histfunc="sum",
            y=y1,
            x=city,
            name="negative words"
        )
    ]

    py.plot(data, filename='Positive vs Negative words')


def plotStopwords(stopWordList):

    trace0 = go.Histogram(
        x=stopWordList[str(0)]['wordList'],
        y=stopWordList[str(0)]['wordFreq'],
        name=airports[0],
    )
    trace1 = go.Histogram(
        x=stopWordList[str(1)]['wordList'],
        y=stopWordList[str(1)]['wordFreq'],
        name=airports[1],
    )
    trace2 = go.Histogram(
        x=stopWordList[str(2)]['wordList'],
        y=stopWordList[str(2)]['wordFreq'],
        name=airports[2],
    )
    trace3 = go.Histogram(
        x=stopWordList[str(3)]['wordList'],
        y=stopWordList[str(3)]['wordFreq'],
        name=airports[3],
    )
    trace4 = go.Histogram(
        x=stopWordList[str(4)]['wordList'],
        y=stopWordList[str(4)]['wordFreq'],
        name=airports[4],
    )
    trace5 = go.Histogram(
        x=stopWordList[str(5)]['wordList'],
        y=stopWordList[str(5)]['wordFreq'],
        name=airports[5],
    )
    trace6 = go.Histogram(
        x=stopWordList[str(6)]['wordList'],
        y=stopWordList[str(6)]['wordFreq'],
        name=airports[6],
    )
    trace7 = go.Histogram(
        x=stopWordList[str(7)]['wordList'],
        y=stopWordList[str(7)]['wordFreq'],
        name=airports[7],
    )
    trace8 = go.Histogram(
        x=stopWordList[str(8)]['wordList'],
        y=stopWordList[str(8)]['wordFreq'],
        name=airports[8],
    )
    trace9 = go.Histogram(
        x=stopWordList[str(9)]['wordList'],
        y=stopWordList[str(9)]['wordFreq'],
        name=airports[9],
    )
    trace10 = go.Histogram(
        x=stopWordList[str(10)]['wordList'],
        y=stopWordList[str(10)]['wordFreq'],
        name=airports[10],
    )
    trace11 = go.Histogram(
        x=stopWordList[str(11)]['wordList'],
        y=stopWordList[str(11)]['wordFreq'],
        name=airports[11],
    )
    trace12 = go.Histogram(
        x=stopWordList[str(12)]['wordList'],
        y=stopWordList[str(12)]['wordFreq'],
        name=airports[12],
    )

    fig = tools.make_subplots(rows=5, cols=3)
    fig.append_trace(trace0, 1, 1)
    fig.append_trace(trace1, 1, 2)
    fig.append_trace(trace2, 1, 3)
    fig.append_trace(trace3, 2, 1)
    fig.append_trace(trace4, 2, 2)
    fig.append_trace(trace5, 2, 3)
    fig.append_trace(trace6, 3, 1)
    fig.append_trace(trace7, 3, 2)
    fig.append_trace(trace8, 3, 3)
    fig.append_trace(trace9, 4, 1)
    fig.append_trace(trace10, 4, 2)
    fig.append_trace(trace11, 4, 3)
    fig.append_trace(trace12, 5, 1)

    py.plot(fig, filename='stopwordFrequency')


def plotAllWords(wordAll,freqAll):
    trace0 = go.Histogram(
        x=wordAll[0],
        y=freqAll[0],
        name=airports[0],
    )
    trace1 = go.Histogram(
        x=wordAll[1],
        y=freqAll[1],
        name=airports[1],
    )
    trace2 = go.Histogram(
        x=wordAll[2],
        y=freqAll[2],
        name=airports[2],
    )
    trace3 = go.Histogram(
        x=wordAll[3],
        y=freqAll[3],
        name=airports[3],
    )
    trace4 = go.Histogram(
        x=wordAll[4],
        y=freqAll[4],
        name=airports[4],
    )
    trace5 = go.Histogram(
        x=wordAll[5],
        y=freqAll[5],
        name=airports[5],
    )
    trace6 = go.Histogram(
        x=wordAll[6],
        y=freqAll[6],
        name=airports[6],
    )
    trace7 = go.Histogram(
        x=wordAll[7],
        y=freqAll[7],
        name=airports[7],
    )
    trace8 = go.Histogram(
        x=wordAll[8],
        y=freqAll[8],
        name=airports[8],
    )
    trace9 = go.Histogram(
        x=wordAll[9],
        y=freqAll[9],
        name=airports[9],
    )
    trace10 = go.Histogram(
        x=wordAll[10],
        y=freqAll[10],
        name=airports[10],
    )
    trace11 = go.Histogram(
        x=wordAll[11],
        y=freqAll[11],
        name=airports[11],
    )
    trace12 = go.Histogram(
        x=wordAll[12],
        y=freqAll[12],
        name=airports[12],
    )

    fig = tools.make_subplots(rows=5, cols=3)
    fig.append_trace(trace0, 1, 1)
    fig.append_trace(trace1, 1, 2)
    fig.append_trace(trace2, 1, 3)
    fig.append_trace(trace3, 2, 1)
    fig.append_trace(trace4, 2, 2)
    fig.append_trace(trace5, 2, 3)
    fig.append_trace(trace6, 3, 1)
    fig.append_trace(trace7, 3, 2)
    fig.append_trace(trace8, 3, 3)
    fig.append_trace(trace9, 4, 1)
    fig.append_trace(trace10, 4, 2)
    fig.append_trace(trace11, 4, 3)
    fig.append_trace(trace12, 5, 1)

    py.plot(fig, filename='wordFrequency')
