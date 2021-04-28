from flask import Flask, render_template, request
import json
import csv
import random
from os import path

app = Flask(__name__)

# load combat_text.csv into memory
hits = []
with open("../data/combat_text.csv") as file:
    csv_in = csv.reader(
        file,
        delimiter=",",
    )
    for row in csv_in:
        hits.append(row[1])
    hits = hits[1:]

# create response file with header if does not already exist
if not path.exists("responses.csv"):
    with open("responses.csv", "a") as file:
        file.write("WorkerId,Input.prompt,Answer.answer\n")


@app.route("/")
def index():
    return render_template("hit.html")


@app.route("/hit", methods=["GET"])
def get_hit():
    return random.choice(hits)


@app.route("/hit", methods=["POST"])
def save_hit():
    worker_id = request.form["name"]
    text = request.form["text"]
    actions = request.form["actions"]
    with open("responses.csv", "a") as file:
        csv_out = csv.writer(
            file, delimiter=",", quotechar="`", quoting=csv.QUOTE_NONNUMERIC
        )
        csv_out.writerow([worker_id, text, actions])

    return json.dumps({"success": True}), 200, {"ContentType": "application/json"}