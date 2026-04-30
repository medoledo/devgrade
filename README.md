# DevGrade — University Project Marketplace

## Setup Instructions

### 1. Clone & Install
```bash
pip install -r requirements.txt
```

### 2. Configure Settings
- Set `SECRET_KEY` in settings.py
- Set `ALLOWED_HOSTS` to your domain
- Switch to PostgreSQL for production

### 3. Run Migrations
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

### 4. Deploy on VPS (Nginx + Gunicorn)
```bash
gunicorn devgrade.wsgi:application --bind 0.0.0.0:8000
```

## Admin Panel
Visit `/admin` — add projects, set Gumroad links, manage custom orders.

## Adding a New Project
1. Go to Admin → Projects → Add Project
2. Fill title, description, prices
3. Add features (inline)
4. Add screenshots (inline)
5. Paste your Gumroad product URL
6. Set is_published = True
