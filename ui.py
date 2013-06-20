from flask import Flask, render_template, jsonify, json, Response


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/now_playing')
def now_playing():
    return jsonify(artist='Artista', track='Tema')


@app.route('/get_tracks')
def get_tracks():
    return Response(json.dumps([{'artist': 'Artist %d' % i, 'track': 'Track %d' % i} for i in range(15)]), mimetype='application/json')


if __name__ == '__main__':
    app.run('0.0.0.0')
