import os
import cv2

def load_images(folder_path):
    # Get all images except those starting with 'r'
    images = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.png')) and f.startswith('r')]
    return images

def get_new_filename(folder_path, digit):
    # Generate a new filename in the format "[digit]_i.jpg"
    base_name = f"{digit}"
    new_name = f"{base_name}.jpg"
    i = 1

    while os.path.exists(os.path.join(folder_path, new_name)):
        new_name = f"{base_name}_{i}.jpg"
        i += 1
    return new_name

def main(folder_path):
    images = load_images(folder_path)
    
    if not images:
        print("No images to process.")
        return

    for image_filename in images:
        image_path = os.path.join(folder_path, image_filename)
        
        # Load the image
        img = cv2.imread(image_path)
        
        # Display the image
        cv2.imshow('Image', img)

        # Wait for a digit key press
        key = cv2.waitKey(0)

        if key >= ord('0') and key <= ord('9'):  # Check if a digit key is pressed
            digit = chr(key)  # Convert to character
            new_name = get_new_filename(folder_path, digit)  # Get unique filename
            
            os.rename(image_path, os.path.join(folder_path, new_name))
            print(f'Renamed to: {new_name}')
        
        cv2.destroyAllWindows()  # Close the image window

# Example usage
folder_path = 'Test'  # Replace with your folder path
main(folder_path)
