from flask import Blueprint, render_template, request, g, url_for, redirect, flash
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    posts = get_db().execute(
        'SELECT p.id,title, body,created, author_id,username '
        'FROM post p JOIN user u on u.id = p.author_id '
        'ORDER BY created DESC '
    ).fetchall()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required'
        if not body:
            error = 'Content is required'
        if error is not None:
            flash(error, category='error')
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post(author_id, title, body) VALUES (?,?,?)',
                (g.user['id'], title, body)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(author_id, check_author=True):
    post = get_db().execute(
        'SELECT p.id,title,body,created,author_id,username '
        'FROM post p JOIN user u ON p.author_id = u.id '
        'WHERE p.id =?',
        (author_id,)
    ).fetchone()
    if post is None:
        abort(404, f"Post with id {author_id} not found")
    if check_author and post['author_id'] != g.user['id']:
        abort(403)
    return post


@bp.route('/<int:id>/update', methods=('POST', 'GET'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error, category='error')
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                'WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
