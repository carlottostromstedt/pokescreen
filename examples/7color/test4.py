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

# Define the saturated palette
SATURATED_PALETTE = [
    (0, 0, 0),        # Black
    (217, 242, 255),  # White
    (3, 124, 76),     # Green
    (27, 46, 198),    # Blue
    (245, 80, 34),    # Red
    (255, 255, 68),   # Yellow
    (239, 121, 44),   # Orange
    (255, 255, 255)   # Clear
]

# Convert palette to a flattened list of RGB values
palette_flat = [val for color in SATURATED_PALETTE for val in color]

# Apply the palette to the small image
small_image = small_image.quantize(palette=Image.new("P", (1, 1)), colors=len(SATURATED_PALETTE))
small_image.putpalette(palette_flat)

# Calculate position to center the small image on the background
x = (inky_display.WIDTH - small_image.width) // 2
y = (inky_display.HEIGHT - small_image.height) // 2

# Paste the small image onto the white background
img.paste(small_image, (x, y))

# Optionally draw additional elements like text
draw = ImageDraw.Draw(img)
font = ImageFont.truetype(FredokaOne, 36)
message = "Hello, World!"
_, _, w, h = font.getbbox(message)
text_x = (inky_display.WIDTH / 2) - (w / 2)
text_y = y + small_image.height + 10  # Place text below the image with 10px spacing
draw.text((text_x, text_y), message, inky_display.RED, font)

# Display the final image
inky_display.set_image(img)
inky_display.show()
