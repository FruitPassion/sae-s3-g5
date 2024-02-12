from functools import wraps

from flask import session, redirect, url_for

from model.personnel import Personnel

ACTION_INDEX = "auth.choix_connexion"
EDUCATEUR_ADMIN = "Educateur Administrateur"

def logout_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session.get("name"):
            return redirect(url_for('auth.logout'))
        return func(*args, **kwargs)
    return decorated_function


def admin_login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if (session.get("name") is None) and (Personnel.check_super_admin(session.get("name")) is False):
            return redirect(url_for(ACTION_INDEX))
        return func(*args, **kwargs)
    return decorated_function


def apprenti_login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not session.get("name") or session.get("role") != "apprentis":
            return redirect(url_for(ACTION_INDEX))
        return func(*args, **kwargs)
    return decorated_function


def personnel_login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if (session.get("name") is None) and (
                Personnel.get_role_by_login(session.get("name")) not in [EDUCATEUR_ADMIN, "Educateur", "CIP"]):
            return redirect(url_for(ACTION_INDEX))
        return func(*args, **kwargs)
    return decorated_function


def cip_login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if (session.get("name") is None) or (Personnel.get_role_by_login(session.get("name")) != "CIP"):
            return redirect(url_for(ACTION_INDEX))
        return func(*args, **kwargs)
    return decorated_function


def educadmin_login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if (session.get("name") is None) or (Personnel.get_role_by_login(session.get("name")) != EDUCATEUR_ADMIN):
            return redirect(url_for(ACTION_INDEX))
        return func(*args, **kwargs)
    return decorated_function


def educsimple_login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if (session.get("name") is None) or (Personnel.get_role_by_login(session.get("name")) not in ["Educateur",EDUCATEUR_ADMIN]):
            return redirect(url_for(ACTION_INDEX))
        return func(*args, **kwargs)
    return decorated_function
