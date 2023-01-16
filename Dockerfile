ARG python=python:3.9-alpine

FROM ${python} as build
WORKDIR /code

COPY requirements.txt .
RUN python3 -m venv /venv
ENV PATH=/venv/bin:$PATH

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev && \
    pip install --no-cache-dir --upgrade  -r requirements.txt


FROM ${python}
COPY --from=build /venv /venv
WORKDIR /code
ENV PATH=/venv/bin:$PATH

RUN apk --no-cache --update add libffi libressl postgresql-libs gcc libc-dev

COPY . .
CMD ["alembic", "upgrade", "head"]
CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0"]
