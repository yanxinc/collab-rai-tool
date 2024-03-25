# collab-rai-tool


## Setup
- Environment & Dependencies
  ```bash
    $ python -m venv .venv
    $ source .venv/bin/activate
    $ pip install -r requirements.txt
  ```
- Deploy using Docker
  <!-- ```
    $ docker build -t streamlit .
    $ docker run -p 8501:8501 streamlit
  ``` -->
  ```bash
    $ docker-compose up -d --build
  ```
  <!-- docker-compose up -d --build --remove-orphans -->

