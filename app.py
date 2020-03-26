from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)
#mongo = PyMongo(app, uri='mongodb://localhost:27017/mars_app')

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_info = mongo.db.mars_info.find_one()

    # Return template and data
    return render_template("index.html", mars_info=mars_info)


# Route that will trigger the scrape function
@app.route("/scrape")
# Run the scrape function
def scrape():

    mars_info = mongo.db.mars_info
    mars_news = scrape_mars.scrape_mars_news()
    mars_image = scrape_mars.scrape_mars_image()
    mars_facts = scrape_mars.scrape_mars_facts()
    mars_weather = scrape_mars.scrape_mars_weather()
    mars_hemispheres = scrape_mars.scrape_mars_hemispheres()
    
    print(mars_news)
    print(mars_image)
    print(mars_facts)
    print(mars_weather)
    print(mars_hemispheres)
    
    # Update the Mongo database using update and upsert=True
    mars_info.update({}, mars_news, upsert=True)
    mars_info.update({}, mars_image, upsert=True)
    mars_info.update({}, mars_facts, upsert=True)
    mars_info.update({}, mars_weather, upsert=True)
    mars_info.update({}, mars_hemispheres, upsert=True)
    

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
