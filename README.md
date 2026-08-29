# Financial Dashboard

A full-stack fintech dashboard built as part of a Master's thesis, with a Flask/Python backend, Vue.js frontend, and PostgreSQL data layer.

**Live app:** [finance.puljic.ch](https://finance.puljic.ch)
*(Frontend on Vercel, backend on Render, database on Neon Postgres)*

![Financial Dashboard](/public/dashboard.jpg)

## Stack

- **Backend:** Python, Flask
- **Frontend:** Vue.js
- **Database:** PostgreSQL (hosted on Neon)
- **Hosting:** Render (API) + Vercel (client)

## Server

### Project setup

```
pip install -r requirements.txt
```

### Run

```
export FLASK_APP=wsgi.py
flask run
```

or

```
python manage.py runserver
```

## Client

### Project setup

```
npm install
```

### Compiles and hot-reloads for development

```
npm start
```

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

### Render (API)

This repo includes a `render.yaml` file for deploying the backend on [Render](https://render.com).
Create a new **Web Service** from this repository — Render will use the build and start commands defined in that file.
Set environment variables based on `.env.example` (including the Neon Postgres connection string).

### Vercel (Client)

The Vue client is deployed separately on [Vercel](https://vercel.com), pointed at the Render API.

### Database (Neon)

PostgreSQL is hosted on [Neon](https://neon.tech). Set `DATABASE_URL` in your environment to the Neon connection string for both local development and deployment.
