import datetime
import random



def tool_get_time():
    """Returns the current date and time as a string."""
    now = datetime.datetime.now()
    return {"time": now.strftime("%Y-%m-%d %H:%M:%S")}


def tool_random_number():
    """Returns a random integer between 1 and 100."""
    return {"number": random.randint(1, 100)}

def tool_fake_weather(location: str):
    """Returns a fake weather report for the given location."""
    return {"weather": f"Sunny and warm in {location}"}


