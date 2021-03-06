from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
#app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
#mongo = PyMongo(app)
@app.route("/")
def index():

    # Find one record of data from the mongo database
    mars_dict = mongo.db.collection.find_one()
    # Return template and data
    return render_template("index.html", mars=mars_dict)


@app.route("/scrape")
def scrape():
     mars_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
     mongo.db.collection.update_one({}, {"$set": mars_data}, upsert=True)
    
     return redirect("/", code = 302)

if __name__ == "__main__":
    app.run(debug=True)