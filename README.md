# Aurelia — The Curated World

A premium Flask travel-concierge web app built for the Selenium Testing assignment.
Dark luxe theme, glassmorphism, interactive map, weather widget, wishlist, profiles,
trip itineraries, dashboard — wired up to a 40-case Selenium suite.

> **Stack:** Flask 3 · SQLAlchemy 2 · Flask-Login · Flask-WTF · Jinja2 · Leaflet.js · Selenium · Docker · MySQL/SQLite

---

## Features

### User-facing
- **Hero landing** with parallax, animated headline, and global search
- **Catalogue** of curated destinations across **5 categories** (Beach · Mountain · City · Adventure · Cultural)
- **Search & filter** — keyword, category, minimum rating
- **Interactive world map** (Leaflet + dark CARTO tiles + gold pins)
- **Destination detail** with photo gallery + lightbox, live weather widget (Open-Meteo, no key required), reviews + threaded replies
- **Clickable star-rating widget** for posting reviews
- **Wishlist** — AJAX heart toggle, dedicated saved-for-later page
- **User profiles** with initials avatar, bio, animated stat counters, recent reviews
- **Trip itineraries** — start/end dates, daily-spend calculator, multi-stop plans, notes, budget
- **Dashboard** — six stat counters, top-rated leaderboard, most-reviewed list, category breakdown bars, top reviewers
- **Toast notifications**, **dark/light theme toggle** (persisted), custom **404 page**

### Engineering
- App factory pattern (`create_app()`)
- SQLAlchemy 2.0 models with relationships, cascades, computed properties
- Reusable Jinja partials (`_card.html`)
- Vanilla CSS with CSS variables for theming — no build step
- Vanilla JS with `IntersectionObserver` for reveal animations and counters
- CSRF disabled inside the app config so Selenium tests can submit forms
- Dual-database support (SQLite by default, MySQL via env vars)

---

## Project Structure

```
Assignment_3/
├── app.py                    # Flask app factory + 24 routes
├── models.py                 # User, Destination, DestinationImage,
│                             # Review, Reply, TravelPlan, Wishlist
├── forms.py                  # WTForms (registration, login, destination,
│                             # review, reply, plan, profile, search)
├── populate_db.py            # Seeds 24 destinations, 5 users, 77 reviews,
│                             # 31 replies, 3 plans, 21 wishlist items
├── application.py            # Thin alias for some PaaS deployments
├── requirements.txt          # Python 3.12-compatible dependency pins
├── Dockerfile                # Python 3.10 + Chromium + chromedriver
├── docker-compose.yml        # web + MySQL 8 services
├── Jenkinsfile               # CI: docker build → run tests
├── Procfile                  # Heroku/Procfile-style start cmd
├── static/
│   ├── css/luxe.css          # Premium dark theme (~520 lines)
│   └── js/app.js             # Theme toggle, AJAX wishlist, stars,
│                             # weather, lightbox, scroll-reveal
├── templates/
│   ├── base.html             # Shell with luxe nav + footer + lightbox
│   ├── _card.html            # Reusable destination-card partial
│   ├── index.html            # Hero, stats, categories, trending, top-rated
│   ├── destinations.html
│   ├── destination_detail.html
│   ├── destination_form.html
│   ├── category.html         # Filter by category pill
│   ├── search.html           # Keyword + category + min-rating
│   ├── login.html
│   ├── register.html
│   ├── profile.html          # Avatar, stats, bio editor, recent reviews
│   ├── wishlist.html
│   ├── travel_plans.html
│   ├── plan_detail.html      # Itinerary + budget calculator
│   ├── create_plan.html
│   ├── add_destination_to_plan.html
│   ├── map.html              # Leaflet world map
│   ├── dashboard.html        # Insights + leaderboards
│   └── 404.html
└── tests/
    └── test_app.py           # 40 Selenium tests
```

---

## Quick start

### 1. Local (SQLite, fastest)

Requires **Python 3.12** (3.10 / 3.11 also fine). Python 3.14 is currently
unsupported by some pinned native dependencies.

```bash
git clone <your-repo-url>
cd Assignment_3

python3.12 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt

python populate_db.py             # seed demo content
python app.py                     # http://127.0.0.1:5000
```

### 2. Docker Compose (Flask + MySQL 8)

The `web` service uses the included Dockerfile; the `db` service is MySQL 8
with auto-created `flask_app_db` database.

By default the Dockerfile's `CMD` runs the test suite. To serve the app
instead, override `command` in `docker-compose.yml`:

```yaml
services:
  web:
    command: python app.py
```

Then:

```bash
docker-compose up --build
```

### 3. Run the Selenium suite

In one terminal: `python app.py`
In another:

```bash
pip install selenium pytest
pytest -v tests/test_app.py
```

