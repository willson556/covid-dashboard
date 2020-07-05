# United States COVID-19 Data Dashboard

An interactive COVID-19 data dashboard that plots the derivative of key metrics.

See the published site at [data.thomasewillson.com](https://data.thomasewillson.com).

## Data Sources

- [The COVID Tracking Project at _The Atlantic_](https://covidtracking.com)
- [COVID-19 Dashboard by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19)

## Build and Run

### Development

#### Install Dependencies

```bash
git clone https://github.com/willson556/covid-dashboard.git
cd covid-dashboard
cp debug.env .env

# Python 3 Dependencies
pip3 install -r requirements.txt # I recommend doing this in a virtualenv.

# Node.js Dependencies
cd src/covid_dashboard
npm install -g ember-cli
npm install
```

#### Run Dev Server

This project requires two processes to be running for development; a flask dev server for the backend and an ember-cli dev server for the frontend.

Backend:
```bash
cd covid-dashboard
flask run # Starts backend at http://localhost:5000
```

Frontend:
```bash
cd covid-dashboard/src/covid_dashboard
ember serve --proxy http://localhost:5000 # Start frontend dev server at http://localhost:4200 while proxying api requests to the backend.
```

Once both of those are running, the site should be accessible at http://localhost:4200. The dev servers will automatically reload files as they change.

### Production

This project is designed to be deployed using Docker Compose. Simply run

```bash
git clone https://github.com/willson556/covid-dashboard.git
cd covid-dashboard
docker-compose up --build -d
```

to deploy. That will run the site at <http://localhost:1337>. To update, run

```bash
cd covid-dashboard
git pull
docker-compose up --build -d
```