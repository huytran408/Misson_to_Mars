from flask import Flask, render_template, redirect
import pymongo
import scrape_mars


####################
# Flask Instance
####################
app = Flask(__name__)

####################
# Database Setup
####################


client = pymongo.MongoClient()
db = client.mars_db
collection = db.mars_facts


####################
# Flask Setup
####################

@app.route("/")
def home():
    mars_info = db.mars_facts.find_one()
    return render_template("index.html", mars_info=mars_info)



@app.route('/scrape')
def scraper():
    db.collection.remove()
    scraped = scrape_mars.scrape()
    db.mars_facts.insert_one(scraped)
    
    return redirect("/")




if __name__ == "__main__":
    app.run(debug=True)