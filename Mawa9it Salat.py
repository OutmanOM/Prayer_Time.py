import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
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

def fetch_and_display_prayer_times():
    city = city_entry.get()
    country = country_entry.get()

    result = fetch_prayer_times(city, country)

    if "Input validation error" in result:
        result_label.config(text=result)
    else:
        result_label.config(text="مواقيت الصلاة")
        # Create a smaller table for prayer timings
        table = ttk.Treeview(window, columns=("Prayer", "Time"), height=11)
        table.heading("#1", text="Prayer")
        table.heading("#2", text="Time")
        table.pack()

        for name, time in result.items():
            table.insert("", "end", values=(name, time))

# Create the main application window
window = tk.Tk()
window.title("Prayer Times App")
window.geometry("700x500")  # Set window size

# Load the background image
image = Image.open("download.jpeg")  # Replace with your image path
background_image = ImageTk.PhotoImage(image)

# Create a label to display the image
background_label = tk.Label(window, image=background_image)
background_label.place(relwidth=1, relheight=1)

# Create and configure labels and entry widgets
city_label = tk.Label(window, text="Enter City:")
city_label.pack()

city_entry = tk.Entry(window)
city_entry.pack()

country_label = tk.Label(window, text="Enter Country:")
country_label.pack()

country_entry = tk.Entry(window)
country_entry.pack()

# Create a button to fetch and display prayer times
fetch_button = tk.Button(window, text="Get Prayer Times", command=fetch_and_display_prayer_times)
fetch_button.pack()

# Create a label to display the result
result_label = tk.Label(window, text="", wraplength=400)
result_label.pack()

# Start the Tkinter main loop
window.mainloop()
