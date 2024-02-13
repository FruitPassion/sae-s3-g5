#!/var/www/FichesProd/.env/bin/python3.10

import sys

sys.path.insert(0, '/var/www/FichesProd')

activate_this = '/var/www/FichesProd/.env/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))
    
from app import create_app
application = create_app('prod')