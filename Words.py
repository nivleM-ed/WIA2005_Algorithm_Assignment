import urllib.request
import nltk
from bs4 import BeautifulSoup
from bs4.element import Comment
from nltk.corpus import stopwords


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
    arr = arr.split(" ")

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
           # print(arr[x])
            x += 1
        return arr



html = urllib.request.urlopen('https://www.straitstimes.com/politics').read()
str_split = removeNone(text_from_html(html))

# print("[STOP WORDS NOT REMOVED]", str_split, "[STOP WORDS NOT REMOVED]")
# print("[STOP WORDS REMOVED]", removeStopWord(str_split), "[STOP WORDS REMOVED]")

wordfreq = []

text_file = open("assets/negative.txt", "r")
negative_array = text_file.read().split(',')
text_file2 = open("assets/positive.txt", "r")
positive_array = text_file2.read().split(',')
text_file.close()
text_file2.close()

for w in str_split:
    wordfreq.append(str_split.count(w))
result = zip(str_split, wordfreq)
resultSet = set(result)
print(resultSet)

# def calculatePercentage(str_split):
totalWord = len(str_split)
positiveWord = 0
negativeWord = 0
neutralWord = 0
try:
   # print(cleanStrip(lines))
    print(cleanStrip(negative_array), "\n")
    print(cleanStrip(positive_array))
    print(len(str_split))

    for word in str_split:
        if word.lower() in positive_array:
            positiveWord += 1
        elif word.lower() in negative_array:
            negativeWord += 1
        else:
            neutralWord += 1

    print("Positive: ", (round((positiveWord/totalWord)*100)))
    print("Negative: ", (round((negativeWord/totalWord)*100)))
    print("Neural: ", (round((neutralWord/totalWord)*100)))
except:
    print(str(Exception))
