import imageio
import matplotlib.pyplot as plt
import pickle
from scipy.misc import imresize
from settings import *

def normalize(array):
    """
    Resize and normalize the image array. Normalized array has a range of (0,1)
    """
    X = imresize(array, (28, 28), interp='cubic').astype(float).reshape(1, 784)
    X /= 255
    return X

if __name__ == '__main__':
    im = imageio.imread('tmp.png', as_gray=True)
    # for item in im:
    #     print(item)


    X = normalize(im)
    plt.imshow(X.reshape(28,28), cmap="gray")
    plt.show()
