import gmplot 
import webbrowser
from airport_map import latitude, longitude, airport_names
   
gmap = gmplot.GoogleMapPlotter(latitude[0], 
                                longitude[0], 5) 
  
# scatter method of map object  
# scatter points on the google map 
gmap.scatter( latitude, longitude, '# FF0000', 
                              size = 5, marker = False ) 
gmap.apikey = "AIzaSyD3cSr8TLouz71dNLj-VBMnacep2ChcFLM"
# Plot method Draw a line in 
# between given coordinates 
gmap.plot(latitude, longitude,  
           'cornflowerblue', edge_width = 2.5) 

gmap.draw( "assets/map1.html" ) 

url = 'C:/Users/Melvin/Documents/GithubRepo/WIA2005_Algorithm_Assignment/assets/map1.html'
webbrowser.open(url, new=2)