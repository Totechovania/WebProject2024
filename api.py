import base64
import datetime
import json
from io import BytesIO

import flask
from flask_login import login_user, login_required, logout_user, current_user

from GraphDrawer.GraphDrawer import GraphDrawer
from data import db_session, graphs, users, news
from utilities.draw import hex_to_rgb
from utilities.system import get_manager

blueprint = flask.Blueprint(
    'api',
    __name__,
    template_folder='templates'
)

db_sess = db_session.create_session()
login_manager = get_manager()


@login_manager.user_loader
def load_user(user_id):
    return db_sess.query(users.User).get(user_id)


@blueprint.route('/api/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return flask.make_response(flask.jsonify({'status': 'OK'}), 200)


@blueprint.route('/api/sign_up', methods=['POST'])
def sign_up():
    data = json.loads(flask.request.json)
    if not data:
        return flask.make_response(flask.jsonify({'reason': 'Empty request'}), 400)
    elif not all(key in data for key in
                 ['name', 'email', 'password']):
        return flask.make_response(flask.jsonify({'reason': 'Bad request'}), 400)
    user = db_sess.query(users.User).filter(users.User.email == data['email']).first()
    if user:
        return flask.make_response(flask.jsonify({'reason': 'User already exists'}), 409)
    new_user = users.User(
        name=data['name'],
        email=data['email'],
        hashed_password=data['password'],
        created_date=datetime.datetime.now()
    )
    new_user.set_password(data['password'])
    db_sess.add(new_user)
    db_sess.commit()
    return flask.make_response(flask.jsonify({'status': 'OK'}), 200)


@blueprint.route('/api/sign_in', methods=['POST'])
def sign_in():
    data = json.loads(flask.request.json)
    if not data:
        return flask.make_response(flask.jsonify({'reason': 'Empty request'}), 400)
    elif not all(key in data for key in
                 ['email', 'password']):
        return flask.make_response(flask.jsonify({'reason': 'Bad request'}), 400)
    user = db_sess.query(users.User).filter(users.User.email == data['email']).first()
    if not user:
        return flask.make_response(flask.jsonify({'reason': 'Not found'}), 404)
    if user and user.check_password(data['password']):
        login_user(user, remember=data['remember_me'])
        return flask.make_response(flask.jsonify({'status': 'OK'}), 200)
    return flask.make_response(flask.jsonify({'reason': 'Incorrect data'}), 401)


@blueprint.route('/api/delete_graph<int:graph_id>', methods=['DELETE'])
@login_required
def delete_graph(graph_id):
    graph = db_sess.query(users.User).get(graph_id)
    if not graph:
        return flask.make_response(flask.jsonify({'reason': 'Not found'}), 404)
    db_sess.delete(graph)
    db_sess.commit()
    return flask.make_response(flask.jsonify({'status': 'OK'}), 200)


@blueprint.route('/api/delete_user<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    user = db_sess.query(users.User).get(user_id)
    if not user:
        return flask.make_response(flask.jsonify({'reason': 'Not found'}), 404)
    db_sess.delete(user)
    db_sess.commit()
    return flask.make_response(flask.jsonify({'status': 'OK'}), 200)


@blueprint.route('/api/new_graph', methods=['POST'])
@login_required
def new_graph():
    if not flask.request.json:
        return flask.make_response(flask.jsonify({'reason': 'Empty request'}), 400)
    elif not all(key in flask.request.json for key in
                 ['name', 'function', 'created_date', 'private']):
        return flask.make_response(flask.jsonify({'reason': 'Bad request'}), 400)
    graph = graphs.Graph(
        name=flask.request.json['name'],
        function=flask.request.json['function'],
        created_date=flask.request.json['created_date'],
        private=flask.request.json['private']
    )
    db_sess.add(graph)
    db_sess.commit()
    return flask.make_response(flask.jsonify({'status': 'OK'}), 200)


@blueprint.route('/api/open_graph/<int:graph_id>', methods=['GET'])
@login_required
def open_graph(graph_id):
    graph = db_sess.query(graphs.Graph).get(graph_id)
    if not graph:
        return flask.make_response(flask.jsonify({'reason': 'Not found'}), 404)
    return flask.jsonify(
        {
            'graph': graph.to_dict(only=(
                'name', 'function', 'created_date', 'private'))
        }
    )


@blueprint.route('/api/update_graph<int:graph_id>', methods=['PUT'])
@login_required
def update_graph(graph_id):
    graph = db_sess.query(graphs.Graph).get(graph_id)
    req = flask.request.json
    if not graph:
        return flask.make_response(flask.jsonify({'reason': 'Not found'}), 404)
    db_sess.query(graphs.Graph).update(graph_id, req)
    db_sess.commit()
    return flask.make_response(flask.jsonify({'status': 'OK'}), 200)


@blueprint.route('/api/all_graphs', methods=['GET'])
@login_required
def all_graphs():
    graph = db_sess.query(graphs.Graph).all()
    return flask.jsonify(
        {
            'graphs':
                [item.to_dict(only=('name', 'function', 'created_date'))
                 for item in graph]
        }
    )


@blueprint.route('/api/add_news', methods=['POST'])
@login_required
def add_news():
    new = news.News()
    new.title = flask.request.json['title']
    new.content = flask.request.json['content']
    new.is_private = flask.request.json['is_private']
    current_user.news.append(new)
    db_sess.merge(current_user)
    db_sess.commit()
    return flask.make_response(flask.jsonify({'status': 'OK'}), 200)


@blueprint.route('/api/edit_news/<int:news_id>', methods=['GET', 'POST'])
@login_required
def edit_news(news_id):
    if flask.request.method == "GET":
        return db_sess.query(news.News).filter(news.News.id == news_id, news.News.user == current_user).first()
    new = db_sess.query(news.News).filter(news.News.id == news_id,
                                          news.News.user == current_user).first()
    if not new:
        return flask.make_response(flask.jsonify({'reason': 'Not found'}), 404)
    new.title = flask.request.json['title']
    new.content = flask.request.json['content']
    new.is_private = flask.request.json['is_private']
    db_sess.commit()
    return flask.make_response(flask.jsonify({'status': 'OK'}), 200)


@blueprint.route('/api/news_delete/<int:news_id>', methods=['DELETE'])
@login_required
def news_delete(news_id):
    new = db_sess.query(news.News).filter(news.News.id == news_id,
                                          news.News.user == current_user).first()
    if not new:
        return flask.make_response(flask.jsonify({'reason': 'Not found'}), 404)
    db_sess.delete(new)
    db_sess.commit()
    return flask.make_response(flask.jsonify({'status': 'OK'}), 200)


@blueprint.route('/api/all_news', methods=['GET'])
def all_news():
    if current_user.is_authenticated:
        new = json.dumps(list(map(lambda x: x.to_dict(
            only=('id', 'title', 'content', 'created_date', 'is_private', 'user_id')), db_sess.query(news.News).filter(
            (news.News.user == current_user) | (news.News.is_private != True)))))
    else:
        new = json.dumps(list(map(lambda x: x.to_dict(
            only=('id', 'title', 'content', 'created_date', 'is_private', 'user_id')),
                                  db_sess.query(news.News).filter(news.News.is_private != True))))
    return flask.make_response(flask.jsonify({'status': 'OK', 'news': new}), 200)


'''
@blueprint.route('/api/all_users', methods=['GET'])
def all_users():
    user = db_sess.query(users.User).all()
    return flask.jsonify(
        {
            'users':
                [item.to_dict(only=('name', 'email', 'hashed_password', 'created_date'))
                 for item in user]
        }
    )
'''


@blueprint.route('/api/open_user/<int:user_id>', methods=['GET'])
def open_user(user_id):
    user = db_sess.query(users.User).get(user_id)
    if not user:
        return flask.make_response(flask.jsonify({'reason': 'Not found'}), 404)
    return flask.jsonify(
        {
            'user': user.to_dict(only=(
                'name', 'created_date'))
        }
    )


@blueprint.route('/api/draw', methods=['POST'])
@login_required
def draw():
    json = flask.request.get_json()
    print(json)
    colors = json['colors']
    for i in range(len(colors)):
        colors[i] = hex_to_rgb(colors[i][1:])

    drawer = GraphDrawer(int(json['width']),
                         int(json['height']),
                         1 / float(json['pixel_per_unit']),
                         float(json['center_x']),
                         float(json['center_y']))
    img = drawer.draw(json['formulas'], colors)

    image_file = BytesIO()
    img.save(image_file, format='PNG')
    imagedata = image_file.getvalue()

    return base64.b64encode(imagedata)
