from flask import Blueprint, render_template

from model.personnel import getAllPersonnel

auth = Blueprint('auth', __name__)


@auth.route('/hello-world')
def hello_world():
    return "Hello World"


@auth.route('/')
def index():
    personnel = getAllPersonnel()
    return render_template('auth/index.html', personnel=personnel)

