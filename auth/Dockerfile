FROM quay.io/bitnami/python:3.8.6-prod-debian-10-r81

WORKDIR /auth

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py ./

COPY .env ./

COPY middleware.py  ./

COPY auth_handler.py  ./

EXPOSE 3000

CMD ["python", "app.py", "3000"]
