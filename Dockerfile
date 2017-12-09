FROM python:3-alpine
WORKDIR /usr/src/app
# This is required to build psycopg2 (PGSQL connector)
RUN apk add --update gcc musl-dev python-dev postgresql postgresql-dev
COPY ./drf_sp_hub/requirements.txt ./
RUN pip install -r requirements.txt
# NPM deployment for webpack and all
RUN apk add --update nodejs
COPY ./drf_sp_hub/package.json ./
RUN npm install
COPY ./drf_sp_hub .
# Run webpack
RUN ./node_modules/.bin/webpack --config webpack.config.js
CMD [ "python3", "/usr/src/app/manage.py", "runserver 0.0.0.0:8000" ]
