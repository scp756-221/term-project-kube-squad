FROM quay.io/bitnami/python:3.8.6-prod-debian-10-r81

WORKDIR /subcription

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY .env ./

COPY middleware.py  ./

COPY sub_app.py ./

COPY sub_handler.py ./

EXPOSE 4000

CMD ["python", "sub_app.py", "4000"]
