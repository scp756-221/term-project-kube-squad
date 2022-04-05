FROM quay.io/bitnami/python:3.8.6-prod-debian-10-r81

WORKDIR /playlist

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py ./
COPY middleware.py ./
COPY playlist_handler.py ./
COPY .env ./

EXPOSE 6000

CMD ["python", "app.py", "6000"]
