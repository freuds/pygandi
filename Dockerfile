# Build whl on pipenv docker image
FROM kennethreitz/pipenv as build

ADD . /app
WORKDIR /app

RUN pipenv install --dev \
 && pipenv lock -r > requirements.txt \
 && pipenv run python setup.py bdist_wheel

# build on python alpine
FROM python:3.9-alpine

ARG version=0.1.3

COPY --from=build /app/dist/pygandi-$version-py39-none-any.whl .

RUN python3 -m pip install \
    --no-cache-dir \
    --no-cache \
    /pygandi-$version-py39-none-any.whl

ENTRYPOINT [ "python3", "./usr/local/bin/pygandi" ]