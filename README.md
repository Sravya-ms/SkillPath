# SkillPath - Student Placement Readiness Tracker

Django + SQLite (local) / PostgreSQL (deploy). Theme: "The Trail" (ink-green, ember orange, moss, glacier teal).

## Run locally (Windows Command Prompt)
```
cd SkillPath\backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations students resumes careers learning jobs
python manage.py migrate
python manage.py seed
python manage.py createsuperuser
python manage.py test
python manage.py runserver
```
Open http://127.0.0.1:8000 (admin at /admin). On macOS/Linux use `source venv/bin/activate`.

## Environment (.env)
SECRET_KEY, DEBUG, ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS, DATABASE_URL (optional - SQLite is used when unset).

## Deploy on Render
1. Commit the generated `*/migrations/0001_initial.py` files, push to GitHub (`.env` is git-ignored).
2. Render: create a PostgreSQL database, copy its Internal URL.
3. New Web Service: root dir `backend`, build `./build.sh`, start `gunicorn config.wsgi`.
4. Env vars: SECRET_KEY, DEBUG=False, DATABASE_URL, ALLOWED_HOSTS=your-app.onrender.com, CSRF_TRUSTED_ORIGINS=https://your-app.onrender.com
5. Resume files live on local disk, which Render wipes on redeploy. Before real users: use a persistent disk or private S3/R2 storage.

## Known gaps (v1)
Starter question bank is 4 questions for HTML/CSS/JavaScript/Git only (add 15+ per topic in /admin); video links are YouTube search links until an admin curates them; no settings page, resume-version compare view, or push notifications (in-app reminders only).
