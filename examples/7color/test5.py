from inky import Inky_Impressions_7
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne

# Initialize the display
inky_display = Inky_Impressions_7(resolution=(800, 480))
inky_display.set_border(inky_display.WHITE)

# Create a white background
img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT), inky_display.WHITE)

# Load the smaller image
small_image = Image.open("images/bulbasaur.jpg").convert("RGB")

# Resize the small image if needed (e.g., ensure it's 300x350)
small_image = small_image.resize((300, 350))

# Calculate position to center the small image on the background
x = (inky_display.WIDTH - small_image.width) // 2
y = (inky_display.HEIGHT - small_image.height) // 2

# Create a palette image to map the RGB image to the Inky display's palette
palette = inky_display._palette_blend(saturation=0.5)
palette_image = Image.new("P", (1, 1))
palette_image.putpalette(palette + [0, 0, 0] * 248)

# Convert the small image to the Inky display's palette
small_image_palettized = small_image.convert("RGB").convert("P", palette=palette_image)

# Paste the palettized small image onto the white background
img.paste(small_image_palettized, (x, y))

# Optionally draw additional elements like text
draw = ImageDraw.Draw(img)
font = ImageFont.truetype(FredokaOne, 36)
message = "Hello, World!"
_, _, w, h = font.getbbox(message)
text_x = (inky_display.WIDTH / 2) - (w / 2)
text_y = y + small_image.height + 10  # Place text below the image with 10px spacing
draw.text((text_x, text_y), message, inky_display.RED, font)

# Set the image with a saturation of 0.5 (you can adjust this)
inky_display.set_image(img, saturation=0.5)

# Display the final image
inky_display.show()
