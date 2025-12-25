#Convert the picture to a sudoku matrix for processing.

import cv2
import numpy as np
from trainDigitRecognition import knn_train

def image_to_sudoku_matrix(image_path, knn):
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
    # cv2.imshow('Image', gray)

    #         # Wait for a digit key press
    # cv2.waitKey(0)

    # Since data was trained without threshold, better not use it
   # _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    # Initialize a 9x9 matrix for the Sudoku grid
    sudoku_matrix = np.zeros((9, 9), dtype=int)

    cell_size = gray.shape[0] // 9  # Assuming the image is 9x9 cells
    for i in range(9):
        for j in range(9):
            # Extract the cell from the image
            cell = gray[i * cell_size:(i + 1) * cell_size, j * cell_size:(j + 1) * cell_size]

            # Preprocess the cell for KNN input
            cell_resized = cv2.resize(cell, (48, 48))  # Resize to match training size
            cell_flat = cell_resized.flatten() / 255.0  

            prediction = knn.predict([cell_flat])
            digit = prediction[0]

            if digit >= 0 and digit <= 9:
                sudoku_matrix[i, j] = digit  # Fill the matrix with the predicted digit
            else:
                sudoku_matrix[i, j] = 0  # If KNN can't predict, fill with 0

            if digit >= 0 and digit <= 9:
                cv2.putText(img, str(digit), 
                            (j * cell_size + cell_size // 4, i * cell_size + 3 * cell_size // 4),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    print("Sudoku Matrix:")
    print(sudoku_matrix)

    return sudoku_matrix

knn = knn_train()  # Uses the knn from trainDigitRecognitionS

image_path = 'gt_1.jpg'  # Unsolved one to try
try:
    sudoku_matrix = image_to_sudoku_matrix(image_path, knn)
except FileNotFoundError as e:
    print(e)
