FROM python:3.10.7-slim-bullseye

WORKDIR /app
COPY requirements.txt requirements.txt
COPY lib lib
COPY app.py app.py

RUN pip3 install -r requirements.txt

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]