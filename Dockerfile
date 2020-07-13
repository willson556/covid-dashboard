FROM node:14.5.0 AS builder
RUN npm install -g ember-cli

ADD src/covid_dashboard /opt/covid_dashboard
WORKDIR /opt/covid_dashboard
RUN npm install
RUN ember build --environment=production --output-path /build-output
RUN ls /build-output

FROM python:3.8

COPY requirements.txt /app/covid_api/
WORKDIR /app/covid_api
RUN pip install -r requirements.txt

COPY src/covid_api .
COPY production.env .env
COPY --from=builder /build-output static/

WORKDIR /app
COPY src/wsgi.py .
COPY prod_run.sh .
COPY uwsgi.ini .
EXPOSE 3031
CMD ["bash", "prod_run.sh"]
