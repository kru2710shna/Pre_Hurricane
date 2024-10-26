# Here is a Python script `gemini.py` that can encapsulate all functionalities related to Google Gemini interactions.
# It will handle generating responses based on weather data, hurricane data, simulations, and any other 
# task Google Gemini is responsible for.

import google.generativeai as genai
import random
import os

# Configuration: Load the API key for Gemini from environment variables.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# If the key isn't set, raise an error
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

# Function to configure and ask Gemini questions related to hurricane simulation, weather analysis, and safety tips.
def ask_gemini(question, weather_data, hurricane_data):
    """
    Takes in user question, real-time weather data, and NOAA hurricane data
    to generate appropriate responses using Google Gemini.

    :param question: User query to ask Gemini.
    :param weather_data: Real-time weather data from OpenWeatherMap API.
    :param hurricane_data: Historical hurricane data from NOAA API.
    :return: Response from Google Gemini API.
    """
    prompts = generate_prompts(question, weather_data, hurricane_data)
    prompt = random.choice(prompts)

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            prompt,
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

        return chatbot_response

    except Exception as e:
        print(f"Error with Gemini API: {e}")
        return "Sorry, something went wrong with the chatbot."

# Function to create different prompt types for Gemini
def generate_prompts(question, weather_data, hurricane_data):
    """
    Generate multiple prompts for various scenarios like hurricane simulation,
    real-time narration, global context insight, and safety tips.

    :param question: User's question
    :param weather_data: Real-time weather data
    :param hurricane_data: Historical hurricane data from NOAA
    :return: List of prompts
    """
    prompts = []

    # # Add simulation prompt
    # prompts.append(f"Simulate a scenario where the wind speed reaches {weather_data['wind_speed']} m/s. What should we expect?")

    # # Add real-time narration prompt
    # prompts.append(f"Narrate the current weather condition. The temperature is {weather_data['temp']}°C, wind speed is {weather_data['wind_speed']} m/s, and the weather is described as {weather_data['description']}.")

    # # Add global context insight prompt
    # prompts.append(f"Compare the current hurricane's wind speed of {weather_data['wind_speed']} m/s to past hurricanes globally.")

    # # Add personalized safety recommendation based on the question
    # prompts.append(f"Provide safety tips based on the current weather, with wind speed {weather_data['wind_speed']} m/s and humidity {weather_data['humidity']}%. The user asked: {question}.")
    
    # General Hurricane Information Prompts
    prompts.extend([
        "What is a hurricane, and how does it form?",
        "What are the different categories of hurricanes, and how are they measured?",
        "What is the difference between a hurricane, a typhoon, and a cyclone?",
        "What are the deadliest hurricanes in history?",
        "How do hurricanes get their names?",
        "What is the structure of a hurricane, and how does the eye of the storm work?",
        "How long does a typical hurricane last?",
        "How are hurricanes monitored and tracked in real-time?",
        "How do scientists predict the path of a hurricane?",
        "What tools and technologies are used to predict hurricanes?"
    ])

    # Real-Time Hurricane Scenarios
    prompts.append(f"Simulate the impact of a Category 5 hurricane hitting a coastal city.")
    prompts.append(f"How does the current weather condition with wind speed of {weather_data['wind_speed']} m/s compare to previous hurricanes?")
    prompts.append(f"What safety measures should people take if wind speeds reach {weather_data['wind_speed']} m/s in this area?")
    prompts.append(f"Given the current hurricane path, what cities are at risk, and how should they prepare?")
    prompts.append(f"What impact will the current humidity of {weather_data['humidity']}% have on the strength of the hurricane?")

    # Safety and Evacuation Prompts
    prompts.append("What are the recommended safety measures during a hurricane?")
    prompts.append("How do I prepare for a hurricane when evacuation isn’t an option?")
    prompts.append(f"Based on the wind speed of {weather_data['wind_speed']} m/s, what is the best time to evacuate?")
    prompts.append("Recommend the safest evacuation routes based on the predicted hurricane path and real-time traffic conditions.")
    prompts.append("What should be included in an emergency kit for a hurricane evacuation?")
    prompts.append("What should people avoid doing during a hurricane?")

    # Hurricane Physics and Calculations
    prompts.append("What mathematical models are used to predict hurricane trajectories?")
    prompts.append(f"Given wind speeds of {weather_data['wind_speed']} m/s, calculate the possible damage in a coastal area.")
    prompts.append(f"How do pressure changes, such as a drop to {weather_data['pressure']} hPa, affect the intensity of a hurricane?")
    prompts.append(f"Given current wind speeds and pressure data, estimate the potential category of this storm.")
    prompts.append(f"Calculate the Coriolis force acting on a hurricane with wind speed of {weather_data['wind_speed']} m/s at a latitude of {weather_data.get('latitude', 'N/A')}.")  # If latitude exists in the data

    # Climate Change and Hurricanes
    prompts.extend([
        "How is climate change affecting the frequency and intensity of hurricanes?",
        "Compare current hurricane patterns to those from 50 years ago. Are storms becoming more frequent or intense?",
        "How does rising ocean temperature influence the formation of hurricanes?",
        "What impact does climate change have on hurricane season duration?",
        "What regions are most vulnerable to increased hurricane activity due to global warming?"
    ])

    # Comparing Current and Historical Data
    prompts.append(f"Compare the current hurricane wind speeds of {weather_data['wind_speed']} m/s with the winds during Hurricane Katrina.")
    prompts.append(f"How does the current hurricane pressure of {weather_data['pressure']} hPa compare to other major hurricanes?")
    prompts.append(f"Compare the storm surge of the current hurricane with historical storms that hit the same region.")
    prompts.append(f"How does the sea surface temperature currently recorded compare to temperatures during major hurricanes?")

    # Prediction and Simulation Prompts
    prompts.append("Predict the trajectory of the hurricane given wind speed, humidity, and pressure readings.")
    prompts.append(f"Simulate the potential landfall of the hurricane in the area and estimate the damage.")
    prompts.append(f"Given the current weather data, how likely is the hurricane to change direction?")
    prompts.append("Simulate the changes in hurricane strength if the sea temperature rises by 2°C.")

    # Real-Time Insights and Context
    prompts.append("What are the current global trends in hurricane formation?")
    prompts.append("How does the current Atlantic hurricane season compare to previous seasons in terms of intensity?")
    prompts.append("What are the most hurricane-prone regions in the world?")
    prompts.append("Based on current weather patterns, what regions are likely to experience increased hurricane activity in the future?")

    # Geographical Impact Prompts
    prompts.append("What are the most vulnerable cities along the Gulf Coast for hurricanes?")
    prompts.append("How does hurricane activity differ between the Atlantic and Pacific Oceans?")
    prompts.append("Which countries are most affected by hurricanes each year?")
    prompts.append(f"Given the current path of the storm, what areas in the region should prepare for the hurricane?")
    prompts.append(f"What impact will a hurricane have on local infrastructure in {weather_data.get('city', 'this area')}, and how should they prepare?")

    # Hurricane Damage and Aftermath
    prompts.extend([
        "How long does it take for cities to recover from major hurricanes?",
        "What are the economic impacts of hurricanes on coastal cities?",
        "What is the role of emergency services during and after a hurricane?",
        "What are the long-term effects of hurricanes on ecosystems?",
        "How are hurricanes affecting insurance premiums in hurricane-prone areas?"
    ])

    # Specific Weather Conditions and Impact
    prompts.append(f"What happens when the sea level pressure drops below {weather_data['sea_level']} hPa during a hurricane?")
    prompts.append(f"How does a wind gust of {weather_data['wind_gust']} m/s influence the destructive power of a hurricane?")
    prompts.append(f"What effect does humidity above {weather_data['humidity']}% have on hurricane intensity?")
    prompts.append(f"Given the current wind direction of {weather_data['wind_deg']}°, how will it affect the storm's path?")

    # Advanced Meteorology and Calculations
    prompts.append(f"Calculate the energy released by a hurricane with a radius of 100 km and wind speeds of {weather_data['wind_speed']} m/s.")
    prompts.append("How does the angular velocity of a hurricane change with increasing wind speed?")
    prompts.append("Use the Navier-Stokes equation to model airflow in a hurricane.")
    prompts.append(f"Calculate the change in sea surface temperature required to intensify a Category 3 hurricane into a Category 5 storm.")

    # Personalized Safety Recommendation
    prompts.append(f"Provide safety tips based on the current weather, with wind speed {weather_data['wind_speed']} m/s and humidity {weather_data['humidity']}%. The user asked: {question}.")
    
    return prompts
