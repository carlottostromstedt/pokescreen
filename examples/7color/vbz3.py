import asyncio
import signal
import logging
from library import Inky as inky7
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne
import numpy
import time
import requests
import json
from datetime import datetime, timedelta

# Fonts
font_departures = ImageFont.load("vbz-font.pil")
font_date = ImageFont.truetype("Roboto-Bold.ttf", 18)
font_time = ImageFont.truetype("Roboto-Bold.ttf", 16)
font_weather = ImageFont.truetype("Roboto-Bold.ttf", 16)

# Constants
MINUTES_TO_DEPARTURE_LIMIT = 4
stops = ["Stauffacher"]
running = True

# Weather API (https://openweathermap.org — free tier is sufficient)
OPENWEATHER_API_KEY = "YOUR_API_KEY_HERE"
WEATHER_LAT = 47.3769  # Zürich
WEATHER_LON = 8.5417

def get_weather():
    """Fetch current weather + today's high/low from OpenWeatherMap.
    Returns (temp, temp_high, temp_low, description, weather_id, wind_speed) or all-None tuple on error."""
    try:
        current_url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?lat={WEATHER_LAT}&lon={WEATHER_LON}"
            f"&appid={OPENWEATHER_API_KEY}&units=metric"
        )
        current_resp = requests.get(current_url, timeout=10)
        current_resp.raise_for_status()
        current = current_resp.json()
        temp = round(current["main"]["temp"])
        description = current["weather"][0]["description"].capitalize()
        weather_id = current["weather"][0]["id"]
        wind_speed = current.get("wind", {}).get("speed", 0)  # m/s

        forecast_url = (
            f"https://api.openweathermap.org/data/2.5/forecast"
            f"?lat={WEATHER_LAT}&lon={WEATHER_LON}"
            f"&appid={OPENWEATHER_API_KEY}&units=metric&cnt=16"
        )
        forecast_resp = requests.get(forecast_url, timeout=10)
        forecast_resp.raise_for_status()
        forecast = forecast_resp.json()

        today = datetime.now().strftime("%Y-%m-%d")
        today_temps = [e["main"]["temp"] for e in forecast["list"] if e["dt_txt"].startswith(today)]
        if not today_temps:
            today_temps = [temp]
        temp_high = round(max(today_temps))
        temp_low = round(min(today_temps))

        return temp, temp_high, temp_low, description, weather_id, wind_speed
    except requests.exceptions.RequestException as err:
        logging.error("Weather error: %s", err)
        return None, None, None, None, None, None


def get_clothing_recommendation(temp, temp_low, weather_id, wind_speed):
    """Returns 1–2 short clothing recommendation strings based on weather conditions."""
    is_rain = 200 <= weather_id < 600   # thunderstorm, drizzle, rain
    is_snow = 600 <= weather_id < 700
    is_windy = wind_speed >= 6          # ~22 km/h

    # Main outer layer
    if temp < 0:
        layer = "Heavy winter jacket"
    elif temp < 8:
        layer = "Winter jacket"
    elif temp < 14:
        layer = "Light jacket"
    elif temp < 19:
        layer = "Hoodie / cardigan"
    else:
        layer = "T-shirt"

    # Precipitation modifier
    if is_snow:
        layer += " + boots"
    elif is_rain and temp >= 14:
        layer = "Rain jacket"
    elif is_rain:
        layer += " + umbrella"

    # Accessories: gloves/hat and scarf
    acc = ""
    if temp < 5:
        acc = "Gloves & winter hat"
    elif temp < 10:
        acc = "Consider gloves & hat"

    if is_windy and temp < 15:
        acc = (acc + " + scarf") if acc else "Scarf (it's windy!)"

    return [layer, acc] if acc else [layer]

def departure_to_minutes(departure_time):
    departure_datetime = datetime.strptime(departure_time, "%Y-%m-%dT%H:%M:%S%z")
    current_datetime = datetime.now(departure_datetime.tzinfo)
    time_difference = (departure_datetime - current_datetime).total_seconds() / 60
    return max(round(time_difference), 0)

def remove_zurich(input_string):
    if "Zürich" in input_string:
        zurich_index = input_string.find("Zürich")
        return input_string[:zurich_index].strip(",") + input_string[zurich_index + 6:].lstrip(",")
    return input_string

def get_departure_time(connection):
    prognosis = connection["stop"]["prognosis"]["departure"]
    return prognosis if prognosis else connection["stop"]["departure"]

