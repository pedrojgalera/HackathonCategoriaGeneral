FROM alpine

RUN apk add --no-cache python3
RUN python3 -m ensurepip
RUN rm -r /usr/lib/python*/ensurepip
RUN pip3 install pytemperature requests

COPY . /app

WORKDIR /app

CMD python3 api.py
