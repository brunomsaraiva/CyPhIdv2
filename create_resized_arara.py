import os
import pickle
import numpy as np
from random import shuffle
from skimage.transform import resize

pickle_in = open("Arara Pickles\\balanced_X_rotations_arara.p", "rb")
tmp = pickle.load(pickle_in)
pickle_in.close()

for i in range(len(tmp)):
    tmp[i][0] = resize(tmp[i][0], (100, 100), order=0, preserve_range=True, anti_aliasing=False,
                       anti_aliasing_sigma=None)
    tmp[i][1] = resize(tmp[i][1], (100, 100), order=0, preserve_range=True, anti_aliasing=False,
                       anti_aliasing_sigma=None)

    print(i)

print(tmp[0][0].shape)

pickle_out = open("resized_balanced_X_rotations_arara.p", "wb")
pickle.dump(tmp, pickle_out)
pickle_out.close()


pickle_in = open("Arara Pickles\\X_rotations_arara.p", "rb")
tmp = pickle.load(pickle_in)
pickle_in.close()

for i in range(len(tmp)):
    tmp[i][0] = resize(tmp[i][0], (100, 100), order=0, preserve_range=True, anti_aliasing=False,
                       anti_aliasing_sigma=None)
    tmp[i][1] = resize(tmp[i][1], (100, 100), order=0, preserve_range=True, anti_aliasing=False,
                       anti_aliasing_sigma=None)

    print(i)

pickle_out = open("resized_X_rotations_arara.p", "wb")
pickle.dump(tmp, pickle_out)
pickle_out.close()

