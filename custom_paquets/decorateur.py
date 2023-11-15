from functools import wraps

from flask import session, redirect, url_for, abort

from model.personnel import check_super_admin

ACTION_INDEX = "auth.choix_connexion"


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not session.get("name"):
            redirect(url_for(ACTION_INDEX))
        return func(*args, **kwargs)


def admin_login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not session.get("name") or not check_super_admin(session.get("name")):
            redirect(url_for(ACTION_INDEX))
        return func(*args, **kwargs)

    return decorated_function


def apprenti_login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not session.get("name") or session.get("name") != "apprenti":
            redirect(url_for(ACTION_INDEX))
        return func(*args, **kwargs)

    return decorated_function
