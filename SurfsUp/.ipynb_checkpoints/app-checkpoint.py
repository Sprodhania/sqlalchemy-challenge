from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
from datetime import datetime, timedelta

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, func, text
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(autoload_with = engine)
session = Session(engine)
# reflect the tables
Station = Base.classes.station
Measurement = Base.classes.measurement

#Import Flask
from flask import Flask
#create and app
app = Flask(__name__)
#Start at the homepage
#list all the available routes
@app.route('/')
def home():
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start (enter as YYYY-MM-DD)<br/>"
        f"/api/v1.0/start/end (enter as YYYY-MM-DD/YYYY-MM-DD)"

    )
# Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data)
# to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()
    precipitation_data = {date: prcp for date, prcp in results}
    return jsonify(precipitation_data)


#Return a JSON list of stations from the dataset
#Stations Route (/api/v1.0/stations):

@app.route('/api/v1.0/stations')
def stations():
    results = session.query(Station.name).all()
    stations_list = [station[0] for station in results]
    return jsonify(stations_list)

#Query the dates temperature observations for the most active station for the previous year of data
#Temperature Observations Route (/api/v1.0/tobs):

@app.route('/api/v1.0/tobs')
def tobs():
    results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281', Measurement.date >= one_year_ago).all()
    temperature_list = [temp[0] for temp in results]
    return jsonify(temperature_list)

#return JSON list of min, avg, and max temperatures based on the provided dates.
#Temperature Statistics Routes (/api/v1.0/<start> and /api/v1.0/<start>/<end>):

@app.route('/api/v1.0/<start>')
def start_date(start):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    return jsonify(results)

@app.route('/api/v1.0/<start>/<end>')
def start_end_date(start, end):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)