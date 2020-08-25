FROM python:3.8-alpine as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add postgresql-dev gcc musl-dev libffi-dev

WORKDIR /code

COPY ./requirements /code/requirements

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /code/wheels -r requirements




FROM python:3.8-alpine

RUN adduser -S django

RUN apk update && apk add libpq 

WORKDIR /code
RUN mkdir /code/staticfiles
COPY --from=builder /code/wheels /wheels
COPY --from=builder /code/requirements .

RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

COPY . /code

RUN chown -R django /code

USER django

ENTRYPOINT ["/code/entrypoint.sh"]