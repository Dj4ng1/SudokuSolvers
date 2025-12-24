import os
import cv2

def load_images(folder_path):
    # Get all images except those starting with 'r'
    images = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.png'))]
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

        key_presses = []


        while len(key_presses) < 4:
            # Wait for a key press
            key = cv2.waitKey(0)

            # Check if the key pressed is a digit key (0-9)
            gt_char = chr(key)  # Convert the key to its character representation
            key_presses.append(gt_char)  # Add the character to the list
            print(f'Key pressed: {gt_char}')

        # Generate a string from the collected key presses
        gt_string = ''.join(key_presses)
        print(f'Collected chars: {gt_string}')

        new_name = get_new_filename(folder_path, gt_string)  # Get unique filename
            
        os.rename(image_path, os.path.join(folder_path, new_name))
        print(f'Renamed to: {new_name}')
        
        cv2.destroyAllWindows()  # Close the image window

folder_path = 'Training_GT_Greater'  
main(folder_path)
