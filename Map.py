import requests, json, io, copy, gmplot, webbrowser, math, os
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

airports = ["Kuala Lumpur International Airport", "Changi Airport Singapore", "Abu Dhabi International Airport",  "Sheremetyevo International Airport", "Haneda Airport", "Beijing Capital International Airport", "Shanghai Pudong International Airport", "Incheon International Airport", "Soekarno-Hatta International Airport", "Heathrow Airport", "Stockholm-Arlanda", "Victoria Falls Airport", "Sao Paulo International Airport"]
color = ["red", "blue", "yellow", "green", "black", "orange", "purple", "cornflowerblue", "aqua", "white"]
newspapers = ["https://www.thestar.com.my/",
"https://www.straitstimes.com/politics",
"https://www.khaleejtimes.com/news/government",
"https://www.themoscowtimes.com/news",
"https://www.japantimes.co.jp/news_category/politics-diplomacy/",
"http://www.chinadaily.com.cn/china/Beijing-News-Update.htm",
"https://www.cnbc.com/shanghai/",
"http://english.chosun.com/",
"https://jakartaglobe.id/",
"https://www.standard.co.uk/news/politics",
"https://www.thelocal.se/tag/politics",
"https://www.newsday.co.zw/",
"https://riotimesonline.com/brazil-news/category/rio-politics/local-politics-rio-politics/"]
map_items = list(range(0, 13))
latitude_all = []
longitude_all = []
airport_dict = {}
airport_array={}

def printProgressBarMap (iteration, total, prefix = '', decimals = 1, length = 100, fill = '█'):

    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%%' % (prefix, bar, percent), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()

#create airport_dict (airport_dict.txt)(Details of airport: Name, Address, Latitude, Longitude)
#create airport_array (airport_distance.txt)(Details of distance difference between airports)
def getAirports():
    print("Retrieving airports from database...")
    airport_dict2 = {}
    check = 0
    printProgressBarMap(0, len(map_items), prefix = 'Progress:', length = 50)
    
    for airport in airports:
        try:
            geolocator = Nominatim(user_agent="BestFlight")
            locate_place = geolocator.geocode(airport)
            # print(check,". ",airport, ":",(locate_place.latitude, locate_place.longitude))
            printProgressBarMap(check + 1, len(map_items), prefix = 'Map:', length = 50)
            # print("Map:",check)
            latitude_all.append(locate_place.latitude)
            longitude_all.append(locate_place.longitude)

            airport_dict2["name"] = airport
            airport_dict2["address"] = locate_place.address
            airport_dict2["latitude"]= locate_place.latitude
            airport_dict2["longitude"]= locate_place.longitude
            airport_dict2["link"]= newspapers[check]

            airport_dict[check] = copy.deepcopy(airport_dict2)
            # print("Done part: ", airport)
            check+=1
        except Exception as e:
            print(e)
            getAirports()
            exit()

    airport_array = createList(airport_dict)
    with open('assets/airport_dict.txt', 'w', encoding='utf-8') as outfile:  
        json.dump(airport_dict, outfile, ensure_ascii=False)

    return airport_array

#get difference between two coordinates
def calCoordinates(place1, place2):
    return geodesic(place1, place2).kilometers

def createList(airports_dict):
    airport_array = {}
    array2 = {}

    for x in range(len(airports_dict)):
        array2.clear()
        for y in range(len(airports_dict)): #complexity = n^2
            if(airports_dict[x]["name"]==airports_dict[y]["name"]):
                continue

            key = airports_dict[x]["name"]

            place1 = (airports_dict[x]["latitude"],airports_dict[x]["longitude"])
            place2 = (airports_dict[y]["latitude"],airports_dict[y]["longitude"])
         
            array2[airports_dict[y]["name"]] = calCoordinates(place1, place2)
            airport_array[key] = copy.deepcopy(array2)

    with open('assets/airport_distance.txt', 'w', encoding='utf-8') as outfile:  
        json.dump(airport_array, outfile, ensure_ascii=False)
    return airport_array


def getAirportArr():
    with open('assets/airport_distance.txt','r',encoding="utf8") as f:
        airport_array = json.loads(f.read())
    return airport_array

#Dijikstra Algo 
def addCoordinates(path, latitude, longitude, count):
    temp_latitude = []
    temp_longitude = []
    for y in range(len(path)):
        for z in range(len(airport_dict)): #complexity = n^2
            if(path[y] == airport_dict[z]["name"]):
                temp_latitude.append(airport_dict[z]["latitude"])
                temp_longitude.append(airport_dict[z]["longitude"])
    latitude[count] = copy.deepcopy(temp_latitude)
    longitude[count] = copy.deepcopy(temp_longitude)
    count+=1

def dijkstra(graph, start, goal):
    del graph[start][goal]
    del graph[goal][start]

    shortest_paths ={}
    shortest_paths_str ={}
    distance = {}
    latitude = {}
    longitude = {}

    shortest_distance = {}
    predecessor = {}
    unseenNodes = copy.deepcopy(graph)
    infinity = 9999999
    count = 0
    path = []

    for x in range(10):
        for node in unseenNodes:
            shortest_distance[node] = infinity
        shortest_distance[start] = 0

        while unseenNodes:
            minNode = None
            for node in unseenNodes:
                if minNode is None:
                    minNode = node
                elif shortest_distance[node] < shortest_distance[minNode]:
                    minNode = node

            for childNode, weight in graph[minNode].items():
                if weight + shortest_distance[minNode] < shortest_distance[childNode]:
                    shortest_distance[childNode] = weight + shortest_distance[minNode]
                    predecessor[childNode] = minNode
            unseenNodes.pop(minNode)

        currentNode = goal

        while currentNode != start:
            try:
                path.insert(0, currentNode)
                currentNode = predecessor[currentNode]
            except KeyError:
                print("Path not reachable")
                break
        path.insert(0, start)

        if shortest_distance[goal] != infinity:
            shortest_paths_str[x] = str(path)
            shortest_paths[x] = copy.deepcopy(path)
            distance[x] = str(shortest_distance[goal])
            
            del graph[start][path[1]]
            unseenNodes = copy.deepcopy(graph)
            addCoordinates(path, latitude, longitude, count)
            count+=1
            path.clear()
    
    return shortest_paths_str, shortest_paths, distance, latitude, longitude

def getPossibleRoutes():
    return math.factorial(len(airports))

#Plot map
def plotMap(latitude, longitude):
    gmap = gmplot.GoogleMapPlotter(latitude[0][0], 
                                    longitude[0][0], 5) 
    
    # scatter method of map object  
    # scatter points on the google map 
    gmap.scatter(latitude_all, longitude_all, '# FF0000', 
                                size = 5, marker = False ) 
    gmap.apikey = "AIzaSyD3cSr8TLouz71dNLj-VBMnacep2ChcFLM"
    # Plot method Draw a line in 
    # between given coordinates 
    for x in range(len(latitude)):
        gmap.plot(latitude[x], longitude[x],  
            color[x], edge_width = 2.5) 

    gmap.draw( "templates/map.html" ) 

    # url = os.getcwd() + "\\templates\\map.html"
    # webbrowser.open(url, new=2)