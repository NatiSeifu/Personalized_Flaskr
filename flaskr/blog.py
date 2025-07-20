from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    quote = None
    
    if request.method == 'POST':
        try:
            from google import genai
            from google.genai import types
            
            client = genai.Client()
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents="Give me a random motivational quote in the tone of a German Philosopher.",
                config = types.GenerateContentConfig(
                    thinking_config = types.ThinkingConfig(thinking_budget = 0)
                )
            )
            quote = response.text
        except Exception as e:
            flash(f"An error occurred: {e}", "error")
    
    page_number = int(request.args.get('page', 1)) # 1 -> 0, 2 -> 5 3--> 10
    posts_per_page = 5

    db = get_db()

    # Count total posts
    total_posts = db.execute(
        'SELECT COUNT(*) FROM post'
    ).fetchone()[0]

    total_pages = (total_posts + posts_per_page - 1) // posts_per_page  # Ceiling division

    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
        ' LIMIT ? OFFSET ?',
        (posts_per_page, ((page_number-1) * posts_per_page))
    ).fetchall()

    has_prev = page_number > 1
    has_next = page_number < total_pages

    return render_template(
        'blog/index.html',
        posts=posts,
        quote=quote,
        page_number=page_number,
        total_pages=total_pages,
        has_prev=has_prev,
        has_next=has_next
    )

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
    
        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                'VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)    
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist")
    
    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
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
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
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