FROM python:3.9-alpine

ARG PYGANDI_VERSION=0.1.2
ENV APIKEY=myapikey

#RUN mkdir -v /usr/src/venv
# {dist}-{version}(-{build})?-{python}-{abi}-{platform}.whl

# upgrade pip
RUN python3 -m pip install --user --upgrade pip
RUN python3 -m pip install --user virtualenv

COPY dist/*.whl /usr/src/
RUN python3 -m pip install \
         --no-cache-dir \
         --user \
        #  --dest /usr/local/bin/ \
         --no-cache \
         --only-binary \
         /usr/src/*.whl

RUN rm -f /usr/src/*.whl
#RUN /usr/src/venv/bin/python3 -c "import requests; print(requests.__version__)"

#RUN apt install -y libcurl3-gnutls
#RUN adduser --uid 10000 pyjob

WORKDIR /usr/local/bin

RUN ls -l /usr/local/bin

#USER pyjob

CMD ["/usr/local/bin/pygandi", "--help"]
