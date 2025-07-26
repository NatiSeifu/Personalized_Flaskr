# In the same file (or a new api.py Blueprint)
from flask import Blueprint, request, jsonify, abort, g
from flaskr.db import get_db


bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/posts')
def get_posts():
    page = int(request.args.get('page', 1))
    posts_per_page = 5
    db = get_db()

    total_posts = db.execute('SELECT COUNT(*) FROM post').fetchone()[0]
    total_pages = (total_posts + posts_per_page - 1) // posts_per_page

    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username '
        'FROM post p JOIN user u ON p.author_id = u.id '
        'ORDER BY created DESC '
        'LIMIT ? OFFSET ?',
        (posts_per_page, (page - 1) * posts_per_page)
    ).fetchall()

    return jsonify({
        "posts": [dict(post) for post in posts],
        "pagination": {
            "page": page,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
    })

@bp.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    title = data.get('title')
    body = data.get('body')
    author_id = data.get('author_id')  # or use `g.user['id']` if session-based

    if not title:
        return jsonify({"error": "Title is required"}), 400

    db = get_db()
    db.execute(
        'INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)',
        (title, body, author_id)
    )
    db.commit()
    return jsonify({"message": "Post created"}), 201

@bp.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    db = get_db()
    post = db.execute(
        'SELECT p.id, title, body, created, author_id, username '
        'FROM post p JOIN user u ON p.author_id = u.id '
        'WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        return jsonify({"error": "Post not found"}), 404

    return jsonify(dict(post))

@bp.route('/posts/<int:id>', methods=['PUT'])
def update_post(id):
    data = request.get_json()
    title = data.get('title')
    body = data.get('body')

    if not title:
        return jsonify({"error": "Title is required"}), 400

    db = get_db()
    post = db.execute('SELECT * FROM post WHERE id = ?', (id,)).fetchone()
    if post is None:
        return jsonify({"error": "Post not found"}), 404

    db.execute(
        'UPDATE post SET title = ?, body = ? WHERE id = ?',
        (title, body, id)
    )
    db.commit()
    return jsonify({"message": "Post updated"})

@bp.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    db = get_db()
    post = db.execute('SELECT * FROM post WHERE id = ?', (id,)).fetchone()
    if post is None:
        return jsonify({"error": "Post not found"}), 404

    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return jsonify({"message": "Post deleted"})

@bp.route('/quote', methods=['POST'])
def generate_quote():
    try:
        from google import genai
        from google.genai import types
        
        client = genai.Client()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Give me a random motivational quote in the tone of a German Philosopher.",
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=0)
            )
        )
        return jsonify({"quote": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
