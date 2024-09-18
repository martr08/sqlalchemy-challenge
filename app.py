# Import the dependencies.
from flask import Flask, jsonify, request
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
import datetime as dt
import numpy as np
import pandas as pd


#################################################
# Database Setup
#################################################
# reflect an existing database into a new model Resources\hawaii.sqlite Resources\app.py
engine = create_engine(f"sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Base.classes.keys()
measurement = Base.classes.measurement
station = Base.classes.station
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
# Start at the homepage.# List all the available routes.
@app.route("/")
def home():
    """List all available routes"""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

# /api/v1.0/precipitation

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(measurement.date, measurement.prcp).all()
    session.close()

    all_prcp = []
    for date,prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)
 

# /api/v1.0/stations
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    list_stations = session.query(station.station).distinct().all()
    session.close()

    return jsonify([station[0] for station in list_stations])

#Query the dates and temperature observations of the most-active station for the previous year of data.
#Return a JSON list of temperature observations for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    # Calculate the date one year ago from today
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    # Define the most active station ID
    most_active_station_id = 'USC00519281'
    # Query the temperature observations for the most active station for the past year
    most_active_station_temp = session.query(measurement.tobs)\
        .filter(measurement.station == most_active_station_id)\
        .filter(measurement.date >= year_ago).all()
    session.close()
    # Return the temperature observations as a JSON list
    return jsonify([temp[0] for temp in most_active_station_temp])

#     # Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a given start or start-end range
#     return jsonify({'min': temps[0][0], 'avg': round(temps[0][1], 1), 'max': temps[0][2]})
@app.route("/api/v1.0/<start>")
def temperature_stats2(start):
    # Print request info to terminal for tracking

    # Create new session link
    session = Session(engine)

    # Query for temperature data
    temps = session.query(func.min(measurement.tobs), 
                          func.avg(measurement.tobs), 
                          func.max(measurement.tobs))\
                   .filter(measurement.date >= start).first()
    


    # Close session once queries are complete
    session.close()
    print("__________________________________________________")
    print("Server received request for 'Start Date' search...")
    print(temps)
    print("__________________________________________________")

    #Transform tupple 
    return jsonify(list(temps))

@app.route("/api/v1.0/<start>/<end>")
def temperature_stats(start,end):
    # Print request info to terminal for tracking

    # Create new session link
    session = Session(engine)

    # Query for temperature data
    temps = session.query(func.min(measurement.tobs), 
                          func.avg(measurement.tobs), 
                          func.max(measurement.tobs))\
                   .filter(measurement.date >= start).filter(measurement.date<= end).first()
    


    # Close session once queries are complete
    session.close()
    # print("__________________________________________________")
    # print("Server received request for 'Start Date' search...")
    # print(temps)
    # print("__________________________________________________")

    #Transform tupple 
    return jsonify(list(temps))

    # # Check if any results were returned
    # if not temps or temps[0][0] is None:
    #     return jsonify({"error": "No data found for the specified date"}), 404
    
if __name__ == "__main__":
    app.run(debug=True)


################################################
