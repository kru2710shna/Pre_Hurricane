from flask import Flask, render_template
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Route for the index page
@app.route('/')
def index():
    # Get API keys from environment variables
    openweather_api_key = os.getenv('OPENWEATHERMAP_API_KEY')
    google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    
    # Pass the keys to the HTML template
    return render_template('index.html', openweather_api_key=openweather_api_key, google_maps_api_key=google_maps_api_key)

if __name__ == '__main__':
    app.run(debug=True)
