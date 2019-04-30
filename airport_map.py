import requests
import json
import io
import copy
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

def calCoordinates(place1, place2):
    return geodesic(place1, place2).kilometers

def createList(airports_dict, latitude, longitude):
    array = {}
    array2 = {}

    for x in range(len(airports_dict)):
        array2.clear()
        for y in range(len(airports_dict)):
            if(airports_dict[x]["name"]==airports_dict[y]["name"]):
                continue

            key = airports_dict[x]["name"]

            place1 = (airports_dict[x]["latitude"],airports_dict[x]["longitude"])
            place2 = (airports_dict[y]["latitude"],airports_dict[y]["longitude"])
            
            # print(place1)
            # print(place2,"\n")
            
            array2[airports_dict[y]["name"]] = calCoordinates(place1, place2)
            array[key] = copy.deepcopy(array2)

    print(array)
    with open('data.txt', 'w', encoding='utf-8') as outfile:  
        json.dump(array, outfile, ensure_ascii=False)

api_key = "AIzaSyD3cSr8TLouz71dNLj-VBMnacep2ChcFLM"

airports = ["Kuala Lumpur International Airport", "Changi Airport Singapore", "Abu Dhabi International Airport", "Chhatrapati Shivaji International Airport", "Sheremetyevo International Airport", "Haneda Airport", "Beijing Capital International Airport", "Shanghai Pudong International Airport", "Incheon International Airport", "Soekarno-Hatta International Airport", "Heathrow Airport", "Paris Charles de Gaulle", "Stockholm-Arlanda", "Victoria Falls Airport", "Sao Paulo International Airport"]
latitude = []
longitude = []
airport_names = []
airport_dict = {}
airport_dict2 = {}
x = 0

for airport in airports:
    try:
        geolocator = Nominatim(user_agent="BestFlight")
        locate_place = geolocator.geocode(airport)
        print(locate_place.address, ": ")
        print((locate_place.latitude, locate_place.longitude), "\n")
        
        airport_names.append(locate_place.address)
        latitude.append(locate_place.latitude)
        longitude.append(locate_place.longitude)
        
        airport_dict2["name"] = airport
        airport_dict2["address"] = locate_place.address
        airport_dict2["latitude"]= locate_place.latitude
        airport_dict2["longitude"]= locate_place.longitude

        airport_dict[x] = copy.deepcopy(airport_dict2)

        x+=1
    except:
        print("Can't find place")

# print(airport_dict2)
# print(airport_dict)
with open('airport_dict.txt', 'w', encoding='utf-8') as outfile:  
    json.dump(airport_dict, outfile, ensure_ascii=False)

createList(airport_dict, latitude, longitude)

