#The labels are in the form of 4 chars corresponding to the north, east, south and west borders of each cell respectively
#n = None  g = Greater than  l = Less than.
#Tested accuracy was 100%

import cv2
import numpy as np
import os
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split


def create_masked_image(image):
    # Create a mask of zeros (black)
    mask = np.zeros(image.shape, dtype=np.uint8)

    # Define the coordinates for the white square
    top_left = (10, 10)
    bottom_right = (30, 30)

    # Fill the square area in the mask with white (255)
    cv2.rectangle(mask, top_left, bottom_right, (255, 255, 255), thickness=-1)

    # Combine the original image with the mask
    masked_image = cv2.bitwise_and(image, mask)
    
    return masked_image

def prepare_data_from_directory(directory):
    X = []  # Features
    y = []  # Labels

    for filename in os.listdir(directory):
        if filename.endswith('.jpg'):  # Change to your image extension if needed
            img_path = os.path.join(directory, filename)
            img = cv2.imread(img_path)

            # Check if image is loaded
            if img is None:
                print(f"Could not open or find the image at {img_path}")
                continue

            # Create the masked image
            masked_image = create_masked_image(img)

            # Flatten the masked image and normalize
            img_flat = masked_image.flatten() / 255.0
            X.append(img_flat)

            # Extract the label from the filename (first 4 characters)
            label = (os.path.basename(filename)[:4])
            y.append(label)

    return np.array(X), np.array(y)

#Knn for the recognition of the greater signs
def knn_greater_train():

    # Prepare training data from the Training folder
    X_train, y_train = prepare_data_from_directory('Training_GT_Greater')  # Adjust path as necessary

    # Initialize and train KNN model
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(X_train, y_train)

    # Prepare test data from the Test folder
    X_test, y_test = prepare_data_from_directory('Test_Greater')  # Adjust path as necessary
    # Evaluate KNN model
    y_pred = knn.predict(X_test)  # Make predictions
    accuracy = knn.score(X_test, y_test)

    print(f'Accuracy: {accuracy * 100:.2f}%')

    # Display errors
    errors = []
    for i in range(len(y_pred)):
        if y_pred[i] != y_test[i]:
            errors.append((y_test[i], y_pred[i], i))  # Collect true label, predicted label, and the index

    # Print the errors
    if errors:
        print("\nMisclassified Samples:")
        for true, predicted, index in errors:
            print(f"Index: {index}, True Label: {true}, Predicted Label: {predicted}")
    else:
        print("No misclassifications found.")

    return knn

knn_greater_train()