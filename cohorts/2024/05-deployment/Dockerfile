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
