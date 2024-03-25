FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/streamlit/streamlit-example.git .

COPY ./app/frontend/requirements.txt .

RUN pip3 install -r requirements.txt

COPY .streamlit .streamlit
COPY ./app/frontend ./frontend
COPY ./app/helpers ./helpers
COPY ./app/frontend_test_version ./frontend

EXPOSE 8503

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "frontend/app.py", "--server.port=8503", "--server.address=0.0.0.0"]