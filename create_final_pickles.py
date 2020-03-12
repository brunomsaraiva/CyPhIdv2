import numpy as np
import pickle
import random
from skimage.exposure import rescale_intensity


X_a = pickle.load(open("Arara Pickles\\resized_balanced_X_rotations_arara.p", "rb"))
X_a.extend(pickle.load(open("Elyra Pickles\\Without Discarded\\balanced_X_rotations_elyra.p", "rb")))

print(len(X_a))

y_a = pickle.load(open("Arara Pickles\\balanced_y_rotations_arara.p", "rb"))
y_a.extend(pickle.load(open("Elyra Pickles\\Without Discarded\\balanced_y_rotations_elyra.p", "rb")))

X = np.array([[np.concatenate((rescale_intensity(X_a[i][0]), rescale_intensity(X_a[i][1])), axis=1), y_a[i]] for i in range(len(X_a))])

random.shuffle(X)

pickle.dump(X[:, 0], open("wo_discarded_combined_X.p", "wb"))
pickle.dump(X[:, 1], open("wo_discarded_combined_y.p", "wb"))
