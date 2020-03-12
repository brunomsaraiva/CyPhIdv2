import os
import pickle
import numpy as np
from random import shuffle
from skimage.transform import rotate

rotations = [x for x in range(15, 360, 15)]

X = pickle.load(open("Elyra Pickles\\Without Discarded\\balanced_X_elyra.p", "rb"))
y = pickle.load(open("Elyra Pickles\\Without Discarded\\balanced_y_elyra.p", "rb"))
print(len(X))

data = []

for i in range(len(X)):

    tmp = []
    tmp.append(X[i])
    tmp.append(y[i])

    data.append(tmp)

    for rot in rotations:
        tmp = []
        tmp.append([rotate(X[i][0], rot), rotate(X[i][1], rot)])
        tmp.append(y[i])
        data.append(tmp)

    print(i)

shuffle(data)


new_X = []
new_y = []
for images, label in data:
    new_X.append(images)
    new_y.append(int(label))
    print(int(label))

pickle.dump(new_X, open("Elyra Pickles\\Without Discarded\\balanced_X_rotations_elyra.p", "wb"))
pickle.dump(new_y, open("Elyra Pickles\\Without Discarded\\balanced_y_rotations_elyra.p", "wb"))

