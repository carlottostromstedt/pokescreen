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

# Create a PIL Image to draw text
img = Image.new("P", (800, 480))
draw = ImageDraw.Draw(img)

# Load a font (Fredoka One from the imported module)
font = ImageFont.truetype(FredokaOne, 40)

# Draw text (black color)
draw.text((50, 20), "Hello, World!", font=font, fill=0)

# Set the text image on the display
inky_display.set_image_at_position2(img, x_offset=0, y_offset=0)

# Show the image
inky_display.show()
