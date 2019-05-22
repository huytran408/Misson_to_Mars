from flask import Flask, render_template, jsonify
import pymongo
import scrape_mars




####################
# Database Setup
####################

client = pymongo.MongoClient()
db = client.mars_db
collection = db.mars_facts

####################
# Flask Setup
####################
app = Flask(__name__)


@app.route('/scrape')
def scrape():
   # db.collection.remove()
    mars = scrape_mars.scrape()
    print("huy\n\n\n")
    db.mars_facts.insert_one(mars)
    return "Some scrapped data"

@app.route("/")
def home():
    mars = list(db.mars_facts.find())
    print(mars)
    return render_template("index.html", mars = mars)


if __name__ == "__main__":
    app.run(debug=True)