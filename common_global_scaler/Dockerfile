FROM python:3.11

WORKDIR /app

COPY src ./src

COPY requirements.txt ./

RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=0
CMD ["python", "./src/main.py"]

