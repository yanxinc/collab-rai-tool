FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

COPY ./app/backend/requirements.txt .

RUN pip3 install -r requirements.txt

COPY ./app/backend .
COPY ./app/helpers ./helpers

EXPOSE 8502

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8502" ,"--reload"]