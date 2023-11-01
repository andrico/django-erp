# DJANGO ERP

## Installation
Create a virtual environment and install the requirements:

```bash
python3 -m venv venv
source venv/bin/activate
pip install poetry
poetry install
```

## Run
```bash
poetry run python manage.py migrate
poetry run python manage.py runserver
```

## Create superuser
```bash
poetry run python manage.py createsuperuser
```

## Access to admin
http://localhost:8000/admin/


# WIP
## Test
```bash
poetry run python manage.py test
```

## Lint
```bash
poetry run flake8
```

## Coverage
```bash
poetry run coverage run manage.py test
poetry run coverage report
```

## Docker
```bash
docker build -t django-erp .
docker run -p 8000:8000 django-erp
```
