from matplotlib import pyplot as plt
from PIL import Image
import numpy as np
import math
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
                    pixel = bytes_to_int(f.read(1))
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

def get_all_train_with_label(xtrain, ytrain):
    zipped = zip(xtrain,ytrain)
    res = sorted(list(zipped),key=lambda x:x[1])
    return res

def sortPixel(xtrain, ytrain, label):
    listOfSorted = []
    listWLabel = get_all_train_with_label(xtrain,ytrain)
    numb1 = (np.count_nonzero(np.array(ytrain)<label))
    numb2 = (np.count_nonzero(np.array(ytrain)==label))
    newList = listWLabel[numb1:(numb1)+numb2]
    newList = (list(zip(*newList)))[0]
    for i in range (784):
        listOfSorted.append(rotateA(newList,i))
    return listOfSorted


def rotateA (ima,x):
    newL = []
    for sublist in ima:
        newL.append(sublist[x])
    return newL

def showImage(imageF):
    #img = Image.fromarray(np.array(imageF),"L")
    plt.imshow(imageF, cmap='gray')
    plt.show(block=False)
    plt.pause(2)
    plt.close()

def getMean(sortedxtrain):
    mean =[]
    for sublist in sortedxtrain:
        mean.append(np.mean(sublist))
    return mean

def getVar(sortedxtrain):
    var = []
    for sublist in sortedxtrain:
        var.append(np.var(sublist)+0.01)
    return var

def log_likelyhood(shortedxtest,mean,var,porbofY):
    total =0
    for i in range(len(shortedxtest)):
        total += ((-0.5*math.log(2*math.pi))-(0.5*math.log(var[i]))-((1/(2*var[i]))*(shortedxtest[i]-mean[i])**2))
    total += math.log(porbofY)
    return total

def Bayes(X_train, Y_train, X_test):
    y_test_predF = []
    totalmean = []
    totalvar = []
    probofL = []
    for i in range(10):
        probofL.append((np.count_nonzero(np.array(Y_train) == i)/len(Y_train)))
        totalmean.append(getMean(sortPixel(X_train, Y_train, i)))
    for i in range(10):
        totalvar.append(getVar(sortPixel(X_train, Y_train, i)))
    for sublist in X_test:
        y_test_pred = []
        for i in range(10):
            y_test_pred.append(log_likelyhood(sublist,totalmean[i],totalvar[i],probofL[i]))
        y_test_predF.append(np.argmax(y_test_pred))

    return y_test_predF

def main():
    st = time.time()
    X_train = read_images(TRAIN_DATA,5000)
    Y_train = read_labels(TRAIN_LABEL,5000)
    X_test = read_images(TEST_DATA,100)
    Y_test = read_labels(TEST_LABEL,100)
    #for idx, test_sample in enumerate(X_test):
        #showImage(rotateB(test_sample))

    X_train = extract(X_train)
    X_test = extract(X_test)

    y_pred = Bayes(np.array(X_train),np.array( Y_train),np.array(X_test))
    print(y_pred)

    accuracy = [
        sum(int(y_pred_i ==(y_test_i)) for y_pred_i, y_test_i in zip(y_pred,Y_test))/len(Y_test)
    ]
    print("the accuracy of this execution was "+ str(accuracy[0]*100)+"%")
    et = time.time()
    print ("Time it took to finish training and testing the data is " + str(et-st)+ " seconds.")
    print("Efficiency was " +str((accuracy[0]*100)/(et-st)))

if __name__ == '__main__':
    main()