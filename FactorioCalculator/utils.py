import functools
import hashlib
import jinja2

from flask import session, redirect, flash, jsonify


def login_required(func):
    """Make sure user is logged in before proceeding"""
    @functools.wraps(func)
    def wrapper_login_required(*args, **kwargs):
        if "uuid" not in session:
            flash(["You must be logged in to access this resource!", "danger"])
            return redirect("/")
        return func(*args, **kwargs)
    return wrapper_login_required


def api_login(func):
    """Make sure user is logged in before proceeding"""
    @functools.wraps(func)
    def wrapper_login_required(*args, **kwargs):
        if "uuid" not in session:
            return jsonify(
                {'code': 401, 'error': 'Unauthorized', 'message': 'You must be authenticated to access this resource!'}
            ), 401
        return func(*args, **kwargs)
    return wrapper_login_required


def encrypt(text:str):
    return hashlib.sha224(text.encode('utf-8')).hexdigest()


def render_without_request(template_name, **template_vars):
    env = jinja2.Environment(
        loader=jinja2.PackageLoader(__name__,'templates')
    )
    template = env.get_template(template_name)
    return template.render(noAlerts=True, **template_vars)