from inky import Inky_Impressions_7
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne

inky_display = Inky_Impressions_7(resolution=(800, 480))
inky_display.set_border(inky_display.WHITE)

img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT), inky_display.WHITE)
draw = ImageDraw.Draw(img)

font = ImageFont.truetype(FredokaOne, 36)

message = "Hello, World!"
_, _, w, h = font.getbbox(message)
x = (inky_display.WIDTH / 2) - (w / 2)
y = (inky_display.HEIGHT / 2) - (h / 2)

draw.text((x, y), message, inky_display.RED, font)
inky_display.set_image(img)
inky_display.show()
