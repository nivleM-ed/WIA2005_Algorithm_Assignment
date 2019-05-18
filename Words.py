import urllib.request,nltk, copy, json, ssl, plotly, os, sys
import plotly.plotly as py
import plotly.graph_objs as go
from plotly import tools
from bs4 import BeautifulSoup
from bs4.element import Comment
from nltk.corpus import stopwords
from Map import airport_dict
from threading import Thread
from Map import printProgressBar, items


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


try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context


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
def stopWord_freq(str_split): 
    wordFreq2 = []
    wordList = []
    for w in str_split:
        if w in stopWord_list:
            wordList.append(w)
            wordFreq2.append(str_split.count(w))
    result = zip(wordList, wordFreq2)
    resultSet = set(result)
    return resultSet

# 
def Analysis():
    airport_array = airport_dict
    result = {}
    probability = {}
    bil = 0
    print("Analysing political status...\r")
    printProgressBar(0, len(items), prefix='Progress:',
                     suffix='Complete', length=50)

    for i in airport_array:
        printProgressBar(bil + 1, len(items), prefix='Progress:',
                         suffix='Complete', length=50)
        airport_url = airport_array[i]["link"]
        html = urllib.request.urlopen(airport_url).read()

        str = text_from_html(html)
        str_split = str.split(" ")
        str_split = removeNone(str_split)

        stopResult = stopWord_freq(str_split)
        # plotStopwords(stopResult)

        str_split = removeStopWord(str_split)
        wordAll.append(str_split)
        freqAll.append(wordFreq(str_split))

        positive, negative, neutral = calculatePercentage(str_split)

        result["name"] = airport_array[i]["name"]
        result["wordFreq"] = wordFreq_set(str_split, wordFreq(str_split))
        result["positive"] = positive
        result["negative"] = negative
        result["neutral"] = neutral
        result["stopWord"] = stopResult

        probability[bil] = copy.deepcopy(result)

        bil += 1

    try:
        with open('assets/political_probability.txt', 'w', encoding='utf-8')as outfile:
            json.dump(probability, outfile, ensure_ascii=False)
    except Exception as e:
        print(e)

    return probability


def compare(p, n):
    if p > n:
        print("The country have positive political situation.")
    elif p == n:
        print("The country has an average political situation.")
    else:
        print("The country have negative political situation.")


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


def plotNegVPos():
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


def plotStopwords(stopResult):
    #print("Error here")
    x, y = zip(*stopResult)
    data = [go.Histogram(
        histfunc="sum",
        y=y,
        x=x
    ), ]
    py.plot(data, filename='stopwordFrequency')


def plotAllWords():

    x0 = wordAll[0]
    x1 = wordAll[1]
    x2 = wordAll[2]
    x3 = wordAll[3]
    x4 = wordAll[4]
    x5 = wordAll[5]
    x6 = wordAll[6]
    x7 = wordAll[7]
    x8 = wordAll[8]
    x9 = wordAll[9]
    x10 = wordAll[10]
    x11 = wordAll[11]
    x12 = wordAll[12]
    x13 = wordAll[13]
    x14 = wordAll[14]

    y0 = freqAll[0]
    y1 = freqAll[1]
    y2 = freqAll[2]
    y3 = freqAll[3]
    y4 = freqAll[4]
    y5 = freqAll[5]
    y6 = freqAll[6]
    y7 = freqAll[7]
    y8 = freqAll[8]
    y9 = freqAll[9]
    y10 = freqAll[10]
    y11 = freqAll[11]
    y12 = freqAll[12]
    y13 = freqAll[13]
    y14 = freqAll[14]

    trace0 = go.Histogram(
        x=x0,
        y=y0,
        name="Kuala Lumpur",
    )
    trace1 = go.Histogram(
        x=x1,
        y=y1,
        name="Singapore",
    )
    trace2 = go.Histogram(
        x=x2,
        y=y2,
        name="Abu Dhabi",
    )
    trace3 = go.Histogram(
        x=x3,
        y=y3,
        name="Mumbai",
    )
    trace4 = go.Histogram(
        x=x4,
        y=y4,
        name="Moscow",
    )
    trace5 = go.Histogram(
        x=x5,
        y=y5,
        name="Tokyo",
    )
    trace6 = go.Histogram(
        x=x6,
        y=y6,
        name="Beijing",
    )
    trace7 = go.Histogram(
        x=x7,
        y=y7,
        name="Shanghai",
    )
    trace8 = go.Histogram(
        x=x8,
        y=y8,
        name="Seoul",
    )
    trace9 = go.Histogram(
        x=x9,
        y=y9,
        name="Jakarta",
    )
    trace10 = go.Histogram(
        x=x10,
        y=y10,
        name="London",
    )
    trace11 = go.Histogram(
        x=x11,
        y=y11,
        name="Paris",
    )
    trace12 = go.Histogram(
        x=x12,
        y=y12,
        name="Sweeden",
    )
    trace13 = go.Histogram(
        x=x13,
        y=y13,
        name="Zimbabwe",
    )
    trace14 = go.Histogram(
        x=x14,
        y=y14,
        name="Brazil",
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
    fig.append_trace(trace13, 5, 2)
    fig.append_trace(trace14, 5, 3)

    py.plot(fig, filename='wordFrequency')
