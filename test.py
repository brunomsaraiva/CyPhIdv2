from classifier_training import ModelTrainer
import numpy as np

model = ModelTrainer()
model.run_trainer("wo_discarded_combined_X.p",
                  "wo_discarded_combined_y")
model.save_model(path="model_4")

