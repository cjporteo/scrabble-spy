from flask import Flask, render_template, request
from scrabble import solve_tiles
from dictdata import DictData
import pickle

app = Flask(__name__)
dd = DictData('twl06')
loaded_dict = 'twl06'
twl06_twos = pickle.load(open('twl06twos.pickle', 'rb'))
sowpods_twos = pickle.load(open('sowpodstwos.pickle', 'rb'))

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        dictionary = request.form['dictionary']
        sowpods = dictionary == 'sowpods'
        global dd
        global loaded_dict
        if dictionary != loaded_dict:
            dd = DictData(dictionary)
            loaded_dict = dictionary
        if request.form['action'] == 'Search':
            tiles = request.form['tiles']
            pref = request.form['s-prefix']
            suff = request.form['s-suffix']
            substring = request.form['substring']
            includes = request.form['includes']
            results = solve_tiles(tiles, dd, pref, suff, substring, includes)
            if not tiles:
                return render_template('index.html', sowpods=sowpods)
            if results[0] == 'Invalid Input':
                return render_template('invalid.html', sowpods=sowpods)
            elif results[0] == 'No Valid Words':
                return render_template('nowords.html', sowpods=sowpods)
            return render_template('results.html', results=results, sowpods=sowpods)
        else:
            twos = sowpods_twos if sowpods else twl06_twos
            return render_template('twos.html', twos=twos, sowpods=sowpods)

    else:
        return render_template('index.html', sowpods=False)

if __name__ == '__main__':
    app.run(debug=True)