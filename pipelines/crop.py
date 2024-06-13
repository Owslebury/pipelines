import cv2
import os


def crop_image(image_path, folderA, folderB):
    # Step 1: Read the image
    image = cv2.imread(image_path)

    if image is None:
        print(f"Error: Unable to read image from {image_path}. Make sure the file exists and the path is correct.")
        exit()

    # Step 2: Use selectROI to get the ROI
    roi = cv2.selectROI("Select Region", image, fromCenter=False, showCrosshair=True)

    # The roi variable is a tuple of (x, y, w, h)
    x, y, w, h = roi

    # Check if the ROI is valid
    if w == 0 or h == 0:
        print("Error: Invalid ROI. Please select a valid region.")
        exit()

    # Step 3: Crop the image using the ROI coordinates
    cropped_image = image[y:y+h, x:x+w]

    # Step 4: Display the cropped image
    cv2.imshow('Cropped Image', cropped_image)

    # Step 5: Wait for the Enter key to save the image and print coordinates
    print("Press Enter to save the image and print coordinates...")
    key = cv2.waitKey(0)

    if key == 13:  # 13 is the Enter key
        save_path = 'cropped_image.png'
    
        # Save the cropped image in the current directory with the name 'cropped_image.png'
        success = cv2.imwrite(save_path, cropped_image)
    
        if success:
            print(f"Cropped image successfully saved to {save_path}")
            print(f"Coordinates: x={x}, y={y}, width={w}, height={h}")
            crop_and_save_images(folderA, "croppedA", x, y, w, h)
            crop_and_save_images(folderB, "croppedB", x, y, w, h)
            print("Saved to croppedA and croppedB folders")
        else:
            print(f"Error: Failed to save the cropped image to {save_path}")

    # Close all windows
    cv2.destroyAllWindows()

    ##x=217, y=205, width=53, height=43


def crop_and_save_images(source, destination, x, y, w, h):
    # List all files in the source directory
    for filename in os.listdir(source):
        if filename.endswith('.png'):
            # Read the image
            image_path = os.path.join(source, filename)
            image = cv2.imread(image_path)
            
            if image is None:
                print(f"Error: Unable to read image {image_path}. Skipping.")
                continue
            
            # Crop the image
            cropped_image = image[y:y+h, x:x+w]
            
            # Define the path for the cropped image
            cropped_image_path = os.path.join(destination, filename)
            
            # Save the cropped image
            success = cv2.imwrite(cropped_image_path, cropped_image)
            
            if success:
                print(f"Cropped image saved to {cropped_image_path}")
            else:
                print(f"Error: Failed to save cropped image {cropped_image_path}")