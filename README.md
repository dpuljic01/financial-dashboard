# Financial Dashboard — Master's Thesis Project

A full-stack financial portfolio tracker built with **Vue 3 + Flask + PostgreSQL + Redis + MongoDB**.

![Financial Dashboard](/public/images/dashboard.png)

---

## Stack

| Layer      | Technology                                         |
|------------|----------------------------------------------------|
| Frontend   | Vue 3, Vue Router 4, Vuex 4, ApexCharts, vue-material |
| Backend    | Python 3.11, Flask 2.3, SQLAlchemy 2.0, gunicorn   |
| Primary DB | PostgreSQL (via psycopg2)                          |
| Cache/Auth | Redis (JWT token blacklist + Flask-Caching)        |
| Search DB  | MongoDB (ticker symbol search)                     |
| Deployment | Render (render.yaml included)                      |

---

## Local Run Guide (Fresh Machine)

### Prerequisites

- Python 3.11+
- Node.js 18+ (tested on 22)
- PostgreSQL 14+
- Redis 7+
- MongoDB (optional — only for ticker search; can be left unconfigured)

### 1. Clone & configure environment

```bash
git clone <repo-url>
cd financial-dashboard
cp .env.example .env
# Edit .env and fill in DATABASE_URL, SECRET_KEY, SECURITY_PASSWORD_SALT at minimum
```

### 2. Python backend setup

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Database setup

```bash
# Create the PostgreSQL database
createdb financial_dashboard       # or via psql: CREATE DATABASE financial_dashboard;

# Run migrations
flask db upgrade
```

### 4. Frontend setup

```bash
npm install --legacy-peer-deps --ignore-scripts
# Note: --ignore-scripts bypasses a broken postinstall hook in vue-material
```

### 5a. Run in development mode (separate processes, hot-reload)

**Terminal 1 — Backend:**
```bash
source .venv/bin/activate
flask run                          # runs on http://127.0.0.1:5000
```

**Terminal 2 — Frontend (proxies /api to Flask):**
```bash
npm start                          # runs on http://127.0.0.1:8080
```

Open `http://127.0.0.1:8080` in your browser.

### 5b. Run in production-proxy mode (Flask serves Vue)

```bash
npm run build
# Then set SHOULD_PROXY=1 in .env
flask run                          # serves everything on port 5000
```

### 6. Create a user

```bash
source .venv/bin/activate
python manage.py create_user \
  --email you@example.com \
  --first_name Your \
  --last_name Name \
  --password yourpassword \
  --role user
```

### 7. Populate ticker search (optional, requires MongoDB + IEX token)

```bash
python manage.py populate_tickers
```

---

## Deployment Guide — Render.com (free tier)

### Prerequisites

- A Render account at https://render.com
- A GitHub/GitLab repo with this code

### Steps

1. **Fork or push this repo** to your GitHub account.

2. **Create a new Blueprint** in Render:
   - Dashboard → New → Blueprint
   - Connect your repository
   - Render will detect `render.yaml` and provision: one Web Service + PostgreSQL + Redis

3. **Set the required secret env vars** in the Render dashboard (Environment tab):

   | Variable | Where to get it |
   |---|---|
   | `FINANCIAL_DASHBOARD_FE_URL` | Your Render web service URL, e.g. `https://financial-dashboard.onrender.com` |
   | `ALPHA_VANTAGE_API_KEY` | https://www.alphavantage.co/support/#api-key (free) |
   | `IEX_TOKEN` | https://iexcloud.io (sandbox is free) |
   | `MONGO_DB_CONNECTION_STRING` | MongoDB Atlas free tier (optional, for ticker search) |
   | `MAIL_SERVER`, `MAIL_USERNAME`, `MAIL_PASSWORD` | Gmail/SMTP credentials (optional, for email verification) |

4. **Deploy** — Render will:
   - `pip install -r requirements.txt`
   - `npm install --legacy-peer-deps --ignore-scripts --production=false`
   - `npm run build`
   - Start with `gunicorn -w 2 wsgi:application`

5. **Run migrations** via Render Shell or one-off job:
   ```bash
   flask db upgrade
   ```

6. **Create your first user**:
   ```bash
   python manage.py create_user --email ... --first_name ... --last_name ... --password ... --role user
   ```

---

## What Changed — Changelog

### Backend

1. **`runtime.txt`** — Updated Python version from `3.8.3` (EOL) to `3.11.14`.

2. **`server/extensions.py`** — Fixed `flask-jwt-extended` 4.x callback signatures:
   - `expired_token_loader` now requires `(jwt_header, jwt_data)` — was `(expired)`.
   - `token_in_blocklist_loader` now requires `(jwt_header, jwt_payload)` — was `(decrypted_token)`.
   - `unauthorized_loader` / `invalid_token_loader` — renamed functions to avoid duplicate definitions.
   - Replaced deprecated `flask_babelex` import with `flask_babel`.

