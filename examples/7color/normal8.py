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

# Create a new image with the correct palette
img = Image.new("P", (200, 300), inky_display.WHITE )
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
font = ImageFont.truetype(FredokaOne, 36)
message = "Hello, World!"

# Use getbbox() correctly for newer Pillow versions
bbox = font.getbbox(message)
w = bbox[2] - bbox[0]
h = bbox[3] - bbox[1]

text_x = (inky_display.WIDTH / 2) - (w / 2)
text_y = 100  # Place text below the image

# Use color index instead of RGB
draw.text((text_x, text_y), message, fill=4, font=font)  # 4 is RED in Inky's palette

# Set the text image on the display
inky_display.set_image_at_position2(img, x_offset=0, y_offset=0)

# Show the image
inky_display.show()
