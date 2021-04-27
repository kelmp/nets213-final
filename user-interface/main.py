from flask import Flask, render_template, request
import json
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/model", methods=['POST'])
def run_model():
    action = request.form["action"]
    # output = model(action)
    output = { "action": "sample action response" }
    return json.dumps(output)