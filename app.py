from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai
import os

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
    
    
if __name__ == '__main__':
    app.run(debug=True)
