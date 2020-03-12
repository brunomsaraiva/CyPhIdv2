import os
import pickle
import numpy as np
from skimage.io import imread
from skimage.util import img_as_float
from skimage.exposure import rescale_intensity
from skimage.transform import resize
from keras.models import load_model
from tkinter.filedialog import askdirectory, askopenfilename

class Classifier(object):
    def __init__(self):
        self.model = load_model("model")
        self.data = None
        self.predictions = None

    def load_model(self, model_path=None):

        if model_path is None:
            model_path = askopenfilename()

        self.model = load_model(model_path)

    def load_data(self, data_path=None, microscope=None):

        if data_path is None:
            data_path = askopenfilename()

        self.data = pickle.load(open(data_path, "rb"))

        if microscope == "Arara":
            self.data = [resize(np.concatenate((rescale_intensity(x[0]), rescale_intensity(x[1])), axis=1), (100, 200),
                                order=0, preserve_range=True, anti_aliasing=False,
                                anti_aliasing_sigma=None) for x in self.data]
        elif microscope == "Elyra":
            self.data = [np.concatenate((rescale_intensity(x[0]), rescale_intensity(x[1])), axis=1) for x in self.data]

        self.data = np.array(list(self.data)).reshape(-1, 100, 200, 1)

    def classify_data(self, true_class=0):

        total = 0
        misclassified = 0

        pred = self.model.predict_classes(self.data)

        for classification in pred:
            total += 1
            if classification+1 != true_class:
                misclassified += 1


        print(float(misclassified)*100.0/float(total))

    def classify_data_prob(self):

        pred = self.model.predict_proba(self.data)

        return pred

    def preprocess_image(self, image):
        h, w = image.shape
        image = image[:, int(w/2):w+1]
        h, w = image.shape

        max_h, max_w = 50, 50

        lines_to_add = max_h - h
        columns_to_add = max_w - w

        if lines_to_add%2 == 0:
            new_line = np.zeros((int(lines_to_add/2), w))
            image = np.concatenate((new_line, image, new_line), axis=0)
        else:
            new_line_top = np.zeros((int(lines_to_add/2)+1, w))
            new_line_bot = np.zeros((int(lines_to_add/2), w))
            image = np.concatenate((new_line_top, image, new_line_bot), axis=0)

        if columns_to_add%2 == 0:
            columns_to_add = np.zeros((50, int(columns_to_add/2)))
            image = np.concatenate((columns_to_add, image, columns_to_add), axis=1)
        else:
            columns_to_add_left = np.zeros((50, int(columns_to_add/2)+1))
            columns_to_add_right = np.zeros((50, int(columns_to_add/2)))
            image = np.concatenate((columns_to_add_left, image, columns_to_add_right), axis=1)

        image = img_as_float(image)
        image = image.reshape(50, 50, 1)

        return image

    def classify_new_images(self, images, prediction_type="Class"):

        if prediction_type == "Class":
            prediction = self.model.predict_classes(images)
        elif prediction_type == "Probability":
            prediction = self.model.predict_proba(images)
        return prediction

    def classify_screening_report(self, prediction_type="Class", report_path=None):

        self.predictions = []

        if report_path is None:
            report_path = askdirectory()

        images_path = report_path + os.sep + "_cell_data" + os.sep + "fluor"
        dna_path = report_path + os.sep + "_cell_data" + os.sep + "optional"
        images_list = os.listdir(images_path)
        images = []

        cell_ids = []

        for image_name in images_list:
            img = imread(images_path + os.sep + image_name)

            h, w = img.shape

            if h <= 50 and w <= 100:
                img = self.preprocess_image(img)
                cell_ids.append(image_name.split(".")[0])

            dna_img = imread(dna_path + os.sep + image_name)

            h, w = dna_img.shape

            if h <= 50 and w <= 100:
                dna_img = self.preprocess_image(dna_img)

            images.append(resize(np.concatenate((rescale_intensity(img), rescale_intensity(dna_img)), axis=1),
                                 (100, 200), order=0, preserve_range=True, anti_aliasing=False,
                                 anti_aliasing_sigma=None).reshape(100, 200, 1))

        images = np.array(images)
        images = images.reshape(-1, 100, 200, 1)
        pred = self.classify_new_images(images, prediction_type="Class")

        self.predictions = [cell_ids, pred+1]

    def save_predictions(self, save_path=None):

        if save_path is None:
            save_path = askdirectory()

        report = "CellId;Prediction;\n"

        for i in range(len(self.predictions[0])):
            report += self.predictions[0][i] + ";" + str(self.predictions[1][i]) + ";\n"

        file = open(save_path + os.sep + "classification_report_v2.csv", "w")
        file.writelines(report)
        file.close()

