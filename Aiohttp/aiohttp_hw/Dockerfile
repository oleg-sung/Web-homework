FROM python:3.9-alpine

WORKDIR /src
EXPOSE 8080

RUN apk add --no-cache gcc musl-dev linux-headers

COPY requirements.txt .

RUN pip3 install --no-cache-dir --upgrade -r /src/requirements.txt

COPY . /src