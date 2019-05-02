import gmplot 
import webbrowser
from airport_map import latitude_all, longitude_all

color = ["red", "blue", "yellow", "green", "black", "orange", "purple", "cornflowerblue", "aqua", "white"]
   
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

    gmap.draw( "assets/map1.html" ) 

    url = 'C:/Users/Melvin/Documents/GithubRepo/WIA2005_Algorithm_Assignment/assets/map1.html'
    webbrowser.open(url, new=2)