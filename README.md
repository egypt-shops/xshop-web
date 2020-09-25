# XShop Web

The Web part of XShop's system.

## Environment Preparation

- Install Python 3.8.2 (recommendation: using Pyenv)
- Install virtualenvwrapper
- Install docker
- Install docker-compose
- Install Poetry https://python-poetry.org/
- clone the project using git
- `cd` into the project
- copy `.env.example` to `.env`, and change values (if needed)
- create a virtual environment using `mkvirtualenv xshop-web`
- run `poetry install` to install dependencies
- run `docker-compose up`
- run `./manage.py runserver`
- start coding, write tests
- run `./manage.py test` to run your tests
