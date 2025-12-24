import numpy as np
import cv2
import os
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score



# Function to load data from a directory
def load_data_from_directory(directory):
    X = []  # Features
    y = []  # Labels as found in the file name

    for filename in os.listdir(directory):
        if filename.endswith('.jpg'): 
            label = int(filename[0])  # First character as the label
            img_path = os.path.join(directory, filename)  
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)  # Load as grayscale
            
            if img is not None:  
                img_flat = img.flatten() / 255.0  # Normalize and flatten
                X.append(img_flat)
                y.append(label)

    return np.array(X), np.array(y)


def knn_train():

    X_train, y_train = load_data_from_directory('Training')
    X_test, y_test = load_data_from_directory('Test')

    # WOrks best in 2d
    X_train = X_train.reshape(X_train.shape[0], -1)
    X_test = X_test.reshape(X_test.shape[0], -1)

    # Initialize and train KNN model with either 3 or 5 neighbors
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = knn.predict(X_test)

    # Evaluate the model with the 200 remaining pictures
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy * 100:.2f}%')

    return knn

