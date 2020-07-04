FROM sergiolepore/ember-cli:3.1.4-node_10.1.0 AS builder

ADD src/covid_dashboard /opt/covid_dashboard

WORKDIR /opt/covid_dashboard
RUN ember build --environment=production --output-path ../static

FROM python3.8
COPY src/covid_api /covid_api
COPY production.env /covid_api/.env
COPY requirements.txt /covid_api

WORKDIR /covid_api
RUN pip install -r requirements.txt
RUN pip install waitress
CMD ["waitress-serve", "--call", "covid_api"]
