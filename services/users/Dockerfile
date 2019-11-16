FROM python:3.7.2-alpine

# set working directory
WORKDIR /usr/src/app

RUN apk add --no-cache postgresql-libs gcc musl-dev postgresql-dev

# add and install requirements
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# add app
COPY . /usr/src/app

# run server
CMD ["/usr/src/app/entrypoint.sh"]