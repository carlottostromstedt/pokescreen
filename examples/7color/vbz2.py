from library import Inky as inky7
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne
import numpy
import time
import requests
import json
import time
from datetime import datetime

font_departures = ImageFont.load("vbz-font.pil")
font_date_time = ImageFont.truetype("Roboto-Bold.ttf", 18)

# Constants
MINUTES_TO_DEPARTURE_LIMIT = 4
stops = ["Stauffacher"]
running = True

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


def signal_handler(sig, frame):
    global running
    print("Stopping script...")
    running = False

def draw_scaled_bitmap_font(text, font, scale=2):
    # Create a temporary image
    small_img = Image.new("L", (200, 50), 255)
    draw = ImageDraw.Draw(small_img)
    draw.text((0, 0), text, font=font, fill=0)

    # Scale it up
    scaled_img = small_img.resize(
        (small_img.width * scale, small_img.height * scale), Image.NEAREST
    )
    return scaled_img

def draw_connections_on_display(epd, counter):
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
        
        print(connections_sorted)
        x = 10
        y = 200
        amount_displayed = 0
        should_sleep = False
        amount_to_sleep = 0

        for connection in connections_sorted:
            number = connection["number"] or "N"
            departure = get_departure_time(connection)
            destination = remove_zurich(connection["to"])
            minutes_to_departure = departure_to_minutes(departure)

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

        now = datetime.now()
        draw.text((190, 7), now.strftime("%H:%M"), font=font_date_time, fill=0)

        print("connections drawn")
        return should_sleep, amount_to_sleep

    except requests.exceptions.RequestException as err:
        logging.error("Connection error: %s", err)
        return False, 60

# Initialize the display
inky_display = inky7(resolution=(800, 480))

# Create a white background
inky_display.buf = numpy.ones((inky_display.rows, inky_display.cols), dtype=numpy.uint8) * 1

# Open a smaller image
small_image = Image.open("images/poke_card.png")

# Place the image 100 pixels from the left and 50 pixels from the top
inky_display.set_image_at_position2(small_image, x_offset=450, y_offset=20, width=320, height=440)

# Create a new image with the correct palette
img = Image.new("P", (300, 338), color=1)  # Fill with white (color index 1)
# Set up the palette to match Inky display
palette = [
    0, 0, 0,    # Black
    255, 255, 255,  # White
    0, 255, 0,  # Green
    0, 0, 255,  # Blue
    255, 0, 0,  # Red
    255, 255, 0,  # Yellow
    255, 140, 0,  # Orange
    255, 255, 255  # Clear/White
]
img.putpalette(palette + [0, 0, 0] * 248)

draw = ImageDraw.Draw(img)
font = ImageFont.truetype(FredokaOne, 24)
font_time = ImageFont.truetype(FredokaOne, 18)
message = "Hello, World!"
Time = time.strftime("%H : %M", time.localtime())
Date = time.strftime("%Y - %m - %d", time.localtime())


# Use getbbox() correctly for newer Pillow versions
bbox = font.getbbox(message)
w = bbox[2] - bbox[0]
h = bbox[3] - bbox[1]

text_x = 10
text_y = 100  # Place text below the image

# # Use color index instead of RGB
draw.text((text_x, text_y), Time, fill=0, font=font_date_time)  # 4 is RED in Inky's palette
draw.text((text_x, text_y - 50), Date, fill=0, font=font_date_time)  # 4 is RED in Inky's palette

draw_connections_on_display("x", 0)

scale = 2

scaled_img = img.resize(
        (img.width * scale, img.height * scale), Image.NEAREST
    )

# Set the text image on the display
inky_display.set_image_at_position2(scaled_img, width=400, height=450, x_offset=25, y_offset=0)

# Show the image
inky_display.show()

