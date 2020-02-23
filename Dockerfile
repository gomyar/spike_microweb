FROM alpine

RUN apk add --update \
    python \
    python-dev \
    py-pip \
  && pip install virtualenv \
  && rm -rf /var/cache/apk/*

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY ./src/ /app/

EXPOSE 5000
CMD cd /app && /app/prod_server.sh
