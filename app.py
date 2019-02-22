from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import pymongo
import scrape_mars


app = Flask(__name__)


# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.current_mars_info

# Drops collection if available to remove duplicates
#db.mars.drop()

## PALANI HELPED ME TO GET THIS RIGHT

@app.route("/")
def index():
    mars = db.mars_info.find_one()
    
    # {'nasa_title': "NASA's Opportunity Rover Mission on Mars Comes to End", 
    #   'nasa_article': "NASA's Opportunity Mars rover mission is complete after 15 years on Mars. Opportunity's record-breaking exploration laid the groundwork for future missions to the Red Planet.", 
    #   'mars_featured_image': 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA23040_hires.jpg', 
    #   'mars_weather': 'Sol 2319 (2019-02-13), high -17C/1F, low -72C/-97F, pressure at 8.12 hPa, daylight 06:46-18:52', 
    #   'atitle': ['Cerberus Hemisphere Enhanced', 'Schiaparelli Hemisphere Enhanced', 'Syrtis Major Hemisphere Enhanced', 'Valles Marineris Hemisphere Enhanced'], 
    #   'aimage_url': ['https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg', 'https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg', 'https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg', 'https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg']
    #  }
    
   
    return render_template("index.html", mars = mars)


@app.route("/scrape")
def scrape():
   
    data = scrape_mars.scrape()
    #db.mars_info.remove({})
    db.mars_info.update({},data,upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
