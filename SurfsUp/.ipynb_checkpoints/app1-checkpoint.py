import numpy as np
import pandas as pd
import datetime as dt
#from datetime import datetime, timedelta

# Python SQL toolkit and Object Relational Mapper
#import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(autoload_with = engine)
session = Session(engine)
# reflect the tables
Station = Base.classes.station
Measurement = Base.classes.measurement

#setting up flask
#Import Flask
from flask import Flask, jsonify
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
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
        f"<p>'start' and 'end' date should be in the format MMDDYYYY.</p>"
    )

# Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data)
# to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():
    """"return the precipitation data for the last 12 months data"""
    #calculate the date 1 year ago from last date in the database
    prev_yr = dt.date(2017,8,23)-dt.timedelta(days = 365)

    #query for the dtae and precipitation for the last year
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_yr).all()
    session.close()

    precipitation_data = {date: prcp for date, prcp in precipitation}
    return jsonify(precipitation_data)


#Return a JSON list of stations from the dataset
#Stations Route (/api/v1.0/stations):

@app.route('/api/v1.0/stations')
def stations():
    results = session.query(Station.name).all()
    session.close()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

#Query the dates temperature observations for the most active station for the previous year of data
#Temperature Observations Route (/api/v1.0/tobs):

@app.route('/api/v1.0/tobs')
def tobs():
    """"return the temperature observations data for the most activae station for the previous year"""
    #calculate the date 1 year ago from last date in the database
    prev_yr = dt.date(2017,8,23)-dt.timedelta(days = 365)

    #query for the temperature observation for the previous year
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_yr).all()
    session.close()
    temperature = list(np.ravel(results))
    return jsonify(temperature=temperature)

#return JSON list of min, avg, and max temperatures based on the provided dates.
#Temperature Statistics Routes (/api/v1.0/<start> and /api/v1.0/<start>/<end>):

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start = None, end = None):
    # Select statement
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        # start = dt.datetime.strptime(start, "%m/%d/%Y")
        # # calculate TMIN, TAVG, TMAX for dates greater than start
        # results = session.query(*sel).\
        #     filter(Measurement.date >= start).all()
        # # Unravel results into a 1D array and convert to a list
        # temps = list(np.ravel(results))
        # return jsonify(temps)

        start = dt.datetime.strptime(start, "%m%d%Y")
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()

        session.close()

        temps = list(np.ravel(results))
        return jsonify(temps)

    # calculate TMIN, TAVG, TMAX with start and stop
    start = dt.datetime.strptime(start, "%m%d%Y")
    end = dt.datetime.strptime(end, "%m%d%Y")
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    session.close()

    # Unravel results into a 1D array and convert to a list
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

if __name__ == '__main__':
    app.run()