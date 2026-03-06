import time
import logging
import requests
import json
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import signal
import sys
from font_fredoka_one import FredokaOne
from library import Inky as inky7

# Global font setup (customize path/font)
font = ImageFont.truetype(FredokaOne, 24)
font_time = ImageFont.truetype(FredokaOne, 18)

# Constants
MINUTES_TO_DEPARTURE_LIMIT = 1
stops = ["Zürich, Hauptbahnhof", "Zürich, Central"]  # your real stop names
image = Image.new("P", (400, 450), color=1)  # 1 = white
text_draw = ImageDraw.Draw(image)

# Flag to control loop exit
running = True


def signal_handler(sig, frame):
    global running
    print("Stopping script...")
    running = False


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


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


def draw_connections_on_display(epd, counter):
    image.paste(1, [0, 0, image.size[0], image.size[1]])  # Clear to white
    global text_draw
    text_draw = ImageDraw.Draw(image)

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
        y = 12
        amount_displayed = 0
        should_sleep = False
        amount_to_sleep = 0

        for connection in connections_sorted:
            number = connection["number"] or "N"
            departure = get_departure_time(connection)
            destination = remove_zurich(connection["to"])
            minutes_to_departure = departure_to_minutes(departure)

            if minutes_to_departure > MINUTES_TO_DEPARTURE_LIMIT and amount_displayed < 5:
                text_draw.text((x, y), f"{number}", font=font, fill=0)
                offset = 24 if "N" in number else 15
                text_draw.text((x + offset, y), destination, font=font, fill=0)
                text_draw.text((170, y), f"{minutes_to_departure}'", font=font, fill=0)
                y += 24
                amount_displayed += 1

            if minutes_to_departure > 40 and amount_displayed < 5:
                should_sleep = True
                amount_to_sleep = (minutes_to_departure - 1) * 60

        now = datetime.now()
        text_draw.text((190, 7), now.strftime("%H:%M"), font=font_time, fill=0)

        if counter > 0:
            epd.display_Partial_Wait(epd.getbuffer(image))
        else:
            epd.display_Base(epd.getbuffer(image))

        logging.info("Display updated.")
        return should_sleep, amount_to_sleep

    except requests.exceptions.RequestException as err:
        logging.error("Connection error: %s", err)
        return False, 60


def run_loop(epd):
    counter = 0
    while running:
        logging.info("Refreshing screen...")
        should_sleep, delay = draw_connections_on_display(epd, counter)
        counter += 1
        time.sleep(delay if should_sleep else 60)

    print("Loop exited. Bye!")

epd = inky7(resolution=(800, 480))
run_loop(epd)
