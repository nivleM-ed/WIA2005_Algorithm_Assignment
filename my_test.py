from geopy.geocoders import Nominatim
from geopy.distance import geodesic


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

airports = ["Kuala Lumpur International Airport", "Changi Airport Singapore", " Abu Dhabi International Airport", "Chhatrapati Shivaji International Airport", "Sheremetyevo International Airport", "Haneda Airport", "Beijing Capital International Airport",
            "Shanghai Pudong International Airport", "Incheon International Airport", "Soekarno-Hatta International Airport", "Heathrow Airport", "Paris Charles de Gaulle", "Stockholm-Arlanda", "Victoria Falls Airport", "Sao Paulo International Airport"]

for airport in airports:
    try:
        geolocator = Nominatim(user_agent="BestFlight")
        locate_place = geolocator.geocode(airport)
        print(locate_place.address, ": ")
        print((locate_place.latitude, locate_place.longitude), "\n")
    except:
        print("Can't find place")

# Get name of place of coordinates
# locate_place = geolocator.reverse("3.1201011,101.6522106")
# print(locate_place.address)

# Finding distance between 2 places
# place_1 = (latitude,longitude)
# place_2 = (latitude,longitude)
# print(geodesic(place_1, place_2).kilometers)
