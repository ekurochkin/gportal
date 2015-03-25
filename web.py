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


@app.route('/users', defaults={'page': 1})
@app.route('/users/page-<int:page>')
def users_list(page):
    skip = (page - 1) * int(app.config['PER_PAGE'])
    users = userMng.get_users(int(app.config['PER_PAGE']), skip)

    if not users['data']:
        abort(404)

    count = userMng.count()
    pag = pagination.Pagination(page, app.config['PER_PAGE'], count["data"])
    return render_template('users.html', users=users['data'], pagination=pag)


@app.route('/our_news', defaults={'page': 1})
@app.route('/our_news/page-<int:page>')
def news_list(page):
    skip = (page - 1) * int(app.config['PER_PAGE'])
    news = newsMng.get_news(int(app.config['PER_PAGE']), skip)

    if not news['data']:
        abort(404)

    count = newsMng.count()
    pag = pagination.Pagination(page, app.config['PER_PAGE'], count["data"])
    return render_template('news.html', news=news['data'], pagination=pag)


@app.route('/single_news/<permalink>')
def single_news(permalink):
    news = newsMng.find_by_permalink(permalink)
    if not news["data"]:
        abort(404)
    return render_template("single_news.html", news=news["data"])



app.jinja_env.globals['url_for_other_page'] = url_for_other_page

if __name__ == '__main__':
    app.run(port=5000, debug=True)
