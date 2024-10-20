from flask import Flask, render_template, request, redirect, jsonify
from dotenv import load_dotenv
import google.generativeai as genai
import requests
from datetime import datetime, timedelta
import os
import numpy as np
import joblib
from geopy.distance import geodesic
import pandas as pd
import mysql.connector


# Function to establish a connection to the Cloud SQL database
# def get_db_connection():
#     connection = mysql.connector.connect(
#         user=os.getenv('DB_USER'),
#         password=os.getenv('DB_PASSWORD'),
#         host=os.getenv('DB_HOST'),  # Use /cloudsql/project:region:instance for Unix socket connection
#         database=os.getenv('DB_NAME')
#     )
#     return connection

    
    
model = joblib.load("best_random_forest_model4.pkl")
preprocessor = joblib.load("preprocessor4.pkl")

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
openweather_api_key = os.getenv("openweather_api_key")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")


# Check if GEMINI_API_KEY is set
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    raise ValueError("GEMINI_API_KEY environment variable not set.")


# Route for the index page
@app.route("/")
def index():
    # Handle missing API keys for weather and maps gracefully
    if not openweather_api_key or not GOOGLE_MAPS_API_KEY:
        return "API keys missing. Please check your .env file.", 500
    return render_template(
        "index.html",
        openweather_api_key=openweather_api_key,
        google_maps_api_key=GOOGLE_MAPS_API_KEY,
    )


# Route for Gemini chatbot to give hurricane tips


@app.route("/gemini_chatbot", methods=["POST"])
def gemini_chatbot():
    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"response": "Please ask a valid question."}), 400

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            question,
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,
                stop_sequences=["."],
                max_output_tokens=100,
                temperature=1.0,
            ),
        )

        # Directly access candidates in the response
        candidates = response.candidates if hasattr(response, "candidates") else []

        if candidates and len(candidates) > 0:
            chatbot_response = candidates[0].content.parts[0].text
        else:
            chatbot_response = "Sorry, I couldn't find an answer."

        return jsonify({"response": chatbot_response})

    except Exception as e:
        print(f"Error with Gemini API: {e}")
        return jsonify(
            {"response": "Sorry, something went wrong with the chatbot."}
        ), 500
    



@app.route("/predict_status", methods=["POST"])
def predict_status():
    label_mapping = {
        0: "Disturbance (0-20 mph) - A weak, disorganized system with minimal wind, often the early stage of a developing storm.",
        1: "Extratropical Cyclone (30-60 mph) - Storms formed outside the tropics, often bringing heavy rain and strong winds.",
        2: "Hurricane (74+ mph) - A powerful tropical storm with sustained winds above 74 mph, causing significant damage and heavy rainfall.",
        3: "Gale Winds (39-54 mph) - Strong winds that can cause minor damage, but are not part of a tropical storm or hurricane.",
        4: "Subtropical Depression (0-38 mph) - A weaker subtropical system with lower wind speeds, a mix of tropical and extratropical characteristics.",
        5: "Subtropical Storm (39-73 mph) - A storm with both tropical and extratropical characteristics, typically less organized than a hurricane.",
        6: "Tropical Depression (0-38 mph) - A tropical system with winds below 39 mph, often a precursor to a tropical storm.",
        7: "Tropical Storm (39-73 mph) - A well-developed tropical system with winds between 39 and 73 mph, less intense than a hurricane.",
        8: "Clear Sky (0 mph) - Calm weather with no active storm or disturbance.",
        9: "Tropical Wave (10-30 mph) - A tropical disturbance with low wind speeds, which could develop into a stronger system.",
    }
    try:
        # Create the encoded number to label mapping
        # Get the JSON data from the request
        data = request.get_json()
        print("Received request data:", data)

        # Extract the input values from the JSON payload
        lat = data.get("latitude")
        lng = data.get("longitude")
        wind_speed = data.get("windSpeed")
        pressure = data.get("pressure")
        distance_to_land = data.get("distanceToLand")
        day_night = data.get("day_night")

        # Convert to floats and handle potential missing values
        wind_speed = float(wind_speed)
        pressure = float(pressure)
        distance_to_land = float(distance_to_land)
        lat = float(lat)
        lng = float(lng)
        wind_pressure_ratio = float(wind_speed / pressure)
        day_night = float(day_night)

        # Prepare the input data as a pandas DataFrame
        input_data_df = pd.DataFrame(
            {
                "USA_WIND": [wind_speed],
                "USA_PRES": [pressure],
                "DIST2LAND": [distance_to_land],
                "USA_LAT": [lat],
                "USA_LON": [lng],
                "wind_pressure_ratio": [wind_pressure_ratio],
                "Day_Night_encoded": [day_night],
            }
        )

        print(f"Input DataFrame:\n{input_data_df}")

        # Preprocess the input data using the loaded preprocessor
        processed_input_data = preprocessor.transform(input_data_df)
        print(f"Processed input data:\n{processed_input_data}")

        # Perform prediction using the loaded model
        prediction = model.predict(processed_input_data)

        predicted_label = label_mapping.get(prediction[0], "Clear Sky")

        # print(f"Prediction: {prediction}")
        print(f"Prediction: {prediction[0]} -> {predicted_label}")

        # Return the prediction result as JSON
        return jsonify({"status": predicted_label})

    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({"error": "Prediction failed"}), 500


