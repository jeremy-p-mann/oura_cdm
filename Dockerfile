FROM python:3.9

WORKDIR docker

COPY . .

RUN pip install pipenv
RUN pipenv install --dev
