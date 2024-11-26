import os
from PIL import Image, ImageEnhance

def adjust_lightness(path, value):
    """
    Adjusts the lightness of all image files in the specified path by the given value.

    Parameters:
    path (str): Path to the directory containing the images.
    value (float): Value to adjust the lightness by (-1.0 to 1.0).

    Returns:
    None
    """
    for filename in os.listdir(path):
        if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
            image_path = os.path.join(path, filename)
            try:
                image = Image.open(image_path)
                lightness_enhancer = ImageEnhance.Color(image)
                adjusted_image = lightness_enhancer.enhance(1 + value)
                adjusted_image.save(image_path)
                print(f"Adjusted lightness for {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

# Get the path and lightness value from the user
path = input("Enter the path to the image directory: ")
value = float(input("Enter the lightness adjustment value (-1.0 to 1.0): "))

# Adjust the lightness of all images in the directory
adjust_lightness(path, value)

print("Press Enter to close the program...")
input()