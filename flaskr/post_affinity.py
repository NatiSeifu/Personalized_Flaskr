import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
from flaskr.auth import login_required


bp = Blueprint('affinity', __name__, url_prefix='/affinity')

@bp.route('/like', methods=("POST",))
@login_required
def like():
    post_id = request.form["post_id"]
    db = get_db()

    status = affinity_status(g.user['id'], post_id)

    if status == 1:
        flash("You have already liked this post.")
        return redirect(url_for("blog.index"))
    elif status == -1:
        affinity_update(g.user['id'], post_id, -1) 
    else:
        try:
            db.execute(
                "INSERT INTO affinity(user_id, post_id, like_status)"
                "VALUES (?, ?, ?)",
                (g.user['id'], post_id, 1)
            )
            db.commit()
        except Exception as e:
            flash("An error occurred while liking")



    return redirect(url_for("blog.index"))

@bp.route('/dislike', methods=("POST",))
@login_required
def dislike():
    post_id = request.form["post_id"]
    db = get_db()

    status = affinity_status(g.user['id'], post_id)

    if status == -1:
        flash("You have already disliked this post.")
        return redirect(url_for("blog.index"))
    elif status == 1:
        affinity_update(g.user['id'], post_id, 1) 
    else:
        try:
            db.execute(
                "INSERT INTO affinity(user_id, post_id, like_status)"
                "VALUES (?, ?, ?)",
                (g.user['id'], post_id, -1)
            )
            db.commit()
        except Exception as e:
            flash("An error occurred while disliking")


    return redirect(url_for("blog.index"))


def affinity_status(user_id, post_id):
    row = get_db().execute(
    'SELECT like_status'
    '   FROM affinity '
    '   WHERE user_id = ? AND post_id = ? ',
    (user_id, post_id)
    ).fetchone()

    return row['like_status'] if row else None


def affinity_update(user_id, post_id, cur_stat):
    db = get_db()
    db.execute(
    'UPDATE affinity SET like_status = ?'
    'WHERE user_id = ? and post_id = ?',
    (-(cur_stat), user_id, post_id)
    )
    db.commit()
