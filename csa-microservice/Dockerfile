FROM python:3.8 AS venv-image

RUN python -m venv /tmp/venv
# Make sure we use the virtualenv:
ENV PATH /tmp/venv/bin:$PATH

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install psycopg2-binary

FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir -p /applis/prod/server

WORKDIR /applis/prod/server

COPY . /applis/prod/server

COPY --from=venv-image /tmp/venv /tmp/venv

# Make sure we use the virtualenv:
ENV PATH /tmp/venv/bin:$PATH


ADD entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh", "--"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]