import os
import joblib
import numpy as np

def model_fn(model_dir):
    model = joblib.load(os.path.join(model_dir, "model.pkl"))
    return model

def input_fn(request_body, request_content_type):
    data = np.array(eval(request_body))
    return data

def predict_fn(input_data, model):
    prediction = model.predict(input_data)
    return prediction

def output_fn(prediction, content_type):
    return str(prediction)

