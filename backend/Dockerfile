FROM python:3.9-alpine3.13

RUN adduser --disabled-password web
USER web

ENV PATH=/home/web/.local/bin:$PATH
ENV FLASK_ENV=development

COPY requirements.txt /tmp/requirements.txt
RUN pip install --user -r /tmp/requirements.txt

WORKDIR /home/web/app

CMD FLASK_APP=main:app flask run --host=0.0.0.0
