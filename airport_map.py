import requests
import json
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

api_key = "AIzaSyD3cSr8TLouz71dNLj-VBMnacep2ChcFLM"

airports = ["Kuala Lumpur International Airport", "Changi Airport Singapore", " Abu Dhabi International Airport", "Chhatrapati Shivaji International Airport", "Sheremetyevo International Airport", "Haneda Airport", "Beijing Capital International Airport", "Shanghai Pudong International Airport", "Incheon International Airport", "Soekarno-Hatta International Airport"]
latitude = [] * 10;
longitude = [] * 10;

for airport in airports:
    try:
        geolocator = Nominatim(user_agent="BestFlight")
        locate_place = geolocator.geocode(airport)
        print(locate_place.address, ": ")
        print((locate_place.latitude, locate_place.longitude), "\n")
        latitude.append(locate_place.latitude)
        longitude.append(locate_place.longitude)
    except:
        print("Can't find place")

    # get individual maps
    # url = "http://maps.googleapis.com/maps/api/staticmap?center="+str(locate_place.latitude)+","+str(locate_place.longitude)+"&zoom=1&size=400x350&sensor=false&markers="+str(locate_place.latitude)+","+str(locate_place.longitude)+"&scale=2&key="+api_key
    
    # r = requests.get(url) 
    # f = open('assets/map_'+airport+'.png', 'wb')
    # f.write(r.content)
    # f.close() 
