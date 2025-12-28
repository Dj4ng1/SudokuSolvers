import os
import cv2
import numpy as np
import pandas as pd
from trainDigitRecognition_GT import knn_digit_train
from trainPatternRecognition_GT import knn_greater_train, create_masked_image

# Function to validate predictions
def is_valid_prediction(prediction):
    if len(prediction[0]) != 4:
        return False
    valid_chars = {'n', 'g', 'l'}
    return all(c in valid_chars for c in prediction[0])

def image_to_sudoku_matrix(image_path, knn_digit, knn_greater):
    print(f"Loading image from: {image_path}")

    img = cv2.imread(image_path)
    img = img[16:img.shape[0]-20, :]  # Cropping the image

    if img is None:
        raise FileNotFoundError(f"Could not open or find the image at {image_path}")

    print("Image loaded successfully.")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sudoku_digit_matrix = np.zeros((9, 9), dtype=int)
    sudoku_greater_matrix = np.full((9, 9), '', dtype=object)

    cell_size_gray = gray.shape[0] // 9

    for i in range(9):
        for j in range(9):
            #### Digit prediction ####
            cell = gray[i * cell_size_gray:(i + 1) * cell_size_gray, j * cell_size_gray:(j + 1) * cell_size_gray]
            cell_resized = cv2.resize(cell, (48, 48))
            cell_flat = cell_resized.flatten() / 255.0  
            prediction = knn_digit.predict([cell_flat])
            digit = prediction[0]

            if 0 <= digit <= 9:
                sudoku_digit_matrix[i, j] = digit  
            else:
                sudoku_digit_matrix[i, j] = 0  

            #### Greater/Less than prediction ####
            cell = img[i * cell_size_gray:(i + 1) * cell_size_gray, j * cell_size_gray:(j + 1) * cell_size_gray]
            cell_white = create_masked_image(cell)
            cell_resized = cv2.resize(cell_white, (48, 48))
            cell_flat = cell_white.flatten() / 255.0 
            prediction = knn_greater.predict([cell_flat])

            if is_valid_prediction(prediction):
                sudoku_greater_matrix[i, j] = str(prediction[0])  
            else:
                sudoku_greater_matrix[i, j] = "xxxx"  

    return sudoku_digit_matrix, sudoku_greater_matrix

def process_images_in_folder(folder_path):
    knn_digit = knn_digit_train()  
    knn_greater = knn_greater_train()  

    # List to hold flattened matrices
    flattened_digit_matrices = []
    flattened_greater_matrices = []

    for index, filename in enumerate(os.listdir(folder_path)):
        if filename.endswith('.jpg') or filename.endswith('.png'):  # Process only image files
            image_path = os.path.join(folder_path, filename)
            try:
                sudoku_digit_matrix, sudoku_greater_matrix = image_to_sudoku_matrix(image_path, knn_digit, knn_greater)

                # Flatten and prepend the index
                flattened_digit_matrices.append(np.insert(sudoku_digit_matrix.flatten(), 0, index))
                flattened_greater_matrices.append(np.insert(sudoku_greater_matrix.flatten(), 0, index))

            except FileNotFoundError as e:
                print(e)

    # Convert lists to DataFrames
    digit_df = pd.DataFrame(flattened_digit_matrices)
    greater_df = pd.DataFrame(flattened_greater_matrices)

    # Save all matrices into single CSV files
    digit_df.to_csv('sudoku_digit_matrice_batch.csv', index=False, header=False)
    greater_df.to_csv('sudoku_gt_matrice_batch.csv', index=False, header=False)

folder_path = 'Solved_GT'  
process_images_in_folder(folder_path)
