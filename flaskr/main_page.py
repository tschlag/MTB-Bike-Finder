from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

from openPinkbike import pinkbikeSearch

bp = Blueprint('main_page', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, riding_type, height, min_budget, max_budget, wheel_size, rear_sus, country, pinkbike_url, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('main/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        riding_type = request.form['riding_type']
        height = request.form['height']
        min_budget = request.form['min_budget']
        max_budget = request.form['max_budget']
        wheel_size = request.form['wheel_size']
        rear_sus = request.form['rear_sus']
        country = request.form['country']

        error = None

        if not riding_type:
            error = 'Riding type is required.'

        if not height:
            error = 'Height is required.'

        if not country:
            error = 'Country is required.'

        global pinkbike_url
        pinkbike_url = pinkbikeSearch(riding_type, height, min_budget, max_budget, wheel_size, rear_sus, country)

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (riding_type, height, min_budget, max_budget, wheel_size, rear_sus, country, pinkbike_url, author_id)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (riding_type, height, min_budget, max_budget, wheel_size, rear_sus, country, pinkbike_url, g.user['id'])
            )
            db.commit()
            return redirect(url_for('main_page.index'))

    return render_template('main/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, riding_type, height, min_budget, max_budget, wheel_size, rear_sus, country, pinkbike_url, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        riding_type = request.form['riding_type']
        height = request.form['height']
        min_budget = request.form['min_budget']
        max_budget = request.form['max_budget']
        wheel_size = request.form['wheel_size']
        rear_sus = request.form['rear_sus']
        country = request.form['country']

        error = None

        if not riding_type:
            error = 'Riding type is required.'

        if not height:
            error = 'Height is required.'

        if not country:
            error = 'Country is required.'

        pinkbike_url = pinkbikeSearch(riding_type, height, min_budget, max_budget, wheel_size, rear_sus, country)

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET riding_type = ?, height = ?, min_budget = ?, max_budget = ?, wheel_size = ?, rear_sus = ?, country = ?, pinkbike_url = ?'
                ' WHERE id = ?',
                (riding_type, height, min_budget, max_budget, wheel_size, rear_sus, country, pinkbike_url, id)
            )
            db.commit()
            return redirect(url_for('main_page.index'))

    return render_template('main/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('main_page.index'))