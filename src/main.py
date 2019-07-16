from flask import Flask, render_template, request
import json

from parse_quaternion import parse_quaternion
from compute_stab import make_plot
import config

app = Flask(__name__)

def parse_group(G_str):
    return [
        parse_quaternion(q)
        for q in G_str.split('\n')
    ]


@app.route('/', methods=['GET'])
def index():
    G1, G2 = config.default_G1, config.default_G2

    plots = make_plot(parse_group(G1), parse_group(G2))
    return render_template('index.html', G1=G1, G2=G2, plots=plots)


@app.route('/get_data', methods=['POST'])
def get_data():
    G1 = request.form['G1']
    G2 = request.form['G2']
    return json.dumps(
        make_plot(
            parse_group(G1), 
            parse_group(G2)
        )
    )


if __name__ == '__main__':
      app.run(host=config.HOST, port=config.PORT)
