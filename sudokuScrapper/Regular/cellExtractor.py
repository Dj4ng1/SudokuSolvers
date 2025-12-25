#This is to extract the cells from solutions grids of regular sudoku for training.
#Tried different OCR, but none of them managed properly

import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
from datetime import datetime, timedelta
import cv2
from PIL import Image

# Get the sudoku from killersudokuonline archiges
BASE_URL = "https://www.killersudokuonline.com/archives"

# Pick some dates to get the dailies. Easier to use datetime and format
START_DATE = datetime(2020, 1, 1)
END_DATE = datetime(2020, 1, 20)

# Put the solved and unsolved versions in 2 different folders
GRID_FOLDER = "Grid_GT"
TRAINING_FOLDER = "Training-GT"


# Create the folders if they don't exist
os.makedirs(GRID_FOLDER, exist_ok=True)
os.makedirs(TRAINING_FOLDER, exist_ok=True)


# Counters for different sections (killersudoku, GreaterThansudoku and Regularsudoku
k_count = 1
gt_count = 1
r_count = 1

def convert_jpg_to_png(folder_path):
    # Create a directory for PNG files if it doesn't exist
    png_folder = os.path.join(folder_path, 'converted_png')
    os.makedirs(png_folder, exist_ok=True)


# Function to locate the images 
def locate_images(url):
    global k_count, gt_count, r_count
    response = requests.get(url) #go to the url
    soup = BeautifulSoup(response.text, 'html.parser')

    # Check different sections for images
    sections = ['kdaily', 'gtdaily', 'rdaily']

    for section in sections:
        anchor = soup.find('a', attrs={'name': section}) #Only way to find the solutions is through the text in the <a> section
        
            # Download the first image in each section (correspond to the sudoku grid)
        img_tag = anchor.find_next('img')
        
        if anchor:
            # Download the "Solution" image
            solution_link = anchor.find('a', string="Solution")
            if solution_link and 'href' in solution_link.attrs:
                solution_image_url = urljoin(url, solution_link['href'])
                if section == 'gtdaily':
                    prefix = 'gt_solved_' #This part is important. Replace with the type of sudoku you wish to download
                    download_image(solution_image_url, GRID_FOLDER, f"{prefix}{r_count}.jpg") 
                    r_count += 1
    print(f"No images found on: {url}")

# Function to download an image
def download_image(image_url, folder, filename):
    try:
        img_data = requests.get(image_url).content
        img_name = os.path.join(folder, filename)  # Full path to the folder

        with open(img_name, 'wb') as img_file:
            img_file.write(img_data)

        print(f"Downloaded: {img_name}")
    except Exception as e:
        print(f"Failed to download {image_url}: {e}")


def preprocess_image(img):
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian Blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply adaptive thresholding
    binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 2)
    
    return binary

def process_sudoku_image(image_path, save_dir):
    print(f"Loading image from: {image_path}")
    
    img = cv2.imread(image_path)

    # Check if the image is loaded
    if img is None:
        raise FileNotFoundError(f"Could not open or find the image at {image_path}")

    print("Image loaded successfully.")
    
    # Crop the image: Remove 16 pixels from the top and 20 pixels from the bottom
    img = img[16:img.shape[0]-20, :]  
    
    # Preprocess the cropped image
    binary = preprocess_image(img)

    cell_size = binary.shape[0] // 9  # Assuming the image is 9x9 cells
    for i in range(9):
        for j in range(9):
            # Extract the cell from the image
            cell = img[i * cell_size:(i + 1) * cell_size, j * cell_size:(j + 1) * cell_size]

            # Save the cell as a JPEG file. Name doesn't matter since we will label it again after
            cell_filename = os.path.join(save_dir, f'{os.path.basename(image_path)}_cell_{i}_{j}.jpg')  # Filename format
            cv2.imwrite(cell_filename, cell)  # Save the cell image

    print(f'Processed {image_path} and saved cells in {save_dir}')





def process_images_in_folder(folder_path, save_dir):
    convert_jpg_to_png(folder_path)
    # Create the directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # List image files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(('.jpg', '.jpeg', 'png')):  # Make sure it is not gif
            image_path = os.path.join(folder_path, filename)
            try:
                process_sudoku_image(image_path, save_dir)
            except Exception as e:
                print(e)


# Loop through the date range and scrape images
# current_date = START_DATE
# while current_date <= END_DATE:
#     date_str = current_date.strftime("%Y/%m/%d") #Easier to do it this way
#     url = f"{BASE_URL}/{date_str}"
#     print(f"Processing: {url}") #Not really useful since in linear time 
#     locate_images(url)
#     current_date += timedelta(days=1)

current_date = START_DATE
while current_date <= END_DATE:
    current_date = START_DATE
    date_str = current_date.strftime("%Y/%m/%d") #Easier to do it this way
    url = f"{BASE_URL}/{date_str}"
    print(f"Processing: {url}") #Not really useful since in linear time 
    locate_images(url)
    process_images_in_folder(GRID_FOLDER,TRAINING_FOLDER)