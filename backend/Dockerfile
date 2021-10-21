FROM python:3.8.8

WORKDIR /usr/src/app
RUN apt-get install libxml2-dev libxslt-dev
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir /data

ENTRYPOINT [ "" ]