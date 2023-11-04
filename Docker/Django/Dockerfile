FROM python:3.9-alpine

WORKDIR /src
EXPOSE 8000

RUN apk add --no-cache gcc musl-dev linux-headers

COPY ./Django_app /src

RUN pip3 install --no-cache-dir --upgrade -r /src/requirements.txt

ENV SECRET_KEY="django-insecure-)shu%nps*iq9ojvrakaz5qj+!n)m-0kk0%2-g^c4u3^w=hno"
ENV DEBUG=1

RUN python manage.py migrate

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "main.wsgi"]

