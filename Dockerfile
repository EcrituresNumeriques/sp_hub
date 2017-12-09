FROM python:3-alpine

# This is required to build psycopg2 (PGSQL connector)
RUN apk add --update gcc git musl-dev python-dev postgresql-dev libxml2-dev libxslt-dev nodejs

# Clone the project
WORKDIR /usr/src/app

# First we install Python and node dependencies
COPY ./drf_sp_hub/package.json ./
COPY ./drf_sp_hub/requirements.txt ./

RUN pip install -r requirements.txt
RUN npm install

RUN git clone https://github.com/timoguic/sp_hub.git

WORKDIR /usr/src/app/sp_hub/drf_sp_hub

# Run webpack
RUN ../../node_modules/.bin/webpack --config webpack.config.js

EXPOSE 8000
CMD [ "python3", "/usr/src/app/sp_hub/drf_sp_hub/manage.py", "runserver", "0.0.0.0:8000" ]
