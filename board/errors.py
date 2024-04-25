from flask import render_template, current_app, request


def page_not_found(e):
    current_app.logger.info(f"'{e.name}' error ({e.code}) at {request.url}")
    return render_template('errors/404.html'), 404
