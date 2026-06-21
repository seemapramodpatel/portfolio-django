# Laxminarayan Patel — Django Portfolio Website

## Project Structure
```
portfolio/
├── core/               ← Django project settings & URLs
│   ├── settings.py
│   └── urls.py
├── portfolio/          ← Main app
│   ├── models.py       ← ContactMessage model (PostgreSQL)
│   ├── views.py        ← index + contact API
│   ├── urls.py
│   ├── admin.py
│   └── templates/portfolio/index.html
├── manage.py
└── requirements.txt
```

---

## Step 1 — Install dependencies
```bash
pip install -r requirements.txt
```

---

## Step 2 — PostgreSQL setup
```sql
-- Run in psql as postgres user
CREATE DATABASE laxmi_portfolio;
CREATE USER portfolio_user WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE laxmi_portfolio TO portfolio_user;
```

---

## Step 3 — Environment variables
Create a `.env` file (or set these in your shell):
```
DB_NAME=laxmi_portfolio
DB_USER=portfolio_user
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST_USER=laxmihardi191@gmail.com
EMAIL_HOST_PASSWORD=your_gmail_app_password
```

> **Gmail App Password**: Go to Google Account → Security → 2-Step Verification → App Passwords → generate one for "Mail".

To load .env automatically, add this to the top of `core/settings.py`:
```python
from dotenv import load_dotenv
load_dotenv()
```

---

## Step 4 — Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Step 5 — Create admin user (optional)
```bash
python manage.py createsuperuser
```
Then visit `http://localhost:8000/admin/` to view contact form submissions.

---

## Step 6 — Run the server
```bash
python manage.py runserver
```
Open `http://localhost:8000` in your browser.

---

## Features
- ✅ Full Django backend with PostgreSQL
- ✅ Contact form saves to `contact_messages` table
- ✅ Auto-sends confirmation email to the person who fills the form
- ✅ Notifies you (Laxmi) with the submission details
- ✅ Django Admin panel to view all submissions
- ✅ Animated hero, scroll reveal, cursor glow, hover effects
- ✅ Fully responsive design
- ✅ All CV content — experience, skills, education, tools

---

## Production Deployment (optional)
- Use `gunicorn` + `nginx`
- Set `DEBUG=False` and add your domain to `ALLOWED_HOSTS`
- Use `python manage.py collectstatic` for static files