def get_weather_data(lat, lon, api_key, landmass_coords):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url)
    weather_data = response.json()

    # Extract relevant fields
    dt = weather_data["dt"]
    timezone_offset = weather_data["timezone"]
    wind_speed_mps = weather_data["wind"][
        "speed"
    ]  # Get wind speed from the API response
    sea_level_pressure = weather_data["main"]["pressure"]

    # Convert Unix timestamp to UTC datetime
    utc_time = datetime.utcfromtimestamp(dt)

    # Apply the timezone offset
    local_time = utc_time + timedelta(seconds=timezone_offset)

    # Get the day of the week and time
    day_of_week = local_time.strftime("%A")  # e.g., Monday
    local_time_str = local_time.strftime("%Y-%m-%d %H:%M:%S")
    wind_speed_kmh = wind_speed_mps * 3.6

    # Calculate the distance to land (find nearest landmass using geodesic distance)
    distance_to_land = calculate_distance_to_land(lat, lon, landmass_coords)

    return {
        "local_time": local_time_str,
        "day_of_week": day_of_week,
        "weather_data": weather_data,
        "wind_speed": wind_speed_kmh,  # Include wind speed in the return data
        "sea_level_pressure": sea_level_pressure,
        "distance_to_land": distance_to_land,
    }


@app.route("/get_distance_to_land", methods=["GET"])
def get_distance_to_land():
    lat = request.args.get("lat")
    lng = request.args.get("lng")

    if not lat or not lng:
        return jsonify({"error": "Missing latitude or longitude"}), 400

    # Call the function to calculate distance to land (from previous logic)
    landmass_coords = [
        # Example coordinates; replace with your actual landmass data
        (37.7749, -122.4194),
        (34.0522, -118.2437),
        # Add more landmass coordinates here
    ]
    distance_to_land = calculate_distance_to_land(
        float(lat), float(lng), landmass_coords
    )

    # Return the distance as JSON
    return jsonify({"distance_to_land": distance_to_land})


def calculate_distance_to_land(lat, lon, landmass_coords):
    current_location = (lat, lon)
    min_distance = float("inf")  # Initialize with a very large number

    for land_lat, land_lon in landmass_coords:
        land_location = (land_lat, land_lon)
        # Calculate the distance using the geodesic function from geopy
        distance = geodesic(current_location, land_location).kilometers
        if distance < min_distance:
            min_distance = distance

    return min_distance

def get_db_connection():
    
    db_config = {
        'user': '{DB_USER}',
        'password': '{DB_PASSWORD}',
        'host': '134.134.183.11',  # Replace with Cloud SQL public IP or use localhost if using Cloud SQL Proxy
        'port': 3306,
        'database': 'prehurricane'
    }
    
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("Connected to the database successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        
    return connection


@app.route('/subscribe', methods=['POST'])
def subscribe():
    try:
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        print(f"Received form data: Name={name}, Email={email}, Phone={phone}")

        connection = get_db_connection()
        cursor = connection.cursor()

        query = "INSERT INTO subscribers (name, email, phone) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, phone))
        connection.commit()

        cursor.close()
        connection.close()

        return redirect('/')
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while subscribing.", 500

if __name__ == "__main__":
    app.run(debug=True)
