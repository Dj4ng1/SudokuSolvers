#Convert the picture to a sudoku matrix for processing.
#Generate 2 matrixes : one for digits and one for the greater/lesser signs.
#Can do it in one matrix, but the digit one gives us more data for regular and other variants of sudoku

import cv2
import numpy as np
import pandas as pd
from trainDigitRecognition_GT import knn_digit_train
from trainPatternRecognition_GT import knn_greater_train, create_masked_image

# Function to validate predictions
def is_valid_prediction(prediction):
    # Check the length of the string
    if len(prediction[0]) != 4:
        print(len(prediction))
        print(prediction)
        return False

    # Check if all characters are either 'n', 'g', or 'l'
    valid_chars = {'n', 'g', 'l'}
    return all(c in valid_chars for c in prediction[0])


def image_to_sudoku_matrix(image_path, knn_digit, knn_greater):
    print(f"Loading image from: {image_path}")
    
    # Load the image
    img = cv2.imread(image_path)
    img = img[16:img.shape[0]-20, :]  # Cropping the image of the date and footer

    # Check if the image is loaded
    if img is None:
        raise FileNotFoundError(f"Could not open or find the image at {image_path}")

    print("Image loaded successfully.")
    
    # Convert the image to grayscale bc of the slight color differences
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    # Initialize a 9x9 matrix for the Sudoku grid
    sudoku_digit_matrix = np.zeros((9, 9), dtype=int)
    sudoku_greater_matrix = np.full((9, 9), '', dtype=object)
  
    cell_size_gray = gray.shape[0] // 9  # Assuming the image is 9x9 cells
    cell_size = img.shape[0] // 9

    for i in range(9):
        for j in range(9):

   ############Preprocess the cell for KNN input for the digit side
            # Extract the cell from the image A BIG DIFFERENCE IS THAT DIGIT NEEDS GRAYSCALE BUT NOT GREATER
            cell = gray[i * cell_size_gray:(i + 1) * cell_size_gray, j * cell_size_gray:(j + 1) * cell_size_gray] 
            cell_resized = cv2.resize(cell, (48, 48))  # Resize to match training size

            cell_flat = cell_resized.flatten() / 255.0  


            prediction = knn_digit.predict([cell_flat])
            digit = prediction[0]

            if digit >= 0 and digit <= 9:
                sudoku_digit_matrix[i, j] = digit  # Fill the matrix with the predicted digit
            else:
                sudoku_digit_matrix[i, j] = 0  # If KNN can't predict, fill with 0



   ############Now we do the same for the greater than side##########
            cell = img[i * cell_size_gray:(i + 1) * cell_size_gray, j * cell_size_gray:(j + 1) * cell_size_gray]
 
            cell_white = create_masked_image(cell)
            cell_resized = cv2.resize(cell_white, (48, 48))  # Resize to match training size


        
            cell_flat = cell_white.flatten() / 255.0  
            # print(cell_flat.shape[0])
            # cv2.imshow('Image', cell)
            # key = cv2.waitKey(0)
            # while True:
            #     pass 
            prediction = knn_greater.predict([cell_flat])

            if(is_valid_prediction(prediction)):
                sudoku_greater_matrix[i, j] = str(prediction[0])  # Fill the matrix with the predicted digit
            else:
                sudoku_greater_matrix[i, j] = "xxxx"  # Fill the matrix with the predicted digit




    print("Sudoku digit Matrix:")
    print(sudoku_digit_matrix)
    print("Sudoku GT Matrix:")
    print(sudoku_greater_matrix)

    return sudoku_digit_matrix, sudoku_greater_matrix


knn_digit= knn_digit_train()  # knn for the digit recognition
knn_greater= knn_greater_train()  # knn for the digit recognition


image_path = 'gt_1.jpg'  # Unsolved one to try
try:
    sudoku_digit_matrix, sudoku_greater_matrix = image_to_sudoku_matrix(image_path, knn_digit, knn_greater)

    pd.DataFrame(sudoku_greater_matrix).to_csv('sudoku_greater_matrix.csv', index=False, header=False)
    pd.DataFrame(sudoku_digit_matrix).to_csv('sudoku_digit_matrix.csv', index=False, header=False)

except FileNotFoundError as e:
    print(e)
