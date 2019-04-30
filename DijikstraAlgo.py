from airport_map import airport_array
import copy

def dijkstra(graph, start, goal):
    del graph[start][goal]
    del graph[goal][start]

    shortest_paths ={}
    distance = {}

    shortest_distance = {}
    predecessor = {}
    unseenNodes = copy.deepcopy(graph)
    infinity = 9999999
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
            path.clear()
    
    return shortest_paths, distance



shortest_paths = {}
distance = {}
shortest_paths, distance = dijkstra(airport_array, "Kuala Lumpur International Airport", "Changi Airport Singapore")

for x in range(len(shortest_paths)):
    print("Route ",x,": ",shortest_paths[x])
    print("Distance: ", distance[x])