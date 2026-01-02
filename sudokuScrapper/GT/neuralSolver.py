import numpy as np
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from tensorflow import keras
import pandas as pd

#######Function to load csv
def load_csv_to_grids(csv_file):
    # Load the CSV file
    df = pd.read_csv(csv_file, header=None)  # No header in the CSV
    grids = []

    for index, row in df.iterrows():
        # Skip the first element (index) and transform the rest into a 9x9 grid
        grid_elements = row[1:].values  # Get the elements after the index
        grid = grid_elements.reshape((9, 9))  # Reshape into a 9x9 array
        grids.append(grid)

    return grids
        ##########End function to load csv

digit_file = 'sudoku_digit_matrice_batch.csv'  
gt_file = 'sudoku_gt_matrice_batch.csv'  

digit_matrix = load_csv_to_grids(digit_file)
gt_matrix = load_csv_to_grids(gt_file)



