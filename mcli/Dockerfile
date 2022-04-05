FROM quay.io/bitnami/python:3.8.6-prod-debian-10-r81

WORKDIR /mcli

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY mcli.py ./

COPY utils.py ./

COPY .env ./

CMD ["python", "mcli.py", "localhost", "80"]