def draw_connections(draw):
    print("now drawing connections")
    try:
        connections = []
        for stop in stops:
            URL = f"http://transport.opendata.ch/v1/stationboard?station={stop}&limit=15"
            response = requests.get(URL)
            response.raise_for_status()
            data = json.loads(response.text)
            connections.extend(data["stationboard"])

        connections_sorted = sorted(connections, key=lambda x: get_departure_time(x))

        x = 10
        y = 200
        amount_displayed = 0
        should_sleep = False
        amount_to_sleep = 0

        for connection in connections_sorted:
            number = connection["number"] or "N"
            departure = get_departure_time(connection)
            destination = remove_zurich(connection["to"])
            minutes_to_departure = departure_to_minutes(departure) - 1

            if minutes_to_departure > MINUTES_TO_DEPARTURE_LIMIT and amount_displayed < 5:
                draw.text((x, y), f"{number}", font=font_departures, fill=0)
                offset = 24 if "N" in number else 15
                draw.text((x + offset, y), destination, font=font_departures, fill=0)
                draw.text((230, y), f"{minutes_to_departure}'", font=font_departures, fill=0)
                y += 24
                amount_displayed += 1

            if minutes_to_departure > 40 and amount_displayed < 5:
                should_sleep = True
                amount_to_sleep = (minutes_to_departure - 1) * 60

        # now = datetime.now()
        # draw.text((190, 7), now.strftime("%H:%M"), font=font_date_time, fill=0)

        print("connections drawn")
        return should_sleep, amount_to_sleep

    except requests.exceptions.RequestException as err:
        logging.error("Connection error: %s", err)
        return False, 60

def should_pause_for_night():
    """Returns True if the current time is between 23:00 and 06:00."""
    hour = datetime.now().hour
    return hour >= 22 or hour < 5

def update_display():
    # Create display and reset
    inky_display = inky7(resolution=(800, 480))
    inky_display.buf = numpy.ones((inky_display.rows, inky_display.cols), dtype=numpy.uint8) * 1

    # Draw text + connections
    img = Image.new("P", (300, 338), color=1)
    palette = [
        0, 0, 0, 255, 255, 255, 0, 255, 0, 0, 0, 255,
        255, 0, 0, 255, 255, 0, 255, 140, 0, 255, 255, 255
    ]
    img.putpalette(palette + [0, 0, 0] * 248)
    draw = ImageDraw.Draw(img)

    # Add time & date

    now = datetime.now()
    adjusted_time = now + timedelta(hours=1, minutes=1)
    Time = adjusted_time.strftime("%H : %M")
    Date = time.strftime("%Y - %m - %d", time.localtime())
    draw.text((10, 50), Date, fill=0, font=font_date)
    draw.text((10, 80), Time, fill=0, font=font_time)

    # Add weather
    temp, temp_high, temp_low, description, weather_id, wind_speed = get_weather()
    if temp is not None:
        draw.text((10, 110), f"{temp}\u00b0C  {description}", fill=0, font=font_weather)
        draw.text((10, 135), f"H: {temp_high}\u00b0  L: {temp_low}\u00b0", fill=0, font=font_weather)
        outfit = get_clothing_recommendation(temp, temp_low, weather_id, wind_speed)
        for i, line in enumerate(outfit):
            draw.text((10, 160 + i * 20), line, fill=0, font=font_weather)

    # Add departures
    should_sleep, amount_to_sleep = draw_connections(draw)

    # Add image
    small_image = Image.open("images/poke_card.png")
    inky_display.set_image_at_position2(small_image, x_offset=450, y_offset=20, width=320, height=440)

    # Scale and position info
    scale = 2
    scaled_img = img.resize((img.width * scale, img.height * scale), Image.NEAREST)
    inky_display.set_image_at_position2(scaled_img, width=400, height=450, x_offset=25, y_offset=0)

    inky_display.show()

    return should_sleep, amount_to_sleep

# Attach Ctrl+C signal
def signal_handler(sig, frame):
    global running
    print("\n🛑 Exiting loop...")
    running = False

signal.signal(signal.SIGINT, signal_handler)

# Loop until Ctrl+C
print("🔁 Starting display refresh loop (Ctrl+C to exit)")
while running:
    if should_pause_for_night():
        print("⏸ Pausing until 6am...")
        # Sleep until the top of the next hour or just for 10 minutes
        time.sleep(600)
        continue

    should_sleep, sleep_seconds = update_display()
    delay = sleep_seconds if should_sleep else 60
    print(f"⏱️ Next refresh in {delay} seconds\n")
    time.sleep(delay)

print("✅ Display loop stopped.")
