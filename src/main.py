from flask import Flask, render_template, request

from parse_quaternion import parse_quaternion
from compute_stab import make_plot


app = Flask(__name__)

def parse_group(G_str):
    return [
        parse_quaternion(q)
        for q in G_str.split('\n')
    ]

default_G1 = '''
-1
1
0.5 + 1.732*i
0.5 - 1.732*i
-0.5 + 1.732*i
0.5 - 1.732*i
'''

default_G2 = default_G1


@app.route('/', methods=['POST', 'GET'])
def index():
    G1, G2 = default_G1, default_G2

    if request.method == 'POST':
        G1 = request.form['G1']
        G2 = request.form['G2']

    plots = make_plot(parse_group(G1), parse_group(G2))
    return render_template('index.html', G1=G1, G2=G2, plots=plots)
