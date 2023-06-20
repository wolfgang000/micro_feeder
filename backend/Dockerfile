FROM python:3.11.4 as requirements-stage

WORKDIR /tmp
RUN pip install poetry==1.5.1
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.11.4

COPY . /app
WORKDIR /app

COPY Procfile .
COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=:/app/src

CMD /app/entrypoint.sh