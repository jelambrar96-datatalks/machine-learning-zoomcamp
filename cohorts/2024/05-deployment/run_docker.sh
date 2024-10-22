docker build -t mlzoomcamp-gunicorn:3.11.5-slim .
docker run --rm -p 9696:9696 mlzoomcamp-gunicorn:3.11.5-slim
