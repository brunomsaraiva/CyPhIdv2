from classifier import Classifier
import pandas as pd
import os

analysis_path = "C:\\Users\\User\\Desktop\\Coding\\screening.csv"

db = pd.read_csv(analysis_path, sep=";")

reports_path = "E:\\Processed Screening Images"

classifier = Classifier()
classifier.load_model(model_path="model")

results = "Plate;Mutant;Images;Phase1;Phase2;Phase3;Total;Phase1perc;Phase2perc;Phase3perc;\n"

def convert_to_image_number(lst):

    image_numbers = []

    for n in lst.split(","):
        try:
            number = int(n)
            image_numbers.append(number)
        except ValueError:
            pass

    return list(set(image_numbers))

for i in range(db.shape[0]):
    plate = db.iloc[i]["Plate"]
    mutant = db.iloc[i]["Mutant"]
    images = convert_to_image_number(db.iloc[i]["Images"])

    print(plate, mutant, images)

    if len(images) > 0:
        mutant_total = 0
        mutant_phase_1 = 0
        mutant_phase_2 = 0
        mutant_phase_3 = 0

        for image_n in images:

            print("Running report " + str(image_n) + " from " + plate + " " + mutant)

            report = reports_path + os.sep + plate + os.sep + mutant + os.sep + "Reports" + os.sep
            report += "Report_" + str(image_n)

            if os.path.exists(report):

                classifier.classify_screening_report(prediction_type="Class", report_path=report)
                preds = classifier.predictions

                image_total = 0
                image_phase_1 = 0
                image_phase_2 = 0
                image_phase_3 = 0
                for ii in range(len(preds[0])):
                    image_total += 1

                    if str(preds[1][ii]) == str(1):
                        image_phase_1 += 1
                    elif str(preds[1][ii]) == str(2):
                        image_phase_2 += 1
                    elif str(preds[1][ii]) == str(3):
                        image_phase_3 += 1

                classifier.save_predictions(save_path=report)

                mutant_total += image_total
                mutant_phase_1 += image_phase_1
                mutant_phase_2 += image_phase_2
                mutant_phase_3 += image_phase_3

        results += plate + ";" + mutant + ";" + ",".join([str(x) for x in images]) + ";"
        results += str(mutant_phase_1) + ";" + str(mutant_phase_2) + ";" + str(mutant_phase_3) + ";"
        results += str(mutant_total) + ";"
        results += str(int(100*mutant_phase_1/mutant_total)) + ";"
        results += str(int(100*mutant_phase_2/mutant_total)) + ";"
        results += str(int(100*mutant_phase_3/mutant_total)) + ";\n"

    else:
        results += plate + ";" + mutant + ";" + "none" + ";;;;;;;\n"

file = open("screening_cyphid_v3.csv", "w")
file.writelines(results)
file.close()