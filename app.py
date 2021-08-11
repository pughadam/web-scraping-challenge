
# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.team_db

# Drops collection if available to remove duplicates
db.team.drop()


# Set route to MongoDB and pass the index.html to display the data
@app.route('/')
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route('/')
def scrapper():
    mars = mongo.db.mars_data
    mars_data = scrape_mars.scrape_all()
    mars.update({}, mars_data, upsert=True)

    # Return the template with the teams list passed in
    return "Successful Scrape"


if __name__ == "__main__":
    app.run(debug=True)
