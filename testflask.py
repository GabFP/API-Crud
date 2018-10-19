from flask import Flask, jsonify, request
from BDconection import BD
import CRUD
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/read/", methods=['GET'])
def read():
    bd = BD('GABFPC', 'admin', 'admin', 'master')
    lido = CRUD.readevento(bd)

    return jsonify(lido)


if __name__ == "__main__":
    app.run(debug=True)