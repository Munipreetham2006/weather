import tkinter as tk
from tkinter import messagebox
import requests
from geopy.geocoders import Nominatim

# Weather code descriptions
weather_codes = {
    0: "Clear Sky",
    1: "Mainly Clear",
    2: "Partly Cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing Rime Fog",
    51: "Light Drizzle",
    53: "Moderate Drizzle",
    55: "Dense Drizzle",
    61: "Slight Rain",
    63: "Moderate Rain",
    65: "Heavy Rain",
    71: "Slight Snow",
    73: "Moderate Snow",
    75: "Heavy Snow",
    80: "Rain Showers",
    81: "Moderate Rain Showers",
    82: "Violent Rain Showers",
    95: "Thunderstorm"
}

def get_weather():
    city = city_entry.get().strip()

    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    try:
        geolocator = Nominatim(user_agent="weather_app")
        location = geolocator.geocode(city)

        if location is None:
            messagebox.showerror("Error", "City not found.")
            return

        latitude = location.latitude
        longitude = location.longitude

        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={latitude}"
            f"&longitude={longitude}"
            f"&current=temperature_2m,relative_humidity_2m,"
            f"wind_speed_10m,weather_code"
        )

        response = requests.get(url)
        data = response.json()

        current = data["current"]

        temperature = current["temperature_2m"]
        humidity = current["relative_humidity_2m"]
        wind_speed = current["wind_speed_10m"]
        weather_code = current["weather_code"]

        condition = weather_codes.get(
            weather_code,
            "Unknown"
        )

        result_label.config(
            text=(
                f"📍 City: {location.address}\n\n"
                f"🌡 Temperature: {temperature}°C\n"
                f"💧 Humidity: {humidity}%\n"
                f"🌬 Wind Speed: {wind_speed} km/h\n"
                f"☁ Condition: {condition}"
            )
        )

    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Something went wrong:\n{e}"
        )


# Main Window
root = tk.Tk()
root.title("Weather App")
root.geometry("500x450")
root.resizable(False, False)
root.configure(bg="#87CEEB")

# Heading
title = tk.Label(
    root,
    text="Weather Forecast App",
    font=("Arial", 22, "bold"),
    bg="#87CEEB",
    fg="navy"
)
title.pack(pady=20)

# Entry
city_entry = tk.Entry(
    root,
    font=("Arial", 14),
    width=30
)
city_entry.pack(pady=10)

# Button
search_button = tk.Button(
    root,
    text="Get Weather",
    font=("Arial", 12, "bold"),
    bg="navy",
    fg="white",
    command=get_weather
)
search_button.pack(pady=15)

# Result Label
result_label = tk.Label(
    root,
    text="Enter a city name and click Get Weather",
    font=("Arial", 12),
    justify="left",
    wraplength=450,
    bg="#87CEEB"
)
result_label.pack(pady=20)

# Footer
footer = tk.Label(
    root,
    text="Powered by Open-Meteo",
    bg="#87CEEB",
    font=("Arial", 9)
)
footer.pack(side="bottom", pady=10)

root.mainloop()