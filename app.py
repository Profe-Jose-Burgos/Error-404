from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

#from flask_cors import CORS

from chat import get_response

app = Flask(__name__)



@app.get("/")
def index_get():
    return render_template("base.html")


@app.post("/predict")
def predictier():
    text = request.get_json().get("message")
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)

if __name__ == "__main__":
    app.debug = True
    app.run()