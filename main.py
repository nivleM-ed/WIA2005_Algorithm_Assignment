from DijikstraAlgo import dijkstra
from airport_map import airport_array
from map_plot import plotMap

shortest_paths = {}
distance = {}
latitude = {}
longitude = {}
shortest_paths, distance, latitude, longitude = dijkstra(airport_array, "Kuala Lumpur International Airport", "Sao Paulo International Airport")

for x in range(len(shortest_paths)):
    print("Route ",x,": ",shortest_paths[x])
    print("Distance: ", distance[x]),"\n"

plotMap(latitude, longitude)