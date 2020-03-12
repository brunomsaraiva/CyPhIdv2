from classifier import Classifier

app = Classifier()
app.load_model(model_path="model")
app.load_data(data_path="Elyra Pickles\\test_X_phase3.p", microscope="Elyra")
app.classify_data(true_class=3)