3. **`server/config.py`** — `CACHE_TYPE = "simple"` → `"SimpleCache"` (flask-caching 2.0 renamed it).

4. **`server/apis/yfinance.py`** — Two fixes:
   - `data.get_info()` → `data.info` (method was removed from yfinance).
   - `pdr.get_quote_yahoo(ticker)` → yfinance `fast_info` (pandas-datareader 0.10.0 removed `get_quote_yahoo`).

5. **`server/mongo_db.py`** — `from flask_pymongo import pymongo` → `import pymongo` (flask-pymongo no longer re-exports the pymongo module).

6. **`server/models/user.py`** — Removed stray hardcoded JSON data block accidentally left at module level.

7. **`requirements.in` / `requirements.txt`** — Removed `flask-script` (dead, not used), `newrelic` (monitoring optional), `speaklater` (transitive dep of removed flask-babelex). Added `flask-babel` (maintained replacement for flask-babelex).

8. **`Procfile`** — Removed `newrelic-admin run-program` wrapper (requires paid New Relic key). Now: `gunicorn -w 2 wsgi:application`.

### Frontend

9. **`package.json`** — Multiple changes:
   - **Removed** `fibers` (fails to compile on Node 16+; was only needed for old Sass fiber mode).
   - **Removed** `vue-toasted` (Vue 2 only; `Vue.toasted` global doesn't exist in Vue 3).
   - **Removed** `chart.js`, `vue-chartjs`, `chartjs-plugin-zoom` (all were dead code — only ApexCharts is used in the actual components).
   - **Added** `@vue/compat ^3.4.0` (Vue 3 migration build; needed to run vue-material which is Vue 2).
   - **Added** `vue-toastification ^2.0.0-rc.5` (Vue 3 native toast replacement).
   - **Added** `postcss ^8.4.0` dev dep (explicit to avoid @vue/cli-service hoisting error).

10. **`vue.config.js`** — Replaced `configureWebpack` alias with `chainWebpack` to also configure the Vue SFC compiler in compat mode (`compatConfig: { MODE: 2 }`). This is required for `@vue/compat` to work with Vue 2 plugins like vue-material.

11. **`src/main.js`** — Replaced `vue-toasted` with `vue-toastification`. Removed non-existent `vue-material/dist/theme/default.css` import.

12. **`src/store/index.js`** — Replaced all `Vue.toasted.show(msg, {type})` calls (Vue 2 global API, undefined in Vue 3) with `useToast().success/error(msg)` from vue-toastification.

13. **`src/plugins/axios.js`** — Same replacement: `Vue.toasted` → `useToast()`.

14. **`src/assets/theme.scss`** — Changed vue-material SCSS imports from `dist/theme/` (which references non-existent `dist/base/`) to `src/theme/` (which has correct relative paths).

15. **`src/components/Compare.vue`** — Fixed Vue 3 compile error: `v-model="symbols"` on a prop is not allowed in Vue 3. Extracted `symbols` prop into `localSymbols` data property.

16. **`render.yaml`** — Rewrote to include PostgreSQL database, Redis, all required env vars (some auto-generated, some marked `sync: false` for manual entry), and `--ignore-scripts` in npm install.

17. **`.env.example`** — Updated with all required variables and descriptions.

---

## Remaining Tech Debt & Optional Improvements

- **vue-material** is Vue 2 only and unmaintained (last release 2020). The `@vue/compat` shim works but adds ~100KB. Consider migrating to [Vuetify 3](https://vuetifyjs.com/) or [PrimeVue](https://primevue.org/) when time allows.
- **flask-babelex** was replaced with **flask-babel**, but the Babel extension is only used for locale/i18n support that isn't currently active in the app. It can be removed from dependencies entirely if i18n is not needed.
- **`iexfinance==0.5.0`** — the IEX Cloud API has changed significantly. Several IEX endpoints may return errors on the free sandbox tier. The app gracefully falls back to yfinance/AlphaVantage.
- **flask-script** pattern in `manage.py` — the file already uses `flask.cli.FlaskGroup` (the modern approach). `flask-script` was removed from requirements but the manage.py CLI is fully functional.
- **News scraping (`views/news.py`)** scrapes Nasdaq HTML which is fragile. The CSS class selectors may break if Nasdaq redesigns their page.
- **SQLAlchemy 2.0** — `Model.query` is deprecated. Migrate to `db.session.execute(select(Model))` pattern for long-term compatibility.
- **npm audit** reports 48 vulnerabilities (6 low, 22 moderate, 20 high) from old transitive deps in `@vue/cli-service`. These are build-time only tools and do not affect the deployed app. Run `npm audit fix` to auto-fix what's possible.