The suite has **40 tests** (15 original + 25 new) and runs against a live
server at `http://127.0.0.1:5000` using **headless Chrome**. Make sure
`chromedriver` is on your PATH (or use the Docker image, which bundles it).

---

## Demo accounts

After running `python populate_db.py`:

| Username | Email                | Password |
| -------- | -------------------- | -------- |
| test     | test@test.com        | 1234     |
| amelia   | amelia@aurelia.com   | 1234     |
| jasper   | jasper@aurelia.com   | 1234     |
| rumi     | rumi@aurelia.com     | 1234     |
| noor     | noor@aurelia.com     | 1234     |

---

## Routes

| Path                                | Auth      | Description                          |
| ----------------------------------- | --------- | ------------------------------------ |
| `/`                                 | public    | Hero, stats, trending, top-rated     |
| `/destinations`                     | public    | Full catalogue                       |
| `/destination/<id>`                 | public    | Detail + reviews + weather + replies |
| `/add_destination`                  | required  | Add a new destination                |
| `/edit_destination/<id>`            | required  | Edit destination                     |
| `/delete_destination/<id>` (POST)   | required  | Delete destination                   |
| `/category/<name>`                  | public    | Filter by category                   |
| `/search`                           | public    | Keyword + filters                    |
| `/map`                              | public    | Leaflet world map                    |
| `/dashboard`                        | public    | Stats & leaderboards                 |
| `/profile/<username>`               | public    | Profile + stats + reviews            |
| `/wishlist`                         | required  | Saved destinations                   |
| `/wishlist/toggle/<id>` (POST)      | required  | Toggle save (AJAX-aware)             |
| `/review/<id>/reply` (POST)         | required  | Threaded reply                       |
| `/travel_plans`                     | required  | List my trips                        |
| `/plan/<id>`                        | required  | Trip detail + budget calc            |
| `/create_plan` · `/edit_plan/<id>`  | required  | Create / edit a plan                 |
| `/delete_plan/<id>` (POST)          | required  | Delete a plan                        |
| `/add_destination_to_plan/<id>`     | required  | Add a stop                           |
| `/remove_from_plan/<plan>/<dest>`   | required  | Remove a stop                        |
| `/login` · `/register` · `/logout`  | mixed     | Auth                                 |

---

## Configuration

Environment variables read by `app.py`:

| Variable        | Default                                         | Notes                            |
| --------------- | ----------------------------------------------- | -------------------------------- |
| `SECRET_KEY`    | `tourism-explorer-secret-key-12345`             | Override in production           |
| `DATABASE_URL`  | unset                                           | Full SQLAlchemy URI; takes over  |
| `DB_HOST`       | unset                                           | Triggers MySQL build-up          |
| `DB_USER`       | `root`                                          |                                  |
| `DB_PASSWORD`   | `rootpassword`                                  |                                  |
| `DB_NAME`       | `flask_app_db`                                  |                                  |

If neither `DATABASE_URL` nor `DB_HOST` is set, the app falls back to
`sqlite:///tourism.db` so a fresh clone runs with zero infrastructure.

---

## Selenium suite

`tests/test_app.py` contains 40 cases covering:

- Auth: register, login (valid + invalid), logout, session persistence
- Navigation: home, links present, multi-page, refresh, brand link
- Catalogue: destinations grid, cards render, category pills
- Search: form filters, keyword query, results render
- Map: page loads, `#map` element present
- Dashboard: stats counters, leaderboard sections
- Profile: page loads, stats counters
- Wishlist: redirects when logged out, loads when logged in
- Plans: form has date + budget fields
- Theme toggle, footer brand, custom 404 page
- Full register → login → wishlist flow

All pages expose stable IDs (`#map`, `#dashboard-heading`, `#profile-username`,
`#wishlist-heading`, `#search-heading`, `#category-heading`, `#plan-title`)
plus class hooks (`.brand`, `.dest-card`, `.theme-toggle`, `.luxe-footer`,
`.cat-pill`, `.star-rating`, `[data-weather]`, `[data-count]`) so tests stay
resilient to copy changes.

---

## Tech notes

- **CSRF is intentionally disabled** in `app.py` (`WTF_CSRF_ENABLED = False`)
  so Selenium can submit forms without scraping tokens. Re-enable for
  production deployment.
- **Passwords use `werkzeug.security.generate_password_hash`** (PBKDF2-SHA256
  by default).
- The **weather widget** calls `api.open-meteo.com` from the browser — no API
  key needed. If the user is offline it falls back gracefully.
- The **map** uses CARTO's free dark tile server via OpenStreetMap.
- All images are pulled from **Unsplash** via direct URLs (no API key).

---

## License

Coursework / educational use.
