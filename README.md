# XShop Web

The Web part of XShop's system.

## Environment Preparation

- Install Python 3.8.6 (recommendation: using Pyenv)
- Install virtualenvwrapper
- Install docker
- Install docker-compose
- Install Poetry https://python-poetry.org/
- clone the project using git
- `cd` into the project
- copy `.env.example` to `.env`, and change values (if needed)
- create a virtual environment using `mkvirtualenv xshop-web`
- run `poetry install` to install dependencies
- run `docker-compose up` to run the db container
- run `./manage.py runserver` to run the development server
- see how to contribute [here](https://github.com/egypt-shops/xshop-docs#how-to-contribute)
- write code for your task 
- write tests to validate your code
- run `./manage.py test` to run your tests
- run `flake8` to make sure your code style is ok
- push and make a PR
