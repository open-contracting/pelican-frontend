FROM python:3.8.8

WORKDIR /workdir
RUN apt-get install libxml2-dev libxslt-dev
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN groupadd -r pelican && useradd --no-log-init -r -g pelican pelican
# for storing the TOKEN_APP
RUN mkdir -p /data
RUN chown -R pelican /data

USER pelican:pelican 

COPY --chown=pelican:pelican . .
