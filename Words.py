import urllib.request,nltk, copy, json, ssl, plotly, os, sys
import plotly.plotly as py
import plotly.graph_objs as go
from plotly import tools
from bs4 import BeautifulSoup
from bs4.element import Comment
from nltk.corpus import stopwords
from threading import Thread
from Map import printProgressBar, items, airports, airport_dict

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
    printProgressBar(0, len(items), prefix='Progress:',
                     suffix='Complete', length=50)

    for i in airport_array:
        printProgressBar(bil + 1, len(items), prefix='Progress:',
                         suffix='Complete', length=50)
        airport_url = airport_array[i]["link"]
        opener = AppURLopener()
        response = opener.open(airport_url)
        # html = urllib.request.urlopen(airport_url).read()
        html = response.read()

        str = text_from_html(html)
        str_split = str.split(" ")
        str_split = removeNone(str_split)
        stopWord_freq(str_split,bil)

        str_split = removeStopWord(str_split)
        wordAll.append(str_split)
        freqAll.append(wordFreq(str_split))

        positive, negative, neutral = calculatePercentage(str_split)

        result["name"] = airport_array[i]["name"]
        result["wordFreq"] = wordFreq_set(str_split, wordFreq(str_split))
        result["positive"] = positive
        result["negative"] = negative
        result["neutral"] = neutral
        # result["stopWord"] = stopResult

        probability[bil] = copy.deepcopy(result)

        bil += 1

    try:
        with open('assets/political_probability.txt', 'w', encoding='utf-8')as outfile:
            json.dump(probability, outfile, ensure_ascii=False)
    except Exception as e:
        print(e)

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


def plotStopwords():
    # x, y = zip(*stopResult)
    # data = [go.Histogram(
    #     histfunc="sum",
    #     y=y,
    #     x=x
    # ), ]

    trace0 = go.Histogram(
        x=stopWordList[0]['wordList'],
        y=stopWordList[0]['wordFreq'],
        name=airports[0],
    )
    trace1 = go.Histogram(
        x=stopWordList[1]['wordList'],
        y=stopWordList[1]['wordFreq'],
        name=airports[1],
    )
    trace2 = go.Histogram(
        x=stopWordList[2]['wordList'],
        y=stopWordList[2]['wordFreq'],
        name=airports[2],
    )
    trace3 = go.Histogram(
        x=stopWordList[3]['wordList'],
        y=stopWordList[3]['wordFreq'],
        name=airports[3],
    )
    trace4 = go.Histogram(
        x=stopWordList[4]['wordList'],
        y=stopWordList[4]['wordFreq'],
        name=airports[4],
    )
    trace5 = go.Histogram(
        x=stopWordList[5]['wordList'],
        y=stopWordList[5]['wordFreq'],
        name=airports[5],
    )
    trace6 = go.Histogram(
        x=stopWordList[6]['wordList'],
        y=stopWordList[6]['wordFreq'],
        name=airports[6],
    )
    trace7 = go.Histogram(
        x=stopWordList[7]['wordList'],
        y=stopWordList[7]['wordFreq'],
        name=airports[7],
    )
    trace8 = go.Histogram(
        x=stopWordList[8]['wordList'],
        y=stopWordList[8]['wordFreq'],
        name=airports[8],
    )
    trace9 = go.Histogram(
        x=stopWordList[9]['wordList'],
        y=stopWordList[9]['wordFreq'],
        name=airports[9],
    )
    trace10 = go.Histogram(
        x=stopWordList[10]['wordList'],
        y=stopWordList[10]['wordFreq'],
        name=airports[10],
    )
    trace11 = go.Histogram(
        x=stopWordList[11]['wordList'],
        y=stopWordList[11]['wordFreq'],
        name=airports[11],
    )
    trace12 = go.Histogram(
        x=stopWordList[12]['wordList'],
        y=stopWordList[12]['wordFreq'],
        name=airports[12],
    )
    # trace13 = go.Histogram(
    #     x=stopWordList[13]['wordList'],
    #     y=stopWordList[13]['wordFreq'],
    #     name=airports[13],
    # )
    # trace14 = go.Histogram(
    #     x=stopWordList[14]['wordList'],
    #     y=stopWordList[14]['wordFreq'],
    #     name=airports[14],
    # )

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
    # fig.append_trace(trace13, 5, 2)
    # fig.append_trace(trace14, 5, 3)

    py.plot(fig, filename='stopwordFrequency')


def plotAllWords():
    trace0 = go.Histogram(
        x=wordAll[0],
        y=freqAll[0],
        name=airports[0],
    )
    trace1 = go.Histogram(
        x=freqAll[1],
        y=freqAll[1],
        name=airports[1],
    )
    trace2 = go.Histogram(
        x=freqAll[2],
        y=freqAll[2],
        name=airports[2],
    )
    trace3 = go.Histogram(
        x=freqAll[3],
        y=freqAll[3],
        name=airports[3],
    )
    trace4 = go.Histogram(
        x=freqAll[4],
        y=freqAll[4],
        name=airports[4],
    )
    trace5 = go.Histogram(
        x=freqAll[5],
        y=freqAll[5],
        name=airports[5],
    )
    trace6 = go.Histogram(
        x=freqAll[6],
        y=freqAll[6],
        name=airports[6],
    )
    trace7 = go.Histogram(
        x=freqAll[7],
        y=freqAll[7],
        name=airports[7],
    )
    trace8 = go.Histogram(
        x=freqAll[8],
        y=freqAll[8],
        name=airports[8],
    )
    trace9 = go.Histogram(
        x=freqAll[9],
        y=freqAll[9],
        name=airports[9],
    )
    trace10 = go.Histogram(
        x=freqAll[10],
        y=freqAll[10],
        name=airports[10],
    )
    trace11 = go.Histogram(
        x=freqAll[11],
        y=freqAll[11],
        name=airports[11],
    )
    trace12 = go.Histogram(
        x=freqAll[12],
        y=freqAll[12],
        name=airports[12],
    )
    # trace13 = go.Histogram(
    #     x=freqAll[13],
    #     y=freqAll[13],
    #     name=airports[13],
    # )
    # trace14 = go.Histogram(
    #     x=freqAll[14],
    #     y=freqAll[14],
    #     name=airports[14],
    # )

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
    # fig.append_trace(trace13, 5, 2)
    # fig.append_trace(trace14, 5, 3)

    py.plot(fig, filename='wordFrequency')
