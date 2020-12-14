from flask import Blueprint, render_template, url_for, redirect

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(500)
def internal_error(error):
    return redirect(url_for('question_page'))


@errors.app_errorhandler(404)
def err_404(error):
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(401)
def err_401(error):
    return render_template('errors/401.html'), 401

