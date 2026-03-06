from PIL import Image

# Initialize Inky display
inky = Inky()

# Create a smaller image (e.g., 300x350)
small_image = Image.new("P", (300, 350), Inky.RED)  # Create a red box
draw = ImageDraw.Draw(small_image)
draw.rectangle((50, 50, 250, 300), fill=Inky.BLUE)  # Draw a blue rectangle

# Draw the smaller image on the Inky screen, centered
inky.draw_sub_image(small_image, align_center=True)

# Show the result
inky.show()
