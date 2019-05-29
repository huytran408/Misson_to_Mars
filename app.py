from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


####################
# Flask Instance
####################
app = Flask(__name__)

####################
# Database Setup
####################

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")


####################
# Flask Setup
####################

@app.route("/")
def home():
    mars_info = mongo.db.mars_facts.find()
    return render_template("index.html", mars_info=mars_info)



@app.route('/scrape')
def scrape():
   # db.collection.remove()
    mars = scrape_mars.scrape()
    
    collection = mongo.db.mars_facts
    collection.update({}, mars, upsert=True)
    print(mars)
    return "Some scrapped data"




if __name__ == "__main__":
    app.run(debug=True)