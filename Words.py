import urllib.request, nltk, copy, json, ssl, plotly
import plotly.plotly as py
import plotly.graph_objs as go
from bs4 import BeautifulSoup
from bs4.element import Comment
from nltk.corpus import stopwords
from Map import airport_dict
from threading import Thread
from Map import printProgressBar, items


positive_freq = []
negative_freq = []

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


def removeNone(arr):
    while("" in arr):
        arr.remove("")
    return arr


def removeStopWord(arr):
    stop_words = stopwords.words('english')
    arr = [x.lower() for x in arr]
    return [word for word in arr if word not in stop_words]


def cleanStrip(arr):
    x = 0
    while x < len(arr):
        arr[x] = arr[x].lower().strip()
        x += 1
    return arr


def calculatePercentage(str_split):
    totalWord = len(str_split)
    negative_array, positive_array = readNegPos()
    positiveWord = 0
    negativeWord = 0
    neutralWord = 0

    cleanStrip(negative_array)
    cleanStrip(positive_array)

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


def Analysis():
    airport_array = airport_dict
    result = {}
    probability = {}
    bil = 0
    print("Analysing political status...\r")
    printProgressBar(0, len(items), prefix = 'Progress:', suffix = 'Complete', length = 50)

    for i in airport_array:
        printProgressBar(bil + 1, len(items), prefix = 'Progress:', suffix = 'Complete', length = 50)
        airport_url = airport_array[i]["link"]
        html = urllib.request.urlopen(airport_url).read()

        str = text_from_html(html)
        str_split = str.split(" ")

        str_split = removeNone(str_split)
        str_split = removeStopWord(str_split)
        
        
        positive, negative, neutral = calculatePercentage(str_split)

        result["name"] = airport_array[i]["name"]
        result["wordFreq"] = wordFreq(str_split)
        result["positive"] = positive
        result["negative"] = negative
        result["neutral"] = neutral

        probability[bil] = copy.deepcopy(result)

        bil += 1

    try:
     with open('political_probability.txt', 'w', encoding='utf-8')as outfile:
        json.dump(probability, outfile, ensure_ascii=False)
    except Exception as e:
        print (e)

    return probability

def compare(p,n):
    if p>n or p==n:
        print("The country have positive political situation.")
    else:
        print("The country have negative political situation.")


def wordFreq(str_split):
    wordfreq = []
    for w in str_split:
        wordfreq.append(str_split.count(w))
    result = zip(str_split, wordfreq)
    resultSet = list(set(result))
    return resultSet


def readNegPos():
    text_file = open("assets/negative.txt", "r")
    negative_array = text_file.read().split(',')
    text_file2 = open("assets/positive.txt", "r")
    positive_array = text_file2.read().split(',')
    return negative_array, positive_array


def plotNegVPos():
    city = ["Kuala Lumpur", "Changi", "Abu Dhabi", "Mumbai", "Moscow", "Tokyo", "BeiJing", "Shanghai", "Seoul", "Jakarta", "London", "Paris", "Sweeden", "Zimbabwe", "Rio de Janeiro"]
    y0 = positive_freq
    y1 = negative_freq

    data = [
    go.Histogram(
        histfunc = "sum",
        y = y0,
        x = city,
        name = "positive words"
    ),
        go.Histogram(
            histfunc = "sum",
            y=y1,
            x=city,
            name = "negative words"
        )
    ]

    py.plot(data, filename='Positive vs Negative words')