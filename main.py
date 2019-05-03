from Map import plotMap, getAirports, dijkstra, airports

shortest_paths = {}
distance = {}
latitude = {}
longitude = {}

print("Retrieving airports from database:(Enter airport according to number)")
airport_array = getAirports()

start = input("\nStart: ")
print("You chose ", airports[int(start)])
goal = input("Goal: ")
print("You chose", airports[int(goal)])

shortest_paths, distance, latitude, longitude = dijkstra(airport_array, airports[int(start)], airports[int(goal)])

print("\n")
for x in range(len(shortest_paths)):
    print("Route ",x+1,": ",shortest_paths[x])
    print("Distance: ", distance[x]),"\n"

plotMap(latitude, longitude)