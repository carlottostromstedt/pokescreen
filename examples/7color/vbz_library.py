import time

def departure_to_minutes(departure_time):
    # Parse the departure time string to a datetime object
    departure_datetime = datetime.strptime(departure_time, "%Y-%m-%dT%H:%M:%S%z")

    # Get the current time
    current_datetime = datetime.now(departure_datetime.tzinfo)

    # Calculate the time difference in minutes
    time_difference = (departure_datetime - current_datetime).total_seconds() / 60

    # Round the time difference to the nearest minute
    rounded_time_difference = round(time_difference)

    # Return the rounded time difference if greater than 0, otherwise return the character representing the tram
    if rounded_time_difference > 0:
        return rounded_time_difference
    else:
        return 0
        # return chr(30)  # Character representing the tram picture

def remove_zurich(input_string):
    if "Zürich" in input_string:
        # Find the index of "Zürich" in the string
        zurich_index = input_string.find("Zürich")

        # Remove "Zürich" and any following comma
        result = input_string[:zurich_index].strip(",") + input_string[zurich_index + 6:].lstrip(",")

        return result
    else:
        return input_string

def get_departure_time(connection):
    prognosis = connection["stop"]["prognosis"]["departure"]
    if prognosis is not None:
        return prognosis
    else:
        return connection["stop"]["departure"]


def fetch_and_display_connections(epd, draw, counter, weather_counter, temperature, weather_description, temperature_max, temperature_min):
  should_sleep = False
  amount_to_sleep = 0
  try:
    logging.info("Fetching connections from API...")
    connections = ""
    stop_index = 0

    for stop in stops:
      URL = f"http://transport.opendata.ch/v1/stationboard?station={stop}&limit=15"
      response = requests.get(URL)
      response.raise_for_status()  # Raise an exception for non-200 status codes
      data = json.loads(response.text)
      if stop_index == 0:
        connections = data["stationboard"]
      else:
        connections.extend(data["stationboard"])
      stop_index += 1

    connections_sorted = sorted(connections, key=lambda x: get_departure_time(x))  

    x = 10
    y = 12

    amount_displayed = 0


    # Iterate over connections to draw text on the blank image
    for connection in connections_sorted:
        number = connection["number"]
        departure = connection["stop"]["prognosis"]["departure"]
        destination = connection["to"]
        destination = remove_zurich(destination)

        if number == None:
            number = "N"

        if departure != None:
            minutes_to_departure = departure_to_minutes(departure)
        else:
            minutes_to_departure = departure_to_minutes(connection["stop"]["departure"])

        # Draw text on the blank image
        if int(minutes_to_departure) > MINUTES_TO_DEPARTURE_LIMIT and amount_displayed < 5:
            minutes_to_departure_string = str(minutes_to_departure) + "'"
            text_draw.text((x, y), f"{number}", font=font, fill=0)
            if "N" in number: 
              text_draw.text(((x + 24), y), f"{destination}", font=font, fill=0) # Black text
            else: 
              text_draw.text(((x + 15), y), f"{destination}", font=font, fill=0) # Black text
            text_draw.text((170, y), f"{minutes_to_departure_string}", font=font, fill=0)  # Black text
            y = y + 24
            amount_displayed += 1

        if int(minutes_to_departure) > 40 and amount_displayed < 5:
            should_sleep = True
            amount_to_sleep = (int(minutes_to_departure) - 1) * 60

    current_hour = datetime.now().strftime("%H") 
    current_minutes = datetime.now().strftime("%M")

    text_draw.text((190, 7), f"{current_hour}:{str(current_minutes)}", font=font_time, fill=0)

    if counter > 0:
        epd.display_Partial_Wait(epd.getbuffer(image))
        logging.info("Displaying partial")
    else:
        epd.display_Base(epd.getbuffer(image))
        logging.info("Displaying Base")# Update screen

    logging.info("All lines displayed simultaneously")

  except requests.exceptions.RequestException as err:
    logging.error("Error fetching data:", err)

  logging.info("Waiting for next update...")
  return should_sleep, amount_to_sleep
