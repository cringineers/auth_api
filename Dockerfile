FROM docker.io/python:3.10-alpine
ENV PATH /app/venv/bin:$PATH
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN python -m venv venv && pip install --no-cache-dir -r requirements.txt
COPY . /app
ENTRYPOINT ["python", "run.py"]
