import urllib.request
from bs4 import BeautifulSoup
from bs4.element import Comment
     
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

html = urllib.request.urlopen('https://www.straitstimes.com/politics').read()
str1 = text_from_html(html)
# str_replace = str.replace(" ",",")
str_split = str1.split(" ")

length = len(str_split)
print(length,"LENGTH")
x = 0

while x < length:
    if str_split[x] == '':
        str_split.remove(str_split[x]);
        length = length - 1
        continue
    x+=1

print(str_split)