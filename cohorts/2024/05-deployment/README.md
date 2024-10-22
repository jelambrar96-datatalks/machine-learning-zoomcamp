## Homework

> Note: sometimes your answer doesn't match one of the options exactly. 
> That's fine. 
> Select the option that's closest to your solution.

> Note: we recommend using python 3.11 in this homework.

In this homework, we will use the Bank Marketing dataset. Download it from [here](https://archive.ics.uci.edu/static/public/222/bank+marketing.zip).

You can do it with `wget`:

```bash
wget https://archive.ics.uci.edu/static/public/222/bank+marketing.zip
unzip bank+marketing.zip 
unzip bank.zip
```

We need `bank-full.csv`.

You can also access the copy of `back-full.csv` directly:

```bash
wget https://github.com/alexeygrigorev/datasets/raw/refs/heads/master/bank-full.csv
```


## Question 1

* Install Pipenv
* What's the version of pipenv you installed?
* Use `--version` to find out

```
pipenv==2024.1.0
```

## Question 2

* Use Pipenv to install Scikit-Learn version 1.5.2
* What's the first hash for scikit-learn you get in Pipfile.lock?

> **Note**: you should create an empty folder for homework
and do it there. 

```
03b6158efa3faaf1feea3faa884c840ebd61b6484167c711548fce208ea09445
```

## Models

We've prepared a dictionary vectorizer and a model.

They were trained (roughly) using this code:

```python
features = ['job', 'duration', 'poutcome']
dicts = df[features].to_dict(orient='records')

dv = DictVectorizer(sparse=False)
X = dv.fit_transform(dicts)

model = LogisticRegression().fit(X, y)
```

> **Note**: You don't need to train the model. This code is just for your reference.

And then saved with Pickle. Download them:

* [DictVectorizer](https://github.com/DataTalksClub/machine-learning-zoomcamp/tree/master/cohorts/2024/05-deployment/homework/dv.bin?raw=true)
* [LogisticRegression](https://github.com/DataTalksClub/machine-learning-zoomcamp/tree/master/cohorts/2024/05-deployment/homework/model1.bin?raw=true)

With `wget`:

```bash
PREFIX=https://raw.githubusercontent.com/DataTalksClub/machine-learning-zoomcamp/master/cohorts/2024/05-deployment/homework
wget $PREFIX/model1.bin
wget $PREFIX/dv.bin
```


## Question 3

Let's use these models!

* Write a script for loading these models with pickle
* Score this client:

```json
{"job": "management", "duration": 400, "poutcome": "success"}
```

What's the probability that this client will get a subscription? 

* 0.359
* 0.559
* **0.759** (answer)
* 0.959

If you're getting errors when unpickling the files, check their checksum:

```bash
$ md5sum model1.bin dv.bin
3d8bb28974e55edefa000fe38fd3ed12  model1.bin
7d37616e00aa80f2152b8b0511fc2dff  dv.bin
```

Python code for solution 

```python
import pickle

import numpy as np
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction import DictVectorizer


def open_pickle(model_file):
    model = None
    with open(model_file, 'rb') as f_in:
        model = pickle.load(f_in)
    return model


MODEL_FILEPATH = "homework/model1.bin"
DV_FILEPATH = "homework/dv.bin"


model1 = open_pickle(MODEL_FILEPATH)
dv = open_pickle(DV_FILEPATH)


X = [{"job": "management", "duration": 400, "poutcome": "success"}]

X_transformed = dv.transform(X)
y_predict = model1.predict_proba(X_transformed)

print(y_predict[0, 1])
```


## Question 4

Now let's serve this model as a web service

* Install Flask and gunicorn (or waitress, if you're on Windows)
* Write Flask code for serving the model
* Now score this client using `requests`:

```python
url = "YOUR_URL"
client = {"job": "student", "duration": 280, "poutcome": "failure"}
requests.post(url, json=client).json()
```

What's the probability that this client will get a subscription?

* **0.335** (answer)
* 0.535
* 0.735
* 0.935


This is the flask webserver app python file: `predict.py`

```python
import pickle

from flask import Flask
from flask import request
from flask import jsonify


model_file = 'model_C=1.0.bin'

with open(model_file, 'rb') as f_in:
    dv, model = pickle.load(f_in)

app = Flask('churn')

@app.route('/predict', methods=['POST'])
def predict():
    customer = request.get_json()

    X = dv.transform([customer])
    y_pred = model.predict_proba(X)[0, 1]
    churn = y_pred >= 0.5

    result = {
        'churn_probability': float(y_pred),
        'churn': bool(churn)
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)
```

This is a spythonscript which send a request to flask webserver app 

```python
import json
import requests

URL = "http://127.0.0.1:9696/predict"

client = {"job": "student", "duration": 280, "poutcome": "failure"}
res = requests.post(URL, json=client)

res_json = res.json()
print(json.dumps(res_json, indent=4))
print(res.status_code)
```

This is the output of python script file: 
```
{
    "churn": false,
    "churn_probability": 0.33480703475511053
}
200
```


## Docker

Install [Docker](https://github.com/DataTalksClub/machine-learning-zoomcamp/blob/master/05-deployment/06-docker.md). 
We will use it for the next two questions.

For these questions, we prepared a base image: `svizor/zoomcamp-model:3.11.5-slim`. 
You'll need to use it (see Question 5 for an example).

This image is based on `python:3.11.5-slim` and has a logistic regression model 
(a different one) as well a dictionary vectorizer inside. 

This is how the Dockerfile for this image looks like:

```docker 
FROM python:3.11.5-slim
WORKDIR /app
COPY ["model2.bin", "dv.bin", "./"]
```

We already built it and then pushed it to [`svizor/zoomcamp-model:3.11.5-slim`](https://hub.docker.com/r/svizor/zoomcamp-model).

> **Note**: You don't need to build this docker image, it's just for your reference.


## Question 5

Download the base image `svizor/zoomcamp-model:3.11.5-slim`. You can easily make it by using [docker pull](https://docs.docker.com/engine/reference/commandline/pull/) command.

So what's the size of this base image?

* 45 MB
* **130 MB** (answer)
* 245 MB
* 330 MB

You can get this information when running `docker images` - it'll be in the "SIZE" column.

```bash
$ docker pull svizor/zoomcamp-model:3.11.5-slim 
3.11.5-slim: Pulling from svizor/zoomcamp-model
a803e7c4b030: Pull complete 
bf3336e84c8e: Pull complete 
eb76b60fbb0c: Pull complete 
a2cee97f4fbd: Pull complete 
0358d4e17ae3: Pull complete 
fb37f8d7a667: Pull complete 
4e69cd59a5af: Pull complete 
Digest: sha256:15d61790363f892dfdef55f47b78feed751cb59704d47ea911df0ef3e9300c06
Status: Downloaded newer image for svizor/zoomcamp-model:3.11.5-slim
docker.io/svizor/zoomcamp-model:3.11.5-slim
```

```bash
$ docker images | grep zoomcamp 
svizor/zoomcamp-model                    3.11.5-slim   975e7bdca086   3 days ago    130MB
```

## Dockerfile

Now create your own Dockerfile based on the image we prepared.

It should start like that:

```docker
FROM svizor/zoomcamp-model:3.11.5-slim
# add your stuff here
```

Now complete it:

* Install all the dependencies form the Pipenv file
* Copy your Flask script
* Run it with Gunicorn 

After that, you can build your docker image.


## Question 6

Let's run your docker container!

After running it, score this client once again:

```python
url = "YOUR_URL"
client = {"job": "management", "duration": 400, "poutcome": "success"}
requests.post(url, json=client).json()
```

What's the probability that this client will get a subscription now?

* 0.287
* 0.530
* **0.757** (answer)
* 0.960

Dockerfile

```Dockerfile
FROM svizor/zoomcamp-model:3.11.5-slim

WORKDIR /app

RUN pip install --no-cache-dir pipenv

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install --system --deploy

COPY predict.py .
COPY homework/ homework/

EXPOSE 9696

ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9696", "predict:app"]
```

creating and running docker image

```bash
docker build -t mlzoomcamp-gunicorn:3.11.5-slim .
docker run --rm -p 9696:9696 mlzoomcamp-gunicorn:3.11.5-slim
```

python script.

```python
import json
import requests

URL = "http://127.0.0.1:9696/predict"

client = {"job": "management", "duration": 400, "poutcome": "success"}
res = requests.post(URL, json=client)

res_json = res.json()
print(json.dumps(res_json, indent=4))
print(res.status_code)
```

output:

```
{
    "churn": true,
    "churn_probability": 0.7590966516879658
}
200
```

## Submit the results

* Submit your results here: https://courses.datatalks.club/ml-zoomcamp-2024/homework/hw05
* If your answer doesn't match options exactly, select the closest one
