from matplotlib import pyplot as plt
from PIL import Image
import numpy as np
import time


DATA_DIR = '/Users/altarazir/PycharmProjects/pythonProject/data/'
TRAIN_DATA = DATA_DIR + 'train-images-idx3-ubyte'
TRAIN_LABEL = DATA_DIR + 'train-labels-idx1-ubyte 2'
TEST_DATA = DATA_DIR + 't10k-images-idx3-ubyte'
TEST_LABEL = DATA_DIR+ 't10k-labels-idx1-ubyte'

def read_image(path):
    return np.array(Image.open(path).convert("L"))


def bytes_to_int(byte_data):
    return int.from_bytes(byte_data, 'big')

def read_images(filename, n_max_images):
    images = []
    with open(filename, 'rb') as f:
        _ = f.read(4)  # magic number
        n_images = bytes_to_int(f.read(4))
        if n_max_images:
            n_images = n_max_images
        n_rows = bytes_to_int(f.read(4))
        n_columns = bytes_to_int(f.read(4))
        for image_idx in range(n_images):
            image = []
            for row_idx in range(n_rows):
                row = []
                for col_idx in range(n_columns):
                    pixel = f.read(1)
                    row.append(pixel)
                image.append(row)
            images.append(image)
    return images

def read_labels(filename, n_max_labels):
    labels = []
    with open(filename, 'rb') as f:
        _ = f.read(4)  # magic number
        n_labels = bytes_to_int(f.read(4))
        if n_max_labels:
            n_labels = n_max_labels
        for label_idx in range(n_labels):
            label = bytes_to_int(f.read(1))
            labels.append(label)
    return labels

def flatten(dataset):
    return [pixel for sublist in dataset for pixel in sublist]

def extract(dataset):
    return[flatten(sample) for sample in dataset]
def dist(train_sample,test_sample):
    return (sum([(bytes_to_int(train_sample_i) - bytes_to_int(test_sample_i))**2 for train_sample_i, test_sample_i in zip(train_sample, test_sample)])**0.5)

def get_training_distances(X_train, test_sample):
    return[dist(train_sample, test_sample) for train_sample in X_train]



def getLetter(x):
    letter = 0
    if (0<=x<=9):
        letter = x+48
    elif (10<=x<=35):
        letter = x+ 55
    elif (36<=x<=60):
        letter = x+61
    return chr(letter)


def showImage(imageF):
    img = Image.fromarray(np.array(imageF),"L")
    plt.imshow(img, cmap='gray')
    plt.show(block=False)
    plt.pause(2)
    plt.close()

def get_top_candidate (candidates):
    return max(candidates, key = candidates.count)

def knn(X_train, Y_train, X_test , k):
    y_test_pred = []
    for test_sample_idx, test_sample in enumerate(X_test):
        training_distances = get_training_distances(X_train, test_sample)
        sorted_distances = [
            pair[0]for pair in sorted(enumerate(training_distances),key=lambda x: x[1])
        ]
        candidates = [
            (Y_train[idx])
            for idx in sorted_distances[:k]
        ]
        top_candidate = get_top_candidate(candidates)
        y_test_pred.append((top_candidate))
    return y_test_pred


def main():
    st = time.time()

    X_train = read_images(TRAIN_DATA,5000)
    Y_train = read_labels(TRAIN_LABEL, 5000)
    X_test = read_images(TEST_DATA,100)
    Y_test = read_labels(TEST_LABEL,100)

   # for idx, test_sample in zip(Y_test,X_test):
    #    showImage((test_sample))
     #   print(idx)

    X_train = extract(X_train)
    X_test = extract(X_test)


    y_pred = knn(X_train, Y_train,X_test,3)
    print(y_pred)

    accuracy = [
        sum(int(y_pred_i ==(y_test_i)) for y_pred_i, y_test_i in zip(y_pred,Y_test))/len(Y_test)
    ]
    print("the accuracy of this execution was " + str(accuracy[0] * 100) + "%")
    et = time.time()
    print("Time it took to finish training and testing the data is " + str(et - st) + " seconds.")
    print("Efficiency was " + str((accuracy[0] * 100) / (et - st)))

if __name__ == '__main__':
    main()