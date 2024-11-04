# This is a basic Dockerfile to run the app.py
# I am running here a lightweight image to run python for the demonstration
FROM python:3.9-slim    

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
