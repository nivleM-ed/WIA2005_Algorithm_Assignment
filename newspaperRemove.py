from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request, copy

input = "stopword.txt"
text = open(input,"r")
text_string = text.read().lower()
word = text_string.split("\n")

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

class RollingHash:
    def __init__(self, text, sizeWord):
        self.text = text
        self.hash = 0
        self.sizeWord = sizeWord

        for i in range(0, sizeWord):
            #ord maps the character to a number
            #subtract out the ASCII value of "a" to start the indexing at zero
            self.hash += (ord(self.text[i]) - ord("a")+1)*(26**(sizeWord - i -1))

        #start index of current window
        self.window_start = 0
        #end of index window
        self.window_end = sizeWord

    def move_window(self):
        if self.window_end <= len(self.text) - 1:
            #remove left letter from hash value
            self.hash -= (ord(self.text[self.window_start]) - ord("a")+1)*26**(self.sizeWord-1)
            self.hash *= 26
            self.hash += ord(self.text[self.window_end])- ord("a")+1
            self.window_start += 1
            self.window_end += 1

    def window_text(self):
        return self.text[self.window_start:self.window_end]

    def delete(text, word):
        i = 0
        while i < len(text):
            if (i == word):
                if text[word] != []:
                    del text[word]
                    print('Key {} deleted'.format(key))
                    break
                else:
                    print('Key {} not deleted'.format(key))
                    break
            else:
                i += 1

def rabin_karp(word, text):
    i = 0
    txt_array = copy.deepcopy(text)
    while(i < len(word)):

        if len(word[i]) > len(text):
            return None

        word_hash = RollingHash(word[i], len(word[i]))
        j = 0
        length = len(text)
        print(length)
        while (j < length):
            # print(txt_array)
            # print(word[i])
            rolling_hash = RollingHash(text[j], len(word[i]))
            
            if rolling_hash.hash == word_hash.hash:
                if rolling_hash.window_text() == word[i]:
                    # try:
                    txt_array.remove(word[i])
                    length = length - 1
                    continue
                    # except ValueError:
                    #     continue
            j+=1
            print("J:",j," I:",i,"Length:",length)
            rolling_hash.move_window()
        i+=1

    return txt_array

html = urllib.request.urlopen('https://www.straitstimes.com/politics').read()
str = text_from_html(html)
# str_replace = str.replace(" ",",")
str_split = str.split(" ")

# for x in str_split:
   # if x.isspace():
   #     str_split.remove()

while("" in str_split):
    str_split.remove("")
print(str_split, "\n")


print(word)
txt = str_split
i = 0
print (rabin_karp(word, txt))


