import time, _thread

from flask import Flask, Response, render_template, request, session, url_for

import main
import Map
import Words

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/airport', methods=['GET','POST'])
def airport():
    return render_template('index.html', airports=Map.airports)

@app.route('/map', methods=['GET','POST'])
def map():
    return render_template('map.html')

@app.route('/results', methods=['GET','POST'])
def results():
    if request.method == 'POST':
        airport_array = Map.getAirportArr()
        probability = Words.getProb()

        user_airport = request.form.get('airports')

        shortest_paths_str, shortest_paths, distance, latitude, longitude = Map.dijkstra(airport_array, Map.airports[0], Map.airports[int(user_airport)])
        Map.plotMap(latitude, longitude)
        
        best_flight = main.getBestFlight(shortest_paths, distance, probability)
    return render_template('results.html', airports = Map.airports, user_choice = str(user_airport), best_route = best_flight, shortest_paths=shortest_paths, distance=distance)

@app.route('/')
def index():
    return render_template('progress.html')

@app.route('/progress', methods=['GET','POST'])
def progress():
    try:
        _thread.start_new_thread( Words.Analysis, () )
        _thread.start_new_thread( Map.getAirports, () )
    except Exception as ex:
        print(ex)
    def generate():
        x=2
        while x<= 100:
            yield "data:" + str(x) + "\n\n"
            x+=int(100/13)
            time.sleep(1)

    return Response(generate(), mimetype= 'text/event-stream')

@app.route('/stopword', methods=['GET','POST'])
def stopword():
    stopWordList = Words.getStopwordsAll()
    Words.plotStopwords(stopWordList)
    return '', 204

@app.route('/posneg', methods=['GET','POST'])
def posneg():
    pos_freq = Words.getPosFreq()
    neg_freq = Words.getNegFreq()
    Words.plotNegVPos(pos_freq, neg_freq)
    return '', 204

@app.route('/wordall', methods=['GET','POST'])
def wordall():
    wordAll = Words.getwordAll()
    freqAll = Words.getfreqAll()
    Words.plotAllWords(wordAll, freqAll)
    return '', 204