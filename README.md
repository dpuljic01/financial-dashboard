# Financial Dashboard

A full-stack fintech dashboard built as part of a Master's thesis, with a Flask/Python backend, Vue 3 frontend, and PostgreSQL data layer.

**Live app:** [finance.puljic.ch](https://finance.puljic.ch)
*(Single Render web service — Flask serves both the API and the built Vue app; PostgreSQL on Neon)*

![Financial Dashboard](/public/dashboard.jpg)

## Stack

- **Backend:** Python, Flask, SQLAlchemy, Flask-Migrate (Alembic)
- **Frontend:** Vue 3, Vuex, Vue Router
- **Charts:** TradingView [lightweight-charts](https://github.com/tradingview/lightweight-charts) (price/performance/compare charts), Chart.js (allocation donut)
- **Market data:** yfinance (primary), [Alpha Vantage](https://www.alphavantage.co/) (fallback for company profile/quote data when yfinance is rate-limited), IEX Cloud
- **Database:** PostgreSQL (hosted on [Neon](https://neon.tech)), Redis (response caching)
- **Hosting:** Render — one web service builds and serves both the API and the client

## Server

### Project setup

```
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in the values (DB connection string, API keys for Alpha Vantage/IEX, Resend for transactional email, etc.).

### Run

```
export FLASK_APP=wsgi.py
flask run
```

or

```
python manage.py runserver
```

### Database migrations

This project uses Flask-Migrate. After pulling a change that touches a model, apply it locally with:

```
python manage.py db upgrade
```

**Nothing in the deploy pipeline runs this automatically in production** — `render.yaml`'s `startCommand` runs migrations before starting `gunicorn` on every boot, but that only happens on its own if the Render service is Blueprint-synced to this repo. If the service was set up by hand in Render's dashboard instead, its Start Command won't pick up changes to `render.yaml` automatically, and a forgotten migration will surface in production as `column ... does not exist` on the very next request that touches that table — as happened once already. If unsure, check the service's Start Command in the Render dashboard matches `render.yaml`, or run `python manage.py db upgrade` manually via Render's Shell after a deploy that adds a migration.

## Client

### Project setup

```
npm install
```

### Compiles and hot-reloads for development

```
npm start
```

To develop against a local Flask backend instead of mocking, set `VUE_APP_API_URL` in `.env` to your local API (e.g. `http://127.0.0.1:5000/api`). `SHOULD_PROXY` controls whether the Flask app proxies requests to the built frontend — run `npm run build` first for that to have something to serve.

### Compiles and minifies for production

```
npm run build
```

### Lints and fixes files

```
npm run lint
```

### Customize configuration

See [Configuration Reference](https://cli.vuejs.org/config/).

## Deployment

### Render (single service)

This repo includes a `render.yaml` file for deploying as one **Web Service** on [Render](https://render.com). Its build step installs Python dependencies and also builds the Vue client (`npm run build`); Flask then serves the built frontend alongside the API from the same process. Set environment variables based on `.env.example` (including the Neon Postgres connection string) in the Render dashboard.

The custom domain (`finance.puljic.ch`) is a CNAME pointed at the Render service's default `onrender.com` URL, configured through the domain's own DNS provider.

### Database (Neon)

PostgreSQL is hosted on [Neon](https://neon.tech). Set `DATABASE_URL` in your environment to the Neon connection string for both local development and deployment.
