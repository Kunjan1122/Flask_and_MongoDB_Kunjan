from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
import json
import os
load_dotenv()

app = Flask(__name__)


# MongoDB connection
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["FlaskDB"]
collection = db["users"]


# Task 1 - JSON API
@app.route("/api") # this create API route
# when we visit http://127.0.0.1:5000/api Flask runs def get_data():
def get_data():
    with open("data.json", "r") as file:  # this open backend file
        data = json.load(file)  # converts json into python data
    return jsonify(data)  # return data as json 

# Home page
@app.route("/")
def home():

    return render_template("index.html")


# Task 2 - Submit form
@app.route("/submit", methods=["POST"])
def submit():
    try:
        name = request.form.get("name")
        email = request.form.get("email")

        if not name or not email:
            return render_template(
                "index.html",
                error="Name and email are required."
            )
        data = {
            "name": name,
            "email": email
        }

        collection.insert_one(data)
        return redirect(url_for("success"))

    except Exception as e:
        return render_template(
            "index.html",
            error=f"Error: {str(e)}"
        )


# Success page
@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)