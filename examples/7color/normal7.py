from library import Inky as inky7
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne
import numpy

# Initialize the display
inky_display = inky7(resolution=(800, 480))

# Create a white background
inky_display.buf = numpy.ones((inky_display.rows, inky_display.cols), dtype=numpy.uint8) * 1

# Open a smaller image
small_image = Image.open("images/bulbasaur.jpg")

# Place the image 100 pixels from the left and 50 pixels from the top
inky_display.set_image_at_position2(small_image, x_offset=100, y_offset=50)

img = Image.new("P", (200, 300), inky_display.WHITE)

draw = ImageDraw.Draw(img)
font = ImageFont.truetype(FredokaOne, 36)
message = "Hello, World!"
_, _, w, h = font.getbbox(message)
text_x = (inky_display.WIDTH / 2) - (w / 2)
text_y = 100  # Place text below the image with 10px spacing
draw.text((text_x, text_y), message, inky_display.RED, font)

# Set the text image on the display
inky_display.set_image_at_position2(img, x_offset=300, y_offset=0)

# Show the image
inky_display.show()
