# StudyTrack

A simple Django web app to track your university/school subjects, exams and grades.

## What it does

- Add your subjects with professor name, semester and credits
- Schedule exams and track their status (upcoming, passed, failed, retake)
- Record grades and see your average percentage
- Organise subjects into study groups

## Setup

### Requirements
- Python 3.10+
- PostgreSQL

### Steps

```bash
# 1. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install django psycopg2-binary

# 3. Create the database in PostgreSQL
# psql -U postgres
# CREATE DATABASE studytrack_db;

# 4. Run migrations
python manage.py migrate

# 5. Start the server
python manage.py runserver
```

Open http://127.0.0.1:8000 in your browser.

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| DB_NAME | studytrack_db | Database name |
| DB_USER | postgres | Database user |
| DB_PASSWORD | postgres | Database password |
| DB_HOST | localhost | Database host |
| DB_PORT | 5432 | Database port |

## Project structure

```
courses/   - Subject and StudyGroup models
exams/     - Exam model
grades/    - Grade model
templates/ - HTML templates
static/    - CSS
```
## Highlights
* Managed *Many-to-One* relationships between Subjects, Exams, and Grades.
* Automated *GPA and weighted* average calculations based on credit hours and exam results.
* Implemented a custom logic workflow to track exams (Upcoming ➔ Passed ➔ Failed ➔ Retake).

