FROM python:3.10.5

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libc6-dev \
    libffi-dev \
    libpq-dev \
    postgresql-client \
    redis-tools
RUN pip install gunicorn
RUN pip install psycopg2-binary
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y postgresql-client redis-tools


COPY . .

ENV DJANGO_SETTINGS_MODULE=vard.settings
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH /app

RUN python manage.py collectstatic --noinput


CMD ["gunicorn", "vard.wsgi:application", "--bind", "0.0.0.0:8000"]
