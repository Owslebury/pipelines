import cv2
import os
from PIL import Image
import json

def block_average_png_to_json(input_folder, output_folder, hs, ws):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Iterate through each PNG file in the input folder
    for filename in os.listdir(input_folder):
        print(filename)
        if filename.endswith(".png"):
            # Read the PNG image
            img_path = os.path.join(input_folder, filename)
            img = cv2.imread(img_path)

            # Resize image using block averaging
            resized = cv2.resize(img, (ws, hs), interpolation=cv2.INTER_AREA)

            # Save the resized image to the output folder
            output_img_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_img_path, resized)

            # Convert the resized image to a PIL image for pixel extraction
            pil_image = Image.fromarray(resized)

            # Get image dimensions
            width, height = pil_image.size

            # Initialize an empty list to store pixel data
            pixels = []

            # Iterate through each pixel in the image
            for y in range(height):
                for x in range(width):
                    # Get the RGB values of the pixel
                    r, g, b = pil_image.getpixel((x, y))

                    # Append the RGB values to the list
                    pixels.append((r, g, b))

            # Write the pixel data to a JSON file
            json_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".json")
            with open(json_path, 'w') as json_file:
                json.dump(pixels, json_file)

def greyscale(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # List all files in the input folder
    files = os.listdir(input_folder)

    # Iterate over each file
    for file in files:
        # Check if the file is a PNG
        if file.lower().endswith('.png'):
            # Open the image
            image_path = os.path.join(input_folder, file)
            with Image.open(image_path) as img:
                # Convert the image to grayscale
                gray_img = img.convert('L')

                # Save the grayscale image to the output folder
                output_path = os.path.join(output_folder, file)
                gray_img.save(output_path)

                print(f"Converted {file} to grayscale.")


def replaceColour(input_image_path, output_image_path):
    # Open an image file
    with Image.open(input_image_path) as img:
        # Convert image to RGBA (if not already in RGBA)
        img = img.convert("RGBA")
        # Get the data of the image
        data = img.getdata()
        
        # Define the target color and the replacement color
        target_color = (41, 255, 168, 255)  # #29ffa8
        replacement_color = (255, 192, 203, 255)  # Pink
        
        # Create a new data list with the modified colors
        new_data = []
        for item in data:
            if item == target_color:
                new_data.append(replacement_color)
            else:
                new_data.append(item)
        
        # Update image data with the new data
        img.putdata(new_data)
        
        # Save the modified image
        img.save(output_image_path)
        print(f"Image saved to {output_image_path}")

# Example usage
input_image_path = 'input_image.png'  # Replace with your input image path
output_image_path = 'output_image.png'  # Replace with your desired output image path

change_pixel_color(input_image_path, output_image_path)
