import json, nltk, urllib.request, copy
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from bs4.element import Comment


# API Used:
# 1. Google Maps => pip install -U googlemaps
# 2. Geopy => pip install geopy
# 3. GMPlot => pip install gmplot

# Countries:
# 1. Kuala Lumpur, Malaysia => Kuala Lumpur International Airport
# 2. Singapore, Singapore => Changi Airport Singapore
# 3. Abu Dhabi, UAE => Abu Dhabi International Airport
# 4. Mumbai, India => Chhatrapati Shivaji International Airport
# 5. Moscow, Russia => Sheremetyevo International Airport
# 6. Tokyo, Japan => Haneda Airport
# 7. Beijing, China => Beijing Capital International Airport
# 8. Shanghai, China => Shanghai Pudong International Airport
# 9. Seoul, South Korea => Incheon International Airport
# 10. Jakarta, Indonesia => Soekarno-Hatta International Airport
# 11. London, United Kingdom => Heathrow Airport
# 12. Paris, France => Paris Charles de Gaulle
# 13. Sweden => Stockholm-Arlanda Airport
# 14. Zimbabwe => Victoria Falls Airport
# 15. Brazil => Sao Paulo International Airport

# airports = ["Kuala Lumpur International Airport", "Changi Airport Singapore", " Abu Dhabi International Airport", "Chhatrapati Shivaji International Airport", "Sheremetyevo International Airport", "Haneda Airport", "Beijing Capital International Airport",
#             "Shanghai Pudong International Airport", "Incheon International Airport", "Soekarno-Hatta International Airport", "Heathrow Airport", "Paris Charles de Gaulle", "Stockholm-Arlanda", "Victoria Falls Airport", "Sao Paulo International Airport"]

# for airport in airports:
#     try:
#         geolocator = Nominatim(user_agent="BestFlight")
#         locate_place = geolocator.geocode(airport)
#         print(locate_place.address, ": ")
#         print((locate_place.latitude, locate_place.longitude), "\n")
#     except:
#         print("Can't find place")

# Get name of place of coordinates
# locate_place = geolocator.reverse("3.1201011,101.6522106")
# print(locate_place.address)

# Finding distance between 2 places
# place_1 = (latitude,longitude)
# place_2 = (latitude,longitude)
# print(geodesic(place_1, place_2).kilometers)
     
# def tag_visible(element):
#     if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
#         return False
#     if isinstance(element, Comment):
#         return False
#     return True

# def text_from_html(body):
#     soup = BeautifulSoup(body, 'html.parser')
#     texts = soup.findAll(text=True)
#     visible_texts = filter(tag_visible, texts)
#     return u" ".join(t.strip() for t in visible_texts)

# html = urllib.request.urlopen('https://www.straitstimes.com/politics').read()
# str1 = text_from_html(html)
# # str_replace = str.replace(" ",",")
# str_split = str1.split(" ")

# length = len(str_split)
# print(length,"LENGTH")
# x = 0
    
# while x < length:
#     if str_split[x] == '':
#         str_split.remove(str_split[x]);
#         length = length - 1
#         continue
#     x+=1

# print(str_split)

# input = "stopword.txt"
# text = open(input,"r")
# text_string = text.read().lower()
# word = text_string.split("\n")

# def tag_visible(element):
#     if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
#         return False
#     if isinstance(element, Comment):
#         return False
#     return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)

# d = 256

# stop_words = stopwords.words('english') 

# html = urllib.request.urlopen('https://www.straitstimes.com/politics').read()
# str = text_from_html(html)
# str_split = str.split(" ")

# while("" in str_split):
#     str_split.remove("")
# # print(str_split, "\n")

# print(str_split)

# tokenized_words = ['i', 'am', 'going', 'to', 'go', 'to', 'the', 'store', 'and', 'park']

# test = [word for word in str_split if word not in stop_words]
# print("\n\n",test)
# print(str_split)


#the function
def cleanStrip(arr):
    x=0
    while x<len(arr):
        arr[x] = arr[x].strip()
        print(arr[x])
        x+=1
    return arr

#opening file
text_file = open("negative.txt", "r")
lines = text_file.read().split(',')
print(lines)
print(len(lines))
text_file.close()

print(cleanStrip(lines))