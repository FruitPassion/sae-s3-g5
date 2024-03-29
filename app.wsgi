#!/var/www/__AREMPLACERSN__/.env/bin/python3.10

import sys

sys.path.insert(0, '/var/www/__AREMPLACERSN__')

activate_this = '/var/www/__AREMPLACERSN__/.env/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))
    
from app import create_app
application = create_app('prod')