from flask import Flask, jsonify, render_template, request
import json
from lod import Control

app = Flask(__name__)
control = Control()

@app.route('/_saveData', methods = ['POST'])
def saveData():
    fout = open("saved_data.txt", "wt")
    fout.write(json.dumps(request.json))
    fout.close()
    control.set_db(request.json)
    print("Data Saved")
    return jsonify("AJAX request success")

@app.route('/_loadData', methods = ['POST'])
def loadData():
    fin = open("saved_data.txt", "rt")
    send_data = json.loads(fin.read())
    fin.close()
    control.set_db(send_data)
    return jsonify(send_data)

@app.route('/_run', methods = ['POST'])
def run():
    move = request.json["move"]
    print("move :", move)
    if move == 0:
        move = control.get_start()
    else:
        move = control.next()
    ret = {"move_data": move}
    print("return : ", ret)
    return jsonify(ret)

@app.route('/')
def hello_world():
    print("render index.html")
    return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run(threaded=True)
