# email_templates.py

def subscription_thank_you_message(name):
    """
    Generate a personalized thank-you message for new subscribers.

    Parameters:
        name (str): The subscriber's name.

    Returns:
        str: A formatted thank-you message for the subscriber.
    """
    message = f"""
    Hello {name},

    Thank you for subscribing to Hurricane Prediction Alerts!

    You will receive real-time notifications and updates on hurricane activities 
    and related weather warnings based on your location and data from reliable 
    sources, including OpenWeather and Google Earth Engine.

    Here's what you can expect:
    - Timely alerts on hurricane patterns in your area.
    - Safety tips and recommendations during hurricane season.
    - Personalized assistance for disaster preparedness.

    Stay informed and stay safe!

    Best Regards,
    Hurricane Prediction Alert Team
    """
    return message
