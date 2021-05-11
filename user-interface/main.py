from flask import Flask, render_template, request
import json
import spacy
app = Flask(__name__)

cls = spacy.util.get_lang_class("en")
friends_model = spacy.load("friends_gold_model_ner")
mturk_model = spacy.load("mturk_gold_model_ner")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/model", methods=['POST'])
def run_model():
    action = request.form["action"]
    model = request.form["model"]

    if model == "friends":
        doc = friends_model(action)
    else:
        doc = mturk_model(action)

    labels = ""
    for ent in doc.ents:
        labels += f"{ent.label_}:{ent.text}\n"

    output = { "action": labels }
    return json.dumps(output)