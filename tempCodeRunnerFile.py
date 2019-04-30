rports = ["Kuala Lumpur International Airport", "Changi Airport Singapore", " Abu Dhabi International Airport", "Chhatrapati Shivaji International Airport", "Sheremetyevo International Airport", "Haneda Airport", "Beijing Capital International Airport",
            "Shanghai Pudong International Airport", "Incheon International Airport", "Soekarno-Hatta International Airport", "Heathrow Airport", "Paris Charles de Gaulle", "Stockholm-Arlanda", "Victoria Falls Airport", "Sao Paulo International Airport"]

for airport in airports:
    try:
        geolocator = Nominatim(user_agent="BestFlight")
        locate_place = geolocator.geocode(airport)
        print(locate_place.address, ": ")
        print((locate_place.latitude, locate_place.longitude), "\n")
    except:
        print("