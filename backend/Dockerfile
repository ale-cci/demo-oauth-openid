FROM alpine:3.13 as ssh-keys
RUN apk update && apk add --no-cache openssh-keygen
RUN ssh-keygen -t rsa -b 4096 -f /root/.ssh/id_rsa

FROM python:3.9-alpine3.13
RUN adduser --disabled-password web
RUN apk update && apk add --no-cache build-base openssl-dev libffi-dev

USER web
RUN mkdir /home/web/.ssh
COPY --from=ssh-keys --chown=web:web /root/.ssh/id_rsa* /home/web/.ssh

# https://www.googleapis.com/oauth2/v3/certs

ENV PATH=/home/web/.local/bin:$PATH
ENV FLASK_ENV=development


ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
COPY requirements.txt /tmp/requirements.txt
RUN pip install --user -r /tmp/requirements.txt

WORKDIR /home/web/app

CMD FLASK_APP=main:app flask run --host=0.0.0.0
