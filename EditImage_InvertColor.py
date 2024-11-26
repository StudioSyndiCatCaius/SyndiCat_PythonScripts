import os
from PIL import Image, ImageOps

def invert_colors(path):
    """
    Inverts the colors of all image files in the specified path, preserving transparency.

    Parameters:
    path (str): Path to the directory containing the images.

    Returns:
    None
    """
    for filename in os.listdir(path):
        if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
            image_path = os.path.join(path, filename)
            try:
                image = Image.open(image_path)
                # Create a new image with the same size and mode as the original
                inverted_image = Image.new(image.mode, image.size)
                
                # Invert the colors, preserving transparency
                pixels = list(image.getdata())
                inverted_pixels = [(255 - r, 255 - g, 255 - b, a) if len(pixel) == 4 else (255 - r, 255 - g, 255 - b) for r, g, b, *a in pixels]
                inverted_image.putdata(inverted_pixels)

                inverted_image.save(image_path)
                print(f"Inverted colors for {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

# Get the path from the user
path = input("Enter the path to the image directory: ")

# Invert the colors of all images in the directory
invert_colors(path)

print("Press Enter to close the program...")
input()