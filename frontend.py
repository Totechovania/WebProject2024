from utilities.system import init_all, load_user_db
from flask import redirect, render_template, abort, request, make_response
from flask_login import login_user, login_required, logout_user, current_user
from forms.user import RegisterForm, LoginForm
from forms.news import NewsForm
from data.news import News
from data.users import User
from data import db_session, graphs
from utilities.message_sender import send_email, generate_code

app, login_manager = init_all()
db_sess = db_session.create_session()


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    return load_user_db(user_id)



@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up_page():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        code = generate_code()
        print(send_email(code, form.email.data))
        print(code, form.email.data)

        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/sign_in')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/profile/<id>', methods=['GET'])
def profile(id):
    user = db_sess.query(User).get(id)
    if not user:
        return make_response('Not found', 404)
    return render_template('profile.html', title='Профиль', usr_id=id)


@app.route('/profile', methods=['GET'])
def self_profile():
    if not current_user.is_authenticated:
        return redirect('/sign_in')
    return redirect('/profile/' + str(current_user.id))


@app.route('/graphs', methods=['GET'])
def graphs_page():
    return render_template('.html', title='Графики')


@app.route('/new_graph', methods=['GET', 'PUT'])
def new_graph_page():
    return render_template('new_graph.html', title='Новый график')


@app.route('/graph/<int:id>', methods=['GET'])
def graph_page(id):
    graph = db_sess.query(graphs.Graph).get(id)
    if not graph:
        return make_response('Not found', 404)
    if graph.private and (not current_user.is_authenticated or current_user.id != graph.user_id):
        return make_response('Not found', 404)
    return render_template('graph.html', title='График', graph=graph)


@app.route('/settings', methods=['GET', 'POST'])
def settings_page():
    return render_template('.html', title='Настройки')


@app.route('/projects', methods=['GET'])
def projects_page():
    return render_template('.html', title='Проекты')


@app.route('/', methods=['GET'])
@app.route('/social_media', methods=['GET'])
def social_media_main_page():
    return render_template("social_media.html", title='Публикации')


@app.errorhandler(404)
def error_404(_):
    return 'Error'


@app.errorhandler(401)
def error_401(_):
    return redirect('/sign_in')
