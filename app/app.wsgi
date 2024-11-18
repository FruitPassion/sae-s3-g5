#!/usr/src/app/.venv/bin/python3.11

import sys

sys.path.insert(0, '/usr/src/app')

activate_this = '/usr/src/app/.venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from app import create_app

application = create_app()
