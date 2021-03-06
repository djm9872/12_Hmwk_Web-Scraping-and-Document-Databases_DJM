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
   
    table = scrape_mars_djm.scrape_table()

    destination_data = mongo.db.collection.find_one()

    # table = mongo.db.collection.find_one({"table":})    
    # Return template and data
    return render_template("index_djm.html", scrape=destination_data, tables=[table.to_html(index=False)])


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    scrape_dict = scrape_mars_djm.scrape_info()
    
    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, scrape_dict, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)


#  destination_data = list(mongo.db.collection.find_one({}, {"table":1})