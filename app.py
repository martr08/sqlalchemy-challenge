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

#Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
#For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
# Route for a specified start date
# /api/v1.0/<start>
# Route for only start date
# @app.route("/api/v1.0/<start>")
# def temperature_stats_start_only(start):

#     return temperature_stats(start, None)  # Pass None for end date

# # Route for both start and end date
# @app.route("/api/v1.0/<start>/<end>")
# def temperature_stats_start_end(start, end):
#     return temperature_stats(start, end)

# Route for only start date
@app.route("/api/v1.0/<start>")
def temperature_stats(start, end=None):  # Make 'end' default to None
    # Validate and parse the start date
    try:
        start_date = dt.datetime.strptime(start, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid start date format. Use YYYY-MM-DD."}), 400

    # Validate and parse the end date if provided
    if end:
        try:
            end_date = dt.datetime.strptime(end, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid end date format. Use YYYY-MM-DD."}), 400
        else:
            end_date = dt.date.today()  # Use today's date if no end date is provided

    # Query logic for fetching temperature data (your existing logic goes here)
    # For example:
    # temperature_data = session.query(...).filter(...).all()
    
    return jsonify({
        "TMIN": ...,
        "TAVG": ...,
        "TMAX": ...,
    })
# Route for only start date
@app.route("/api/v1.0/<start>")
def temperature_stats_start_only(start):
    return temperature_stats(start, None)  # Explicitly pass None for end

# Route for both start and end dates
@app.route("/api/v1.0/<start>/<end>")
def temperature_stats_start_end(start, end):
    return temperature_stats(start, end)
if __name__ == "__main__":
    app.run(debug=True)


################################################



# Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) 
# to a dictionary using date as the key and prcp as the value.

# Return the JSON representation of your dictionary.

# /api/v1.0/stations

# Return a JSON list of stations from the dataset.
# /api/v1.0/tobs

# Query the dates and temperature observations of the most-active station for the previous year of data.

# Return a JSON list of temperature observations for the previous year.

# /api/v1.0/<start> and /api/v1.0/<start>/<end>

# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.

# For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.

#@app.route("/api/v1.0/2016-01-01/2016-01-31")
# def temperature_stats(start, end):
#     # Validate and parse the start date
#     try:
#         start_date = dt.datetime.strptime(start, "%Y-%m-%d").date()
#     except ValueError:
#         return jsonify({"error": "Invalid start date format. Use YYYY-MM-DD."}), 400
    
#     # Validate and parse the end date if provided
#     if end:
#         try:
#             end_date = dt.datetime.strptime(end, "%Y-%m-%d").date()
#         except ValueError:
#             return jsonify({"error": "Invalid end date format. Use YYYY-MM-DD."}), 400
#     else:
#         end_date = dt.date.today()  # Use today's date if no end date is provided

#     # Query for temperature data in the specified date range
#     query = session.query(
#         func.min(measurement.tobs).label('TMIN'),
#         func.avg(measurement.tobs).label('TAVG'),
#         func.max(measurement.tobs).label('TMAX')
#     ).filter(
#         measurement.date >= start_date,
#         measurement.date <= end_date
#     ).all()

#     # Extract results from the query
#     if query:
#         result = query[0]  # Since we are using aggregation, we expect a single result
#         temperature_stats = {
#             "TMIN": result.TMIN,
#             "TAVG": result.TAVG,
#             "TMAX": result.TMAX
#         }
#     else:
#         temperature_stats = {
#             "TMIN": None,
#             "TAVG": None,
#             "TMAX": None
#         }

#     return jsonify(temperature_stats)