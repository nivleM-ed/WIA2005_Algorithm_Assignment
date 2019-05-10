import urllib.request, nltk
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

def cleanArr(arr):
    arr = arr.split(" ")

    while("" in arr):
        arr.remove("")
    return arr

def removeStopWord(arr):
    stop_words = stopwords.words('english')
    arr = [x.lower() for x in arr]
    return [word for word in arr if word not in stop_words]

html = urllib.request.urlopen('https://www.straitstimes.com/politics').read()
str_split = cleanArr(text_from_html(html))

print("[STOP WORDS NOT REMOVED]",str_split,"[STOP WORDS NOT REMOVED]")
print("[STOP WORDS REMOVED]",removeStopWord(str_split),"[STOP WORDS REMOVED]")
