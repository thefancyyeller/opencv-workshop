import cv2 # OpenCV
import numpy as np
from IPython.display import Image, display # Specific to Jupyter Notebook for showing the images
import os, re

# User Options
show_images = True # Disable if too many images
images_per_row = 3
displayDims = [200, 200] # Size of scaled image preview

# Assembles a list of image filepaths into 1 singular image
def stitch(filenames: list[str]):
    # Helper vars
    out = None # This is the actual image file being shown to user, a grid of existing images
    buffer = [] # Holds a singular row of image data so we may accumulate multiple before assembling our row.

    # Open, resize, and merge all images
    for index, fname in enumerate(imFiles): # Open and scale the images
        scaled = cv2.imread(f"./images/{fname}")
        if scaled is not None: # Skip files OpenCV can't read
            buffer.append(cv2.resize(scaled, displayDims))
        # Add buffer to output image
        if buffer and (len(buffer) == images_per_row or index == (len(imFiles)-1)):
            while len(buffer) < images_per_row: # Pad the last row with blanks so widths match
                buffer.append(np.zeros_like(buffer[0]))
            row = cv2.hconcat(buffer)
            if out is None:
                out = row
            else:
                out = cv2.vconcat([out, row])
            buffer = []
    return out

# List the found image files to the user
imFiles = [x.name for x in os.scandir('images') if x.is_file() and re.match(".*\\.(jpe?g|png|webp|bmp)", x.name)]
print("Files found:")
for i in imFiles:
    print (i)

# Display the images in this notebook
out = stitch(imFiles)
# Display our assembled file if user allows and we actually have an image to show
if show_images and out is not None:
    ok, encoded = cv2.imencode('.png', out)
    display(Image(data=encoded.tobytes()))


