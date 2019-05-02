import requests
import json
import io
import copy
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

def calCoordinates(place1, place2):
    return geodesic(place1, place2).kilometers

def createList(airports_dict):
    airport_array = {}
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
            airport_array[key] = copy.deepcopy(array2)

    

    with open('airport_distance.txt', 'w', encoding='utf-8') as outfile:  
        json.dump(airport_array, outfile, ensure_ascii=False)
    return airport_array

api_key = "AIzaSyD3cSr8TLouz71dNLj-VBMnacep2ChcFLM"

airports = ["Kuala Lumpur International Airport", "Changi Airport Singapore", "Abu Dhabi International Airport", "Chhatrapati Shivaji International Airport", "Sheremetyevo International Airport", "Haneda Airport", "Beijing Capital International Airport", "Shanghai Pudong International Airport", "Incheon International Airport", "Soekarno-Hatta International Airport", "Heathrow Airport", "Paris Charles de Gaulle", "Stockholm-Arlanda", "Victoria Falls Airport", "Sao Paulo International Airport"]

airport_dict = {}
airport_dict2 = {}
latitude_all = []
longitude_all = []
x = 0

for airport in airports:
    try:
        geolocator = Nominatim(user_agent="BestFlight")
        locate_place = geolocator.geocode(airport)
        print(airport, ": ")
        print((locate_place.latitude, locate_place.longitude), "\n")
        
        latitude_all.append(locate_place.latitude)
        longitude_all.append(locate_place.longitude)

        airport_dict2["name"] = airport
        airport_dict2["address"] = locate_place.address
        airport_dict2["latitude"]= locate_place.latitude
        airport_dict2["longitude"]= locate_place.longitude

        airport_dict[x] = copy.deepcopy(airport_dict2)

        x+=1
    except:
        print("Can't find place")

airport_array = createList(airport_dict)
with open('airport_dict.txt', 'w', encoding='utf-8') as outfile:  
    json.dump(airport_dict, outfile, ensure_ascii=False)
