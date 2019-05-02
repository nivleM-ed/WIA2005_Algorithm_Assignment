from airport_map import airport_array, airport_dict
import copy

def addCoordinates(path, latitude, longitude, count):
    temp_latitude = []
    temp_longitude = []
    for y in range(len(path)):
        for z in range(len(airport_dict)):
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
            shortest_paths[x] = str(path)
            distance[x] = str(shortest_distance[goal])
            
            print("Distance is " + str(shortest_distance[goal]))
            print("And the path is " + str(path))
            
            del graph[start][path[1]]
            unseenNodes = copy.deepcopy(graph)
            addCoordinates(path, latitude, longitude, count)
            count+=1
            path.clear()
    
    return shortest_paths, distance, latitude, longitude
