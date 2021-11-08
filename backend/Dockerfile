FROM python:3.8

# Required by lxml Python package.
RUN apt-get update && apt-get install -y --no-install-recommends \
      libxml2-dev \
      libxslt-dev \
   && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN groupadd -r runner && useradd --no-log-init -r -g runner runner

# See TOKEN_PATH in settings.py.
RUN mkdir -p /data
RUN chown -R runner:runner /data

WORKDIR /workdir
USER runner:runner
COPY --chown=runner:runner . .

RUN python manage.py compilemessages
