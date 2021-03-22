from flask import Flask, render_template, redirect
import PyMongo
import scrape_mars

app = Flask(_name_)

mongo = PyMongo(app, uri='mongodb://localhost:27017/mars_app')

@app.route("/")
def home():
    mars_dict = mongo.db.mars_dict.find_one()
    return render_template("index.html", mars = mars_dict)

@app.route("/scrape")
def scrape():
     mars_dict = mongo.db.mars_dict
     mars_data = scrape_mars.scrape
     mars_dict.update({}, mars_data, upsert=True)
     return redirect("/")

if __name__ == "_main_":
    app.run(debug=True)