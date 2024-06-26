from utilities.system import init_all
from flask import redirect, render_template, make_response
from flask_login import login_user, login_required, logout_user, current_user
from forms.user import RegisterForm, LoginForm
from data.users import User
from data.codes import Codes
from data import db_session, graphs, codes

app, login_manager = init_all()

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    with db_session.create_session() as db_sess:
        return db_sess.query(User).get(user_id)


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up_page():
    with db_session.create_session() as db_sess:
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

            if not form.code.data:
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Заполните поле код подтверждения")

            code = db_sess.query(Codes).filter(codes.Codes.email == form.email.data).first()

            if not code:
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Код подтверждения не существует")

            if int(form.code.data) != code.code:
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Неправильный код подтверждения")

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
    with db_session.create_session() as db_sess:
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
    with db_session.create_session() as db_sess:
        user = db_sess.query(User).get(id)
        if not user:
            return make_response('Not found', 404)
        return render_template('profile.html', title='Профиль', usr_id=id)


@app.route('/profile', methods=['GET'])
def self_profile():
    if not current_user.is_authenticated:
        return redirect('/sign_in')
    return redirect('/profile/' + str(current_user.id))


@app.route('/new_graph', methods=['GET', 'PUT'])
def new_graph_page():
    return render_template('new_graph.html', title='Новый график')


@app.route('/graph/<int:id>', methods=['GET'])
def graph_page(id):
    with db_session.create_session() as db_sess:
        graph = db_sess.query(graphs.Graph).get(id)
        if not graph:
            return make_response('Not found', 404)
        if graph.private and (not current_user.is_authenticated or current_user.id != graph.user_id):
            return make_response('Not Enough Rights', 401)
        return render_template('graph.html', title='График', graph=graph)


@app.route('/', methods=['GET'])
@app.route('/social_media', methods=['GET'])
def social_media_main_page():
    return render_template("social_media.html", title='Публикации')


@app.errorhandler(404)
def error_404(_):
    return 'Error 404 (Not Found or Not Enough Rights)'


@app.errorhandler(401)
def error_401(_):
    return redirect('/sign_in')
