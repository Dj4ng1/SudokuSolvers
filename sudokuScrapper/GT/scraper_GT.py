import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
from datetime import datetime, timedelta

# Get the sudoku from killersudokuonline archiges
BASE_URL = "https://www.killersudokuonline.com/archives"

# Pick some dates to get the dailies. Easier to use datetime and format
START_DATE = datetime(2020, 1, 1)
END_DATE = datetime(2022, 1, 10)

# Put the solved and unsolved versions in 2 different folders
UNSOLVED_FOLDER = "Unsolved_GT"
SOLVED_FOLDER = "Solved_GT"

# Create the folders if they don't exist
os.makedirs(UNSOLVED_FOLDER, exist_ok=True)
os.makedirs(SOLVED_FOLDER, exist_ok=True)

# Counters for section GreaterThansudoku 
gt_count = 1

# Function to locate the images 
def locate_images(url):
    global k_count, gt_count, r_count
    response = requests.get(url) #go to the url
    soup = BeautifulSoup(response.text, 'html.parser')

    # Check different sections for images
    sections = ['gtdaily']

    for section in sections:
        anchor = soup.find('a', attrs={'name': section}) #Only way to find the solutions is through the text in the <a> section
        
            # Download the first image in each section (correspond to the sudoku grid)
        img_tag = anchor.find_next('img')
        if img_tag and 'src' in img_tag.attrs:
            first_image_url = urljoin(url, img_tag['src'])
            if section == 'gtdaily':
                prefix = 'gt_'
                download_image(first_image_url, UNSOLVED_FOLDER, f"{prefix}{gt_count}.jpg")  
               # gt_count += 1
      
        
        if anchor:
            # Download the "Solution" image
            solution_link = anchor.find('a', string="Solution")
            if solution_link and 'href' in solution_link.attrs:
                solution_image_url = urljoin(url, solution_link['href'])

                if section == 'gtdaily':
                    prefix = 'gt_solved_'
                    download_image(solution_image_url, SOLVED_FOLDER, f"{prefix}{gt_count}.jpg")  
                    gt_count += 1


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

# Loop through the date range and scrape images
current_date = START_DATE
while current_date <= END_DATE:
    date_str = current_date.strftime("%Y/%m/%d") #Easier to do it this way
    url = f"{BASE_URL}/{date_str}"
    print(f"Processing: {url}") #Not really useful since in linear time 
    locate_images(url)
    current_date += timedelta(days=1)

