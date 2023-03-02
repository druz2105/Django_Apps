FROM python:3.11-bullseye

RUN apt-get update -y

WORKDIR /app

RUN pip install -U pip pipenv

# take advantage of cached Docker layers
COPY Pipfile* ./
RUN pipenv install --verbose --system

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE 8000 90

CMD ["bash", "./docker/run.sh"]