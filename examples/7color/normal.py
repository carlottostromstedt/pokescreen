from library import Inky as inky7
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne

# Initialize the display
inky_display = inky7(resolution=(800, 480))

# Open a smaller image
small_image = Image.open("images/bulbasaur.jpg")

# Place the image 100 pixels from the left and 50 pixels from the top
inky_display.place_image(small_image, 100, 50)

# Show the image
inky_display.show()
