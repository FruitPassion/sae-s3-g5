from functools import wraps

from flask import session, redirect, url_for, abort

from model.personnel import check_super_admin, get_role

ACTION_INDEX = "auth.choix_connexion"


def admin_login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if (session.get("name") is None) and (check_super_admin(session.get("name")) is False):
            return redirect(url_for(ACTION_INDEX))
        return func(*args, **kwargs)
    return decorated_function


def apprenti_login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        print(session.get("name"))
        if not session.get("name") or session.get("role") != "apprentis":
            return redirect(url_for(ACTION_INDEX))
        return func(*args, **kwargs)
    return decorated_function


def personnel_login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if (session.get("name") is None) and (
                get_role(session.get("name")) not in ["Educateur Administrateur", "Educateur", "CIP"]):
            return redirect(url_for(ACTION_INDEX))
        return func(*args, **kwargs)
    return decorated_function


def cip_login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if (session.get("name") is None) and (get_role(session.get("name")) != "CIP"):
            return redirect(url_for(ACTION_INDEX))
        return func(*args, **kwargs)
    return decorated_function


def educadmin_login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if (session.get("name") is None) and (get_role(session.get("name")) != "Educateur Administrateur"):
            return redirect(url_for(ACTION_INDEX))
        return func(*args, **kwargs)
    return decorated_function


def educsimple_login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if (session.get("name") is None) and (get_role(session.get("name")) != "Educateur"):
            return redirect(url_for(ACTION_INDEX))
        return func(*args, **kwargs)
    return decorated_function
