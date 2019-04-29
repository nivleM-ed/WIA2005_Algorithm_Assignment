import gmplot 
import webbrowser
from airport_map import latitude, longitude
  
latitude_list = [ 30.3358376, 30.307977, 30.3216419 ] 
longitude_list = [ 77.8701919, 78.048457, 78.0413095 ] 
  
gmap = gmplot.GoogleMapPlotter(latitude[0], 
                                longitude[0], 13) 
  
# scatter method of map object  
# scatter points on the google map 
gmap.scatter( latitude, longitude, '# FF0000', 
                              size = 10, marker = False ) 
gmap.apikey = "AIzaSyD3cSr8TLouz71dNLj-VBMnacep2ChcFLM"
# Plot method Draw a line in 
# between given coordinates 
gmap.plot(latitude, longitude,  
           'cornflowerblue', edge_width = 2.5) 

gmap.draw( "assets/map1.html" ) 

url = 'C:/Users/Melvin/Documents/GithubRepo/WIA2005_Algorithm_Assignment/assets/map1.html'
webbrowser.open(url, new=2)