import os
import pickle
import numpy as np
from random import shuffle
from skimage.transform import rotate

rotations = [x for x in range(15, 360, 15)]

# Maximum for balanced:
max_arara = 1957
max_elyra = 1305

"""
X = {}

for file in os.listdir("Arara Pickles"):

    if file.split("_")[0] == "X":
        tmp = pickle.load(open("Arara Pickles" + os.sep + file, "rb"))
        classification = file.split(".")[0][-1]

        X[classification] = []

        for cell in tmp:
            X[classification].append(cell)

tmp_X = []
tmp_y = []

tmp_X.extend(X["1"][0:1957])
tmp_y.extend(["1"]*1957)
tmp_X.extend(X["2"][0:1957])
tmp_y.extend(["2"]*1957)
tmp_X.extend(X["3"][0:1957])
tmp_y.extend(["3"]*1957)

pickle.dump(tmp_X, open("balanced_X_arara.p", "wb"))
pickle.dump(tmp_y, open("balanced_y_arara.p", "wb"))

tmp_X.extend(X["1"][1957:])
tmp_y.extend(["1"]*(len(X["1"])-1957))
tmp_X.extend(X["2"][1957:])
tmp_y.extend(["2"]*(len(X["2"])-1957))
tmp_X.extend(X["3"][1957:])
tmp_y.extend(["3"]*(len(X["3"])-1957))

pickle.dump(tmp_X, open("X_arara.p", "wb"))
pickle.dump(tmp_y, open("y_arara.p", "wb"))
"""

X = {}

for file in os.listdir("Elyra Pickles"):



    if file.split("_")[0] == "X":
        tmp = pickle.load(open("Elyra Pickles" + os.sep + file, "rb"))
        classification = file.split(".")[0][-1]
        print(classification)

        X[classification] = []

        for cell in tmp:
            X[classification].append(cell)

tmp_X = []
tmp_y = []

tmp_X.extend(X["1"][0:1305])
tmp_y.extend(["1"]*1305)
tmp_X.extend(X["2"][0:1305])
tmp_y.extend(["2"]*1305)
tmp_X.extend(X["3"][0:1305])
tmp_y.extend(["3"]*1305)

pickle.dump(tmp_X, open("Elyra Pickles\\Without Discarded\\balanced_X_elyra.p", "wb"))
pickle.dump(tmp_y, open("Elyra Pickles\\Without Discarded\\balanced_y_elyra.p", "wb"))

tmp_X.extend(X["1"][1305:])
tmp_y.extend(["1"]*(len(X["1"])-1305))
tmp_X.extend(X["2"][1305:])
tmp_y.extend(["2"]*(len(X["2"])-1305))
tmp_X.extend(X["3"][1305:])
tmp_y.extend(["3"]*(len(X["3"])-1305))

pickle.dump(tmp_X, open("Elyra Pickles\\Without Discarded\\X_elyra.p", "wb"))
pickle.dump(tmp_y, open("Elyra Pickles\\Without Discarded\\y_elyra.p", "wb"))

