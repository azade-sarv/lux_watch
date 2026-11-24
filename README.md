# Luxury Watch Store

A watch-store API built with Django and Django REST Framework.

## Requirements

- Python 3.12 or later
- PostgreSQL

## Setup on Windows PowerShell

Run these commands from the project root:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell does not allow activating the virtual environment, replace `python` in the commands below with `.\.venv\Scripts\python.exe`. Install dependencies this way:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Environment and database configuration

Copy the example environment file and generate a unique Django secret key:

```powershell
Copy-Item .env.example .env
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Put the generated key in `DJANGO_SECRET_KEY` in `.env`. The project uses PostgreSQL by default. Create a database named `luxury_watch` and set `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, and `DB_PORT` in `.env` to match your local PostgreSQL configuration. `.env` is ignored by Git; never commit it or share production credentials.

## Run the project

After installing dependencies and configuring `.env` and PostgreSQL:

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The development server runs at `http://127.0.0.1:8000/` by default. The admin site is available at `http://127.0.0.1:8000/admin/`.

## Available API endpoints

- `GET /api/products/` — List products
- `GET /api/products/<slug>/` — Get product details
- `GET /api/luxury-special/` — List available luxury special products
- `GET /api/me/wishlist/` — Get the authenticated user's wishlist

## Checks and tests

```powershell
python manage.py check
python manage.py test
```

The PostgreSQL user must have permission to create a test database to run the test suite.

## Deployment note

`runserver` is for development only. For deployment, set `DJANGO_DEBUG=False`, provide the production `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, and `CSRF_TRUSTED_ORIGINS`, and configure database credentials through environment variables. HTTPS redirects, HSTS, and secure session/CSRF cookies are enabled by default when debug mode is off. Deploy behind HTTPS; configure `SECURE_HSTS_SECONDS` only after confirming the domain is permanently served over HTTPS. Set `SECURE_HSTS_INCLUDE_SUBDOMAINS=True` and `SECURE_HSTS_PRELOAD=True` only if every subdomain is permanently HTTPS and you intend to opt into browser preloading. Set `MAILER_BACKEND` to Django's SMTP backend and provide `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, and the appropriate TLS/SSL setting. The console email backend in `.env.example` is for local development only.
