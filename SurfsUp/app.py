# Import the dependencies.
from flask import Flask, jsonify

# imports
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# set up flask app
app = Flask(__name__)

# home route
@app.route("/")
def home():
        return(
              f"<center><h1>Welcome to the Hawaii Climate Analysis Local API Tool<h1></center>"
              f"<center><h2>Select from one of the available routes:<h2></center>"
              f"<center>/api/v1.0/precipitation</center>"
              f"<center>/api/v1.0/stations</center>"
              f"<center>/api/v1.0/tobs</center>"
              f"<center>/api/v1.0/<start></center>"
              f"<center>/api/v1.0/<start>/<end></center>"
              )



# Database Setup
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
base = automap_base()
# reflect the tables
base.prepare(engine, reflect=True)

# Save references to each table
measurement = base.classes.measurement
station = base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Routes

# /api/v1.0/precipitation route
@app.route("/api/v1.0/precipitation")
def precip():
      # return the previous years precipitation as a json
      # Calculate the date one year from the last date in data set.
      py=dt.date(2017, 8, 23) - dt.timedelta(days=365)  
      # Perform a query to retrieve the date and precipitation scores
      results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= py).all()
      # close session
      session.close()
      # dictionary with the date as the key and the precipitation (prcp) as the value
      precipitation = {date: prcp for date, prcp in results}
      # convert to a json
      return jsonify(precipitation)

# /api/v1.0/stations route
@app.route("/api/v1.0/stations")
def stations():
      # list of the stations
      # Perform a query to retrieve the name of the stations
      results = session.query(station.station).all()
      # close session
      session.close()
      # make the list of stations
      stationList = list(np.ravel(results))
      #convert list to json and display
      return jsonify(stationList)

# /api/v1.0/tobs route
@app.route("/api/v1.0/tobs")
def tobs():
      # return the previous year temp
      # Calculate the date one year from the last date in data set.
      py=dt.date(2017, 8, 23) - dt.timedelta(days=365)  
      # Perform a query to retrieve the temp from the most active station from the past year
      results = session.query(measurement.tobs).filter(measurement.station == 'USC00519281').\
            filter(measurement.date >= py).all()
      # close session
      session.close()
      # make the list of temps
      tempList = list(np.ravel(results))
      #convert list to json and display
      return jsonify(tempList)

#  /api/v1.0/start and /api/v1.0/start/end
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def dateStats(start=None, end=None):
      
      # selection statement
      selection = [func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)]

      if not end:
            startdate = dt.datetime.strptime(start, "%m%d%Y")
            # perform a query to retrieve the start date information
            results = session.query(*selection).filter(measurement.date >= startdate).all()
            # close session
            session.close()
            # make the list of temps
            tempList = list(np.ravel(results))
            #convert list to json and display
            return jsonify(tempList)
      
      else:
            startdate = dt.datetime.strptime(start, "%m%d%Y")
            enddate = dt.datetime.strptime(start, "%m%d%Y")
            # perform a query to retrieve the enddate date information
            results = session.query(*selection).filter(measurement.date >= startdate)\
                                               .filter(measurement.date <= enddate).all()
            # close session
            session.close()
            # make the list of temps
            tempList = list(np.ravel(results))
            #convert list to json and display
            return jsonify(tempList)

# app launcher

if __name__ == '__main__':
    app.run(debug=True)


