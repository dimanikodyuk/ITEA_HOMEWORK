# ДЛЯ СЕБЯ
from flask import Flask, request, render_template, Response

import json

app = Flask(__name__, template_folder='templates')

@app.route("/ping")
def ping():
    return {
        "status": 1,
        "result": "OK"
    }

my_name = "Никодюк Дмитрий Витальевич"

@app.route("/")
@app.route("/main", methods=["GET"])
def homepage():
    return render_template("index.html", user_data=my_name)

@app.route("/create_test_data", methods=["POST"])
def create_data():
    return "OK"


@app.route("/uploader", methods=["GET", "POST"])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f"homework_11/{f.filename}")
        return "SAVED FILE"


app.run(debug=True)

