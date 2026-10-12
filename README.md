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

## Deploy on Vercel (live URL)

Vercel detects Django from `manage.py`, runs `collectstatic` for you and serves `/static/` from its CDN. Two things are different from a normal server: **the disk is read-only** and **SQLite cannot be used**. This project already handles that: resumes are stored in the database, and `DATABASE_URL` is required on Vercel.

1. **Create a free PostgreSQL database** (Neon works well; you can add it from the Vercel dashboard under Storage, or at neon.tech). Copy the connection string. It looks like `postgresql://USER:PASSWORD@HOST/DBNAME?sslmode=require`.
2. **Set up the tables once, from your own computer** (Windows Command Prompt):
   ```
   cd SkillPath\backend
   venv\Scripts\activate
   set DATABASE_URL=postgresql://USER:PASSWORD@HOST/DBNAME?sslmode=require
   python manage.py migrate
   python manage.py seed
   python manage.py createsuperuser
   ```
3. **Push the code to GitHub** (the `.env` file is git-ignored, keep it that way):
   ```
   cd SkillPath
   git init
   git add .
   git commit -m "SkillPath"
   git branch -M main
   git remote add origin https://github.com/YOUR-USER/skillpath.git
   git push -u origin main
   ```
4. **Import the repo in Vercel** (Add New > Project). Set **Root Directory** to `backend`. Leave the framework as detected.
5. **Add environment variables** in the Vercel project settings:
   - `SECRET_KEY` = a long random string (`python -c "import secrets;print(secrets.token_urlsafe(50))"`)
   - `DEBUG` = `False`
   - `DATABASE_URL` = your connection string (skip if the database integration added it)
6. Click **Deploy**, then open the `https://<project>.vercel.app` address. Log in at `/admin` with the superuser from step 2.

Command-line alternative: `npm i -g vercel`, then run `vercel` and later `vercel --prod` inside `backend`.

Limits on Vercel: uploads are capped at 4 MB (Vercel limits request bodies to about 4.5 MB); there is no background scheduler, so study reminders are in-app only; after any model change, run `python manage.py migrate` against the live database again.

## Deploy on Render
1. Commit the generated `*/migrations/0001_initial.py` files, push to GitHub (`.env` is git-ignored).
2. Render: create a PostgreSQL database, copy its Internal URL.
3. New Web Service: root dir `backend`, build `./build.sh`, start `gunicorn config.wsgi`.
4. Env vars: SECRET_KEY, DEBUG=False, DATABASE_URL, ALLOWED_HOSTS=your-app.onrender.com, CSRF_TRUSTED_ORIGINS=https://your-app.onrender.com
5. Resume files live on local disk, which Render wipes on redeploy. Before real users: use a persistent disk or private S3/R2 storage.

## Roles
~105 roles in 13 fields (web, mobile, data/AI, GenAI & emerging, cloud, security, QA, design, product, game/embedded, enterprise platforms, marketing, finance analytics), with NEW badges for the latest roles. Browse them at /careers/ ("Explore Roles"), see your fit, and set a goal. Edit roles in /admin; re-run `python manage.py seed` safely any time.

## Known gaps (v1)
Starter question bank is 4 questions for HTML/CSS/JavaScript/Git only (add 15+ per topic in /admin); video links are YouTube search links until an admin curates them; no settings page, resume-version compare view, or push notifications (in-app reminders only).
