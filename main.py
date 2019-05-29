import copy
from time import sleep

from Map import airports, dijkstra, getAirports, plotMap, getPossibleRoutes
from Words import Analysis, plotAllWords, plotNegVPos, plotStopwords

def compare(p, n):
    if p > n:
        print("The country have positive political situation.")
    elif p == n:
        print("The country has an average political situation.")
    else:
        print("The country have negative political situation.")

def getBestFlight(shortest_path, distance, probability):
    best_flight = {}
    best_flight2 = {}
    last = distance[len(distance)-1]
    for x in range(len(shortest_path)):
        distance_score = ((float(last)-float(distance[x]))/float(last))*70
        y = 0
        
        while shortest_path[x][1] != probability[str(y)]['name']:
            y+=1
        
        if probability[str(y)]['positive'] > probability[str(y)]['negative'] or probability[str(y)]['positive'] == probability[str(y)]['negative']:
            positive_score = probability[str(y)]['positive'] - probability[str(y)]['negative']
        else:
            positive_score = -(2*probability[str(y)]['negative'])
        
        total_score = distance_score + positive_score

        best_flight2["path"] = shortest_path[x]
        best_flight2["distance"] = distance[x]
        best_flight2["positive"] = probability[str(y)]['positive']
        best_flight2["negative"] = probability[str(y)]['negative']
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

def run():
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

    print("Showing the 10 best routes of",getPossibleRoutes(),"possible routes\n")
    shortest_paths_str, shortest_paths, distance, latitude, longitude = dijkstra(airport_array, airports[0], airports[int(goal)-1])

    # print(shortest_paths)
    # for x in range(len(shortest_paths_str)):
    #     print("Route ",x+1,": ",shortest_paths_str[x])
    #     print("Distance: ", distance[x]),"\n"

    best_flight = getBestFlight(shortest_paths, distance, probability)

    for x in range(len(best_flight)):
        print("Route",x+1,":",best_flight[x]["path"])
        print("Distance:", best_flight[x]["distance"],"\tPositive percentage: ", best_flight[x]["positive"],"\tNegative percentage: ", best_flight[x]["negative"])
        compare(best_flight[x]["positive"],best_flight[x]["negative"])
        print("\n")

    yesChoice = ['yes','y']
    noChoice = ['no', 'n']

    user_in = input("Would you like to view the routes before the best route algorithm:(y/n): ")
    if user_in in yesChoice:
        print("Getting routes...")
        for x in range(len(shortest_paths)):
            print(x,".",shortest_paths[x])

    user_in = input("\nWould you like to view the map(y/n): ")
    if user_in in yesChoice:
        print("Plotting map with best routes...")
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
