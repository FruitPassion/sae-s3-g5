from flask import Blueprint, render_template

from model.personnel import getAllPersonnel

auth = Blueprint('auth', __name__)


@auth.route('/')
def index():
    personnel = getAllPersonnel()
    return render_template('auth/index.html', personnel=personnel)
