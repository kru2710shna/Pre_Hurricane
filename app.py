from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai
import os

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

gemini_api_key = os.getenv("GEMINI_API_KEY")
if gemini_api_key:
    genai.configure(api_key=gemini_api_key)
else:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

genai.configure(api_key=gemini_api_key)

# Route for the index page
@app.route('/')
def index():
    # Get API keys from environment variables
    openweather_api_key = os.getenv('OPENWEATHERMAP_API_KEY')
    google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    
    # Pass the keys to the HTML template
    return render_template('index.html', openweather_api_key=openweather_api_key, google_maps_api_key=google_maps_api_key)

# Route for Gemini chatbot to give hurricane tips
@app.route('/gemini_chatbot', methods=['POST'])
def gemini_chatbot():
    data = request.get_json()
    question = data.get('question', '')

    # Make the request to the Gemini API
    try:
        # Instantiate the model
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Generate content using the Gemini API
        response = model.generate_content(
            question,
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,  # Only one response
                stop_sequences=["."],  # Stop at the end of a sentence
                max_output_tokens=100,  # Limit the response length
                temperature=1.0  # Creativity/temperature of the response
            )
        )

        # Log the full response to inspect the structure
        print("Gemini API Response:", response)

        # Extract the correct response text from the API response
        chatbot_response = response.text

        return jsonify({"response": chatbot_response})

    except Exception as e:
        print(f"Error with Gemini API: {e}")
        return jsonify({"response": "Sorry, something went wrong with the chatbot."}), 500

if __name__ == '__main__':
    app.run(debug=True)