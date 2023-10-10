import requests
import re


def validate_input(city, country):
    # Check if city and country contain only letters, spaces, and hyphens
    valid_city = bool(re.match(r'^[a-zA-Z\s-]+$', city))
    valid_country = bool(re.match(r'^[a-zA-Z\s-]+$', country))

    if not valid_city:
        return "City name should contain only letters, spaces, and hyphens."

    if not valid_country:
        return "Country name should contain only letters, spaces, and hyphens."

    return None

def fetch_prayer_times(city, country):
    validation_error = validate_input(city, country)
    if validation_error:
        return f"Input validation error: {validation_error}"

    url = f"http://api.aladhan.com/v1/timingsByCity?city={city}&country={country}&method=2"

    try:
        response = requests.get(url)
        info = response.json()
        if "data" in info:
            timings = info["data"]["timings"]
            return timings
        else:
            return "Prayer times not available."

    except Exception as e:
        return f"An unexpected error occurred: {e}"

while True:
    city = input("Enter the city: ")
    country = input("Enter the country: ")

    result = fetch_prayer_times(city, country)
    if "Input validation error" in result:
        print(result)
    else:
        print("Prayer Timings:")
        for name, time in result.items():
            print(f"{name}: {time}")
        break

