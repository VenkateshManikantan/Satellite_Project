from PIL import Image
from matplotlib import pyplot as plt
import sys
import numpy as np
import math



IMAGE = []
IMAGE_3D_MATRIX = []

def kmeans_main(cluster_points,K):
    """Function: K_means clustering 
    `Function to perform K_means clustering with the image matrix'

    Parameters
    ----------
    cluster_points: 2-D array 
        path to the targeted folder
    K: int 
        k-MEANS CENTRIODS intiation clusters  
    Returns
    -------
    performs K-means clustering on the RGB matrixes """
    # rounding pixel values and getting cluster RGB
    centers = []
    for i in range(len(cluster_points)):
        cluster_points[i] = (int(math.floor(cluster_points[i][0])), int(math.floor(cluster_points[i][1])))
        red = IMAGE_3D_MATRIX[cluster_points[i][0]][cluster_points[i][1]][0]
        green = IMAGE_3D_MATRIX[cluster_points[i][0]][cluster_points[i][1]][1]
        blue = IMAGE_3D_MATRIX[cluster_points[i][0]][cluster_points[i][1]][2]
        centers.append([red, blue, green])

    centers = np.array(centers)

    # Initializing class and distance arrays
    classes = np.zeros([IMAGE_3D_MATRIX.shape[0], IMAGE_3D_MATRIX.shape[1]], dtype=np.float64)
    distances = np.zeros([IMAGE_3D_MATRIX.shape[0], IMAGE_3D_MATRIX.shape[1], K], dtype=np.float64)

    for i in range(10):
        # finding distances for each center
        for j in range(K):
            distances[:, :, j] = np.sqrt(((IMAGE_3D_MATRIX - centers[j]) ** 2).sum(axis=2))

        # choosing the minimum distance class for each pixel
        classes = np.argmin(distances, axis=2)

        # rearranging centers
        for c in range(K):
            centers[c] = np.mean(IMAGE_3D_MATRIX[classes == c], 0)

    # changing values with respect to class centers
    for i in range(IMAGE_3D_MATRIX.shape[0]):
        for j in range(IMAGE_3D_MATRIX.shape[1]):
            IMAGE_3D_MATRIX[i][j] = centers[classes[i][j]]


def kmeans_with_click():
    global IMAGE
    plt.imshow(IMAGE)
    points = plt.ginput(K, show_clicks=True)
    points = [t[::-1] for t in points]  # reversing tuples
    kmeans_main(points)


def kmeans_with_random(K):
    global IMAGE_3D_MATRIX
    points = []
    for i in range(K):
        x = np.random.uniform(0, IMAGE_3D_MATRIX.shape[0])
        y = np.random.uniform(0, IMAGE_3D_MATRIX.shape[1])
        points.append((x, y))

    kmeans_main(points,K)


def read_image(PATH_TO_FILE):
    global IMAGE, IMAGE_3D_MATRIX
    IMAGE = Image.open(open(PATH_TO_FILE, 'rb'))
    IMAGE_3D_MATRIX = np.array(IMAGE).astype(int)


def handle_arguments():
    global PATH_TO_FILE, K, RUN_MODE
    PATH_TO_FILE, K, RUN_MODE = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])

    if K < 1:
        sys.exit("K should be greater than 1, your K value is {}".format(K))

    if RUN_MODE not in {0, 1}:
        sys.exit("Program mode should be either 0 or 1, your value is {}".format(RUN_MODE))


def save_image():
    global IMAGE_3D_MATRIX
    im = Image.fromarray(IMAGE_3D_MATRIX.astype('uint8'))
    im.save('data/temp_data/output_k.png')


def run_K_img_std(PATH_TO_FILE,K):
    read_image(PATH_TO_FILE)
    kmeans_with_random(K)
    save_image()