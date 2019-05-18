import copy
from time import sleep

from Map import airports, dijkstra, getAirports, plotMap
from Words import Analysis, plotAllWords, plotNegVPos, plotStopwords


def getBestFlight(shortest_path, distance, probability):
    best_flight = {}
    best_flight2 = {}
    last = distance[len(distance)-1]
    for x in range(len(shortest_path)):
        distance_score = ((float(last)-float(distance[x]))/float(last))*70
        y = 0
        
        while shortest_path[x][1] != probability[y]['name']:
            y+=1
        
        positive_score = probability[y]['positive'] - probability[y]['negative']
        total_score = distance_score + positive_score

        best_flight2["path"] = shortest_path[x]
        best_flight2["distance"] = distance[x]
        best_flight2["positive"] = probability[y]['positive']
        best_flight2["negative"] = probability[y]['negative']
        best_flight2["score"] = int(total_score)
        best_flight[x] = copy.deepcopy(best_flight2)

    return arrangeBest(best_flight)

def arrangeBest(best_flight):
    n = len(best_flight)
    gap = n//2
    while gap > 0: 
        for i in range(gap,n): 

            # add a[i] to the elements that have been gap sorted 
            # save a[i] in temp and make a hole at position i 
            temp = best_flight[i]

            # shift earlier gap-sorted elements up until the correct 
            # location for a[i] is found 
            j = i 
            while  j >= gap and best_flight[j-gap]["score"] < temp["score"]: 
                best_flight[j] = best_flight[j-gap] 
                j -= gap 

            # put temp (the original a[i]) in its correct location 
            best_flight[j] = temp 
        gap //= 2
    return best_flight

shortest_paths = {}
shortest_paths_str = {}
distance = {}
latitude = {}
longitude = {}

print("Retrieving airports from database...")
airport_array = getAirports()
probability = Analysis()

for x in range(len(airports)):
    print(x+1,". ",airports[x])

print("\nEnter airport according to number:")
print("Origin: ", airports[0])
goal = input("Goal: ")
print("You chose", airports[int(goal)-1])

shortest_paths_str, shortest_paths, distance, latitude, longitude = dijkstra(airport_array, airports[0], airports[int(goal)-1])

# print(shortest_paths)
# for x in range(len(shortest_paths_str)):
#     print("Route ",x+1,": ",shortest_paths_str[x])
#     print("Distance: ", distance[x]),"\n"

best_flight = getBestFlight(shortest_paths, distance, probability)

for x in range(len(best_flight)):
    print("Route",x+1,":",best_flight[x]["path"])
    print("Distance:", best_flight[x]["distance"],"\tPositive percentage: ", best_flight[x]["positive"],"\tNegative percentage: ", best_flight[x]["negative"])

yesChoice = ['yes','y']
noChoice = ['no', 'n']

user_in = input("\nWould you like to view the map(y/n): ")
if user_in in yesChoice:
    print("Plotting graph on plot.ly...")
    plotMap(latitude, longitude)

user_in = input("\nWould you like to view graph of negative and positive words:(y/n) ")
if user_in in yesChoice:
    print("Plotting graph on plot.ly...")
    plotNegVPos()

user_in = input("\nWould you like to view graph of all words:(y/n) ")
if user_in in yesChoice:
    print("Plotting graph on plot.ly...")
    plotAllWords()

user_in = input("\nWould you like to view graph of stopwords:(y/n) ")
if user_in in yesChoice:
    print("Plotting graph on plot.ly...")
    plotStopwords()
