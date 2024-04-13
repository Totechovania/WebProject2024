import json

import flask
from flask import redirect, render_template, abort, request
from requests import get, post, delete

from forms.news import NewsForm
from forms.user import RegisterForm, LoginForm
from utilities.system import init_app

app = init_app()


@app.route('/logout')
def logout():
    get('http://127.0.0.1:2000/api/logout')
    return redirect("/")


@app.route('/news', methods=['POST'])
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        post('http://127.0.0.1:2000/api/add_news', json=flask.jsonify(form))
        return redirect('/')
    return render_template('news.html', title='Добавление новости',
                           form=form)


@app.route('/news/<int:news_id>', methods=['GET', 'POST'])
def edit_news(news_id):
    form = NewsForm()
    if request.method == "GET":
        news = get(f'http://127.0.0.1:2000/api/edit_news/{news_id}').json()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        if post(f'http://127.0.0.1:2000/api/edit_news/{news_id}', json=flask.jsonify(form)).status_code == 404:
            abort(404)
        return redirect('/')
    return render_template('news.html',
                           title='Редактирование новости',
                           form=form)


@app.route('/news_delete/<int:news_id>', methods=['GET', 'DELETE'])
def news_delete(news_id):
    if delete(f'http://127.0.0.1:2000/api/news_delete/{news_id}').status_code == 404:
        abort(404)
    return redirect('/')


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up_page():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        print(form.data)
        response = post(f'http://127.0.0.1:2000/api/sign_up', json=json.dumps(form.data))
        print(response)
        if response.status_code == 409:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        return redirect('/sign_in')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in_page():
    form = LoginForm()
    if form.validate_on_submit():
        response = post(f'http://127.0.0.1:2000/api/sign_in', json=json.dumps(form.data))
        if response.status_code == 401:
            return render_template('login.html',
                                   message="Неправильный логин или пароль",
                                   form=form)
        if response.status_code == 404:
            abort(404)
        return redirect("/")
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/', methods=['GET'])
def main_page():
    return redirect('/social_media')


@app.route('/profile/<int:id>', methods=['GET'])
def profile_page(id):
    return render_template('.html', title='Профиль')


@app.route('/graphs', methods=['GET'])
def graphs_page():
    return render_template('.html', title='Графики')


@app.route('/new_graph', methods=['GET', 'PUT'])
def new_graph_page():
    return render_template('project_page.html', title='Новый график')


@app.route('/settings', methods=['GET', 'POST'])
def settings_page():
    return render_template('.html', title='Настройки')


@app.route('/projects', methods=['GET'])
def projects_page():
    return render_template('.html', title='Проекты')


@app.route('/social_media', methods=['GET'])
def social_media_main_page():
    data = []
    response = json.loads(get(f'http://127.0.0.1:2000/api/all_news').json()['news'])
    for el in response:
        user = get(f'http://127.0.0.1:2000/api/open_user/{el["user_id"]}').json()
        user.update(el)
        data.append(user)
    return render_template("social_media.html", news=data)


@app.errorhandler(404)
def error_404(_):
    return 'Error'


@app.errorhandler(401)
def error_401(_):
    return redirect('/sign_in')
