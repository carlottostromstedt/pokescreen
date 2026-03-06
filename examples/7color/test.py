#!/usr/bin/env python3

import argparse
import pathlib
import sys

from PIL import Image, ImageDraw
from inky.auto import auto

# Initialize Inky display
inky = auto(ask_user=True, verbose=True)

# Set up argument parser
parser = argparse.ArgumentParser(description="Display an image on an Inky e-Ink screen.")
parser.add_argument("--saturation", "-s", type=float, default=0.5, help="Colour palette saturation (default: 0.5)")
parser.add_argument("--file", "-f", type=pathlib.Path, required=True, help="Path to the image file to display")

# Parse arguments
args = parser.parse_args()

# Validate input
saturation = args.saturation
image_path = args.file

if not image_path.exists():
    print(f"Error: File not found at {image_path}")
    sys.exit(1)

# Create a smaller image (e.g., 300x350)
small_image = Image.new("P", (300, 350), inky.RED)  # Create a red box
draw = ImageDraw.Draw(small_image)
draw.rectangle((50, 50, 250, 300), fill=inky.BLUE)  # Draw a blue rectangle

# Draw the smaller image on the Inky screen, centered
inky.draw_sub_image(small_image, align_center=True)

# Show the result
inky.show()
