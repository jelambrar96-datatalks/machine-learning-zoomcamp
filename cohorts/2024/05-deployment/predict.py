import pickle

from flask import Flask
from flask import request
from flask import jsonify


MODEL_FILEPATH = "homework/model1.bin"
DV_FILEPATH = "homework/dv.bin"

def open_pickle(model_file):
    model = None
    with open(model_file, 'rb') as f_in:
        model = pickle.load(f_in)
    return model

MODEL_COLUMNS = ['job', 'duration', 'poutcome']
model1 = open_pickle(MODEL_FILEPATH)
dv = open_pickle(DV_FILEPATH)

app = Flask('churn')

@app.route('/predict', methods=['POST'])
def predict():
    customer = request.get_json()
    X = { item: customer[item] for item in MODEL_COLUMNS }
    X_transformed = dv.transform(X)
    y_pred = model1.predict_proba(X_transformed)[0, 1]
    churn = y_pred >= 0.5
    result = {
        'churn_probability': float(y_pred),
        'churn': bool(churn)
    }
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)
