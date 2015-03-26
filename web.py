# ! /usr/bin/python
# coding: utf8
import dbbackend
import pagination
from flask import Flask, render_template, abort, session, redirect, request
from helper import *


app = Flask("GPortal")
app.config.from_object('config')
userMng = dbbackend.User(app.config["USER_COLLECT"])
newsMng = dbbackend.News(app.config["NEWS_COLLECT"])


@app.route("/user/<permalink>")
def user(permalink):
    user = userMng.find_by_permalink(permalink)
    if not user["data"]:
        abort(404)
    return render_template("single_user.html", user=user["data"])


def paginator(page, per_page, mng, get_func, t_data, template):
    skip = (page - 1) * int(app.config['PER_PAGE'])
    data = getattr(mng, get_func)(int(per_page), skip)

    if not data['data']:
        abort(404)

    count = mng.count()
    pag = pagination.Pagination(page, per_page, count["data"])
    added = {t_data: data["data"]}

    return render_template(template, pagination=pag, **added)


@app.route('/users', defaults={'page': 1})
@app.route('/users/page-<int:page>')
def users_list(page):
    return paginator(page, app.config["PER_PAGE"], userMng, 'get_users',
                     'users', 'users.html')


@app.route('/our_news', defaults={'page': 1})
@app.route('/our_news/page-<int:page>')
def news_list(page):
    return paginator(page, app.config["PER_PAGE"], newsMng, 'get_news',
                     'news', 'news.html')


@app.route('/single_news/<permalink>')
def single_news(permalink):
    news = newsMng.find_by_permalink(permalink)
    if not news["data"]:
        abort(404)
    return render_template("single_news.html", news=news["data"])


@app.route("/user_edit/<permalink>")
def user_edit(permalink):
    user = userMng.find_by_permalink(permalink)
    return render_template('edit_user.html', user=user['data'])


@app.route('/save_user', methods=['POST'])
def save_user():
    user_data = {
        "name": request.form.get("user-name", None),
        "l_name": request.form.get("user-lname", None),
        "nickname": request.form.get("user-nickname", None),
        "permalink": request.form.get("user-permalink", None)
    }

    if not user_data['name'] or not user_data['l_name']:
        flash('Name, Last name are required fields...', 'error')
        return redirect(url_for('user_edit', permalink=user_data['permalink']))
    else:
        user = userMng.update_by_permalink(user_data["permalink"], user_data)
        if user['error']:
            flash(user['error'], 'error')
            return redirect(url_for('user_edit', permalink=user_data['permalink']))
        else:
            flash("User information updated", 'success')
    return redirect(url_for('user_edit', permalink=user_data['permalink']))


@app.before_request
def csrf_protect():
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(400)

app.jinja_env.globals['url_for_other_page'] = url_for_other_page
app.jinja_env.globals['csrf_token'] = generate_csrf_token

if __name__ == '__main__':
    app.run(port=5000, debug=True)
