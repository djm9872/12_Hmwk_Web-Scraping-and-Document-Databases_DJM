from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
import scrape_mars_djm

# Create an instance of Flask
app = Flask(__name__)

# # Use PyMongo to establish Mongo connection
# mongo = PyMongo(app, uri="mongodb://localhost:27017/weather_app")

# setup mongo connection
conn = "mongodb://localhost:27017"
mongo = pymongo.MongoClient(conn)

# connect to mongo db. Will create one if not alreayd available.
db = mongo.mars_scrape_db

# Drops collection if available to remove duplicates
db.scrape_table.drop()

collection = db.scrape_table


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    destination_data = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index_djm.html", scrape=destination_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = scrape_mars_djm.scrape_info()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)