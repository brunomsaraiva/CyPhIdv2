import os
import pickle
import random
import numpy as np

folders = ["Arara Pickles", "Elyra Pickles"]

for fld in folders:
    pickles_list = os.listdir(fld)

    for pck in pickles_list:
        tmp = pickle.load(open(fld + os.sep + pck, "rb"))

        random.shuffle(tmp)

        cut_i = int(len(tmp)*0.1)

        X = tmp[cut_i:]
        X_test = tmp[:cut_i]

        pickle.dump(X_test, open(fld + os.sep + "test_" + pck, "wb"))
        pickle.dump(X, open(fld + os.sep + pck, "wb"))

