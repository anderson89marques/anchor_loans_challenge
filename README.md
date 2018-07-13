wedding_gallery
===============

Getting Started
---------------

- Clone project

    git clone https://github.com/anderson89marques/anchor_loans_challenge.git

- Change directory into your newly created project.

    cd wedding_gallery

- Create a Python virtual environment.

    python3 -m venv env

- Upgrade packaging tools.

    env/bin/pip install --upgrade pip setuptools

- Install the project in editable mode with its testing requirements.

    env/bin/pip install -e ".[testing]"

- Configure the database.

    env/bin/initialize_wedding_gallery_db development.ini

- Run your project's tests.

    env/bin/pytest

- Run your project.

    env/bin/pserve development.ini
