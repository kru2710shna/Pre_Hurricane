from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai
import requests
from datetime import datetime, timedelta
import os
import numpy as np
import joblib
from geopy.distance import geodesic
from flask_cors import CORS




model = joblib.load('/Users/krushna/Downloads/best_random_forest_model1.pkl')
preprocessor = joblib.load('/Users/krushna/Downloads/preprocessor1.pkl')

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
openweather_api_key = os.getenv('openweather_api_key')
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
 

# Check if GEMINI_API_KEY is set
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    raise ValueError("GEMINI_API_KEY environment variable not set.")


# Route for the index page
@app.route('/')
def index():
    # Handle missing API keys for weather and maps gracefully
    if not openweather_api_key or not GOOGLE_MAPS_API_KEY:
        return "API keys missing. Please check your .env file.", 500
    return render_template('index.html',
                           openweather_api_key=openweather_api_key, 
                           google_maps_api_key=GOOGLE_MAPS_API_KEY
                        )

# Route for Gemini chatbot to give hurricane tips

@app.route('/gemini_chatbot', methods=['POST'])
def gemini_chatbot():
    data = request.get_json()
    question = data.get('question', '').strip()

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
                temperature=1.0
            )
        )

        # Directly access candidates in the response
        candidates = response.candidates if hasattr(response, 'candidates') else []

        if candidates and len(candidates) > 0:
            chatbot_response = candidates[0].content.parts[0].text
        else:
            chatbot_response = "Sorry, I couldn't find an answer."

        return jsonify({"response": chatbot_response})

    except Exception as e:
        print(f"Error with Gemini API: {e}")
        return jsonify({"response": "Sorry, something went wrong with the chatbot."}), 500

@app.route('/predict_status', methods=['POST'])
def predict_status():
    data = request.get_json()
    print("Received request data:", data)

    lat = data.get('lat')
    lng = data.get('lng')
    wind_speed = data.get('wind_speed')
    pressure = data.get('pressure')
    distance_to_land = data.get('distance_to_land')
    day_night = data.get('day_night')

    # Validate inputs
    # if None in [lat, lng, wind_speed, pressure, distance_to_land, day_night]:
    #     return jsonify({"error": "Missing required inputs"}), 400

    try:
        # Convert to floats
        wind_speed = float(wind_speed)
        pressure = float(pressure)
        distance_to_land = float(distance_to_land)
        lat = float(lat)
        lng = float(lng)

        # Prepare input data
        input_data = np.array([[wind_speed, pressure, distance_to_land, lat, lng, day_night]])
        processed_input_data = preprocessor.transform(input_data)

        # Perform prediction
        prediction = model.predict(processed_input_data)
        
        print(prediction)
        # Return prediction
        return jsonify({"status": str(prediction[0])})
    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({"error": "Prediction failed"}), 500
    
    
    

    
def get_weather_data(lat, lon, api_key,landmass_coords):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url)
    weather_data = response.json()

    # Extract relevant fields
    dt = weather_data['dt']
    timezone_offset = weather_data['timezone']
    wind_speed_mps = weather_data['wind']['speed']  # Get wind speed from the API response
    sea_level_pressure = weather_data['main']['pressure']

    # Convert Unix timestamp to UTC datetime
    utc_time = datetime.utcfromtimestamp(dt)

    # Apply the timezone offset
    local_time = utc_time + timedelta(seconds=timezone_offset)

    # Get the day of the week and time
    day_of_week = local_time.strftime('%A')  # e.g., Monday
    local_time_str = local_time.strftime('%Y-%m-%d %H:%M:%S')
    wind_speed_kmh = wind_speed_mps * 3.6
    
    # Calculate the distance to land (find nearest landmass using geodesic distance)
    distance_to_land = calculate_distance_to_land(lat, lon, landmass_coords)

    return {
        "local_time": local_time_str,
        "day_of_week": day_of_week,
        "weather_data": weather_data,
        "wind_speed": wind_speed_kmh,  # Include wind speed in the return data
        "sea_level_pressure": sea_level_pressure,
        "distance_to_land": distance_to_land
    }


@app.route('/get_distance_to_land', methods=['GET'])
def get_distance_to_land():
    lat = request.args.get('lat')
    lng = request.args.get('lng')

    if not lat or not lng:
        return jsonify({"error": "Missing latitude or longitude"}), 400

    # Call the function to calculate distance to land (from previous logic)
    landmass_coords = [
        # Example coordinates; replace with your actual landmass data
        (37.7749, -122.4194),  
        (34.0522, -118.2437),
        # Add more landmass coordinates here
    ]
    distance_to_land = calculate_distance_to_land(float(lat), float(lng), landmass_coords)

    # Return the distance as JSON
    return jsonify({"distance_to_land": distance_to_land})
    
def calculate_distance_to_land(lat, lon, landmass_coords):
    current_location = (lat, lon)
    min_distance = float('inf')  # Initialize with a very large number

    for land_lat, land_lon in landmass_coords:
        land_location = (land_lat, land_lon)
        # Calculate the distance using the geodesic function from geopy
        distance = geodesic(current_location, land_location).kilometers
        if distance < min_distance:
            min_distance = distance

    return min_distance

    
if __name__ == '__main__':
    app.run(debug=True)