import random
from datetime import datetime

def get_time():
    return {"time": datetime.now().astimezone().isoformat()}

def random_number():
    return {"number": random.randint(1, 100)}

def fake_weather(location: str):
    return {
        "location": location,
        "forecast": "Sunny with light wind",
        "temperature_c": 24,
    }


def failing_tool():
    """ A tool that always fails to demonstrate error handling """
    raise ValueError("Simulated tool failure.")
