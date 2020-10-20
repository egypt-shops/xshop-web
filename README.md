# XShop Web

The Web part of XShop's system.

## Environment Preparation

- Install Python 3.8.6 (recommendation: using [Pyenv](https://github.com/pyenv/pyenv))
- Install [docker](https://www.docker.com/products/docker-desktop)
- Install [docker-compose](https://docs.docker.com/compose/)
- Install [Poetry](https://python-poetry.org/)
- clone the project using [git](https://git-scm.com/downloads)
- [`cd`](https://linuxize.com/post/linux-cd-command/) into the project
- copy `.env.example` to `.env`, and change values (if needed)
- run `poetry install` to install dependencies (which will create a [virtualenv](https://virtualenv.pypa.io/en/latest/) automatically)
- run `poetry shell` to activate the virtual environment
- run `docker-compose up` to run the db container (and leave it running)
- open another terminal inside the project's folder and activate the virtualenv using `poetry shell` again
- apply the migrations by issueing `./manage.py migrate`
- then run `./manage.py runserver` to run the development server
- Visit the project on this URL: [localhost:8000](http://localhost:8000)
- You should see the project running without any problems
- If you face any problem doing the above steps ask for help

## Contribute

- see how to contribute [here](https://github.com/egypt-shops/xshop-docs#how-to-contribute)
- Think about your task, and gather information before you code
- Ask the team for help if you can't get something right
- write code for your task
- write tests to validate your code
- run `./manage.py test` to run your tests
- run `flake8` to make sure your code style is ok
- push and make a Pull Request
- Wait for code review

## Project Structure

├── [api.http](api.http) API specs through examples directly from vscode, [This extension needed](https://marketplace.visualstudio.com/items?itemName=humao.rest-client)<br>
├── [docker-compose.yml](docker-compose.yml) local dev containers specs<br>
├── [manage.py](manage.py)<br>
├── [poetry.lock](poetry.lock) poetry lock file which contains project's dependencies<br>
├── [pyproject.toml](pyproject.toml) python's project specs new standard<br>
├── [README.md](README.md) This file<br>
├── [Procfile](Procfile) Deployment to heroku<br>
├── [project](project) project dir created by django-admin<br>
│   ├── [settings.py](project/settings.py) Project settings <br>
│   ├── [urls.py](project/urls.py) Project URL Paths<br>
├── [static](static) css/js/img files that help with the design<br>
├── [templates](templates) HTML templates. A folder for each app inside the project<br>
└── [xshop](xshop) Container of all django apps in the project<br>
    ├── [core](xshop/core) Core app that contains essential functionalities like admin edits and management commands<br>
    ├── [invoices](xshop/invoices) Every thing related to invoices should be here<br>
    ├── [orders](xshop/orders) orders-related logic<br>
    ├── [pages](xhsop/pages) static/semi-static pages like (about, home, contact)...etc<br>
    ├── [products](xshop/porducts) products-related code<br>
    ├── [shops](xshop/shops) shops-related code (models, views, apis, etc..)<br>
    ├── [users](xshop/users) users-related logic (models, views, api, etc..)<br>
    └── [utils](xshop/utils) project-wide utilities

**Please Note that each app contains:**

- an _api_ package which contains api-related stuff: _serializers_, _views_, and _urls_
- a _tests_ packages that contains:
  - a _test_api_ package which contains
    - a _test_views_ module for testing api views
    - a _test_serializers_ module for testing api serializers
  - _test_views_ module for testing app's ordinary views
  - _test_models_ for testing app's models
