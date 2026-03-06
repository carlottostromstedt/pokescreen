from library import Inky as inky7
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne
import numpy

# Initialize the display
inky_display = inky7(resolution=(800, 480))

# Create a white background
inky_display.buf = numpy.ones((inky_display.rows, inky_display.cols), dtype=numpy.uint8) * 1  # 1 represents white in the Inky color palette

# Open a smaller image
small_image = Image.open("images/bulbasaur.jpg")

# Place the image 100 pixels from the left and 50 pixels from the top
inky_display.set_image_at_position2(small_image, x_offset=100, y_offset=50)

# Show the image
inky_display.show()
