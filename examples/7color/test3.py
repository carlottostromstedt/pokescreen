from inky import Inky_Impressions_7
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne

# Define palettes
DESATURATED_PALETTE = [
    [0, 0, 0],        # Black
    [255, 255, 255],  # White
    [0, 255, 0],      # Green
    [0, 0, 255],      # Blue
    [255, 0, 0],      # Red
    [255, 255, 0],    # Yellow
    [255, 140, 0],    # Orange
    [255, 255, 255]   # Clear
]

SATURATED_PALETTE = [
    [0, 0, 0],        # Black
    [217, 242, 255],  # White
    [3, 124, 76],     # Green
    [27, 46, 198],    # Blue
    [245, 80, 34],    # Red
    [255, 255, 68],   # Yellow
    [239, 121, 44],   # Orange
    [255, 255, 255]   # Clear
]

# Blend palettes
def palette_blend(saturation, dtype="uint8"):
    saturation = float(saturation)
    palette = []
    for i in range(7):
        rs, gs, bs = [c * saturation for c in SATURATED_PALETTE[i]]
        rd, gd, bd = [c * (1.0 - saturation) for c in DESATURATED_PALETTE[i]]
        if dtype == "uint8":
            palette += [int(rs + rd), int(gs + gd), int(bs + bd)]
    palette += [255, 255, 255]  # Add clear color
    return palette

# Initialize display
inky_display = Inky_Impressions_7(resolution=(800, 480))
inky_display.set_border(inky_display.WHITE)

# Create a white background
img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT), inky_display.WHITE)

# Create blended palette
palette = palette_blend(0.5)
palette += [0, 0, 0] * 248  # Pad to 256 colors

# Load and process smaller image
small_image = Image.open("images/bulbasaur.jpg").convert("RGB")
palette_image = Image.new("P", (1, 1))
palette_image.putpalette(palette)

small_image = small_image.quantize(palette=palette_image)

# Resize the small image to fit (e.g., 300x350)
small_image = small_image.resize((300, 350))

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
