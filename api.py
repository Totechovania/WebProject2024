import base64
from io import BytesIO
import flask
from data import db_session, graphs, users, news
import datetime
from GraphDrawer.GraphDrawer import GraphDrawer
from utilities.draw import hex_to_rgb
from flask_login import current_user, login_required
from utilities.avatar_to_bytes import avatar_to_bytes
from utilities.generate_graph_preview import generate_graph_preview

blueprint = flask.Blueprint(
    'api',
    __name__,
    template_folder='templates'
)

db_sess = db_session.create_session()


@blueprint.route('/api/user_graphs/<int:user_id>', methods=['GET'])
def user_graphs(user_id):
    if current_user.is_authenticated:
        if current_user.id == user_id:
            graph = db_sess.query(graphs.Graph).filter(graphs.Graph.user == current_user)
            return flask.jsonify(
                {
                    'graphs':
                        [item.to_dict(only=(
                            'id', 'private', 'name', 'function', 'preview', 'user_id', 'update_date',
                            'created_date'))
                            for item in graph]
                }
            )
    graph = db_sess.query(graphs.Graph).filter(graphs.Graph.private != True, graphs.Graph.user_id == user_id)
    return flask.jsonify(
        {
            'graphs':
                [item.to_dict(only=(
                    'id', 'private', 'name', 'function', 'preview', 'user_id', 'update_date',
                    'created_date'))
                    for item in graph]
        }
    )


@blueprint.route('/api/user_news/<int:user_id>', methods=['GET'])
def user_news(user_id):
    if current_user.is_authenticated:
        if current_user.id == user_id:
            new = db_sess.query(news.News).filter(news.News.user == current_user)
            return flask.jsonify(
                {
                    'news':
                        [item.to_dict(only=(
                            'id', 'title', 'content', 'created_date', 'is_private', 'user_id'))
                            for item in new]
                }
            )
    new = db_sess.query(news.News).filter(news.News.is_private != True)
    return flask.jsonify(
        {
            'news':
                [item.to_dict(only=(
                    'id', 'title', 'content', 'created_date', 'is_private', 'user_id'))
                    for item in new]
        }
    )


@blueprint.route('/api/sign_up', methods=['POST'])
def sign_up():
    if not flask.request.json:
        return flask.make_response(flask.jsonify({'error': 'Empty request'}), 400)
    elif not all(key in flask.request.json for key in
                 ['name', 'email', 'password']):
        return flask.make_response(flask.jsonify({'error': 'Bad request'}), 400)
    new_user = users.User(
        name=flask.request.json['name'],
        email=flask.request.json['email'],
        password=flask.request.json['password'],
        created_date=datetime.datetime.now()
    )
    db_sess.add(new_user)
    db_sess.commit()
    return flask.jsonify({'id': new_user.id})


@blueprint.route('/api/sign_in', methods=['POST'])
def sign_in():
    if not flask.request.json:
        return flask.make_response(flask.jsonify({'error': 'Empty request'}), 400)
    elif not all(key in flask.request.json for key in
                 ['email', 'password']):
        return flask.make_response(flask.jsonify({'error': 'Bad request'}), 400)
    users_db = db_sess.query(users.User).all()
    if not users_db:
        return flask.make_response(flask.jsonify({'error': 'Empty data_base'}), 404)
    for user in users_db:
        if flask.request.json['email'] == user['email'] and user['password'] == flask.request.json['password']:
            ...
            return flask.jsonify({'success': 'OK'})
        return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)


@blueprint.route('/api/delete_graph/<int:graph_id>', methods=['DELETE'])
@login_required
def delete_graph(graph_id):
    print(graph_id)
    db_sess = db_session.create_session()
    graph = db_sess.query(graphs.Graph).get(graph_id)
    if not graph:
        return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)

    if current_user.id != graph.user_id:
        return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)

    db_sess.delete(graph)
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})


@blueprint.route('/api/delete_user<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = db_sess.query(users.User).get(user_id)
    if not user:
        return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)
    db_sess.delete(user)
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})


@blueprint.route('/api/new_graph', methods=['POST'])
@login_required
def new_graph():
    if not flask.request.json:
        return flask.make_response(flask.jsonify({'error': 'Empty request'}), 400)

    req = flask.request.json

    if not all(key in req.keys() for key in ['name', 'private', 'graphs_params']):
        return flask.make_response(flask.jsonify({'error': 'Bad request'}), 400)

    name = req['name']
    private = req['private']
    graphs_params = req['graphs_params']

    try:
        img = generate_graph_preview(graphs_params)
    except SyntaxError:
        return flask.make_response(flask.jsonify({'error': 'Bad request'}), 400)

    graph = graphs.Graph(
        user_id=current_user.id,
        name=name,
        function=str(graphs_params),
        created_date=datetime.datetime.now(),
        private=bool(private),
        preview=img,

    )

    db_sess = db_session.create_session()
    db_sess.add(graph)
    db_sess.commit()
    return flask.jsonify({'id': graph.id})


@blueprint.route('/api/open_graph/<int:graph_id>', methods=['GET'])
def open_graph(graph_id):
    graph = db_sess.query(graphs.Graph).get(graph_id)
    if not graph:
        return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)
    if not graph:
        return flask.make_response('Not found', 404)
    if graph.private and (not current_user.is_authenticated or current_user.id != graph.user_id):
        return flask.make_response('Not found', 404)

    return flask.jsonify(
        {
            'graph': graph.to_dict(only=('name', 'function', 'created_date', 'preview',  'private', 'user_id', 'id'))
        }
    )


@blueprint.route('/api/update_graph/<int:graph_id>', methods=['PUT'])
@login_required
def update_graph(graph_id):
    graph = db_sess.query(graphs.Graph).get(graph_id)
    if not graph:
        return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)

    if current_user.id != graph.user_id:
        return flask.make_response('Not found', 404)

    if not flask.request.json:
        return flask.make_response(flask.jsonify({'error': 'Empty request'}), 400)

    req = flask.request.json

    if not all(key in req.keys() for key in ['name', 'private', 'graphs_params']):
        return flask.make_response(flask.jsonify({'error': 'Bad request'}), 400)

    name = req['name']
    private = req['private']
    graphs_params = req['graphs_params']

    try:
        img = generate_graph_preview(graphs_params)
    except SyntaxError:
        return flask.make_response(flask.jsonify({'error': 'Bad request'}), 400)

    graph.name = name
    graph.function = str(graphs_params)
    graph.private = bool(private)
    graph.preview = img
    graph.update_date = datetime.datetime.now()

    db_sess.commit()
    return flask.jsonify({'success': 'OK'})


@blueprint.route('/api/all_graphs', methods=['GET'])
def all_graphs():
    graph = db_sess.query(graphs.Graph).all()
    return flask.jsonify(
        {
            'graphs':
                [item.to_dict(only=('name', 'function', 'created_date'))
                 for item in graph]
        }
    )


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


@blueprint.route('/api/open_user/<int:user_id>', methods=['GET'])
def open_user(user_id):
    user = db_sess.query(users.User).get(user_id)
    if not user:
        return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)
    return flask.jsonify(
        {
            'user': user.to_dict(only=(
                'name', 'email', 'hashed_password', 'created_date'))
        }
    )
'''


@blueprint.route('/api/draw', methods=['POST'])
def draw():
    json = flask.request.get_json()
    colors = json['colors']
    for i in range(len(colors)):
        colors[i] = hex_to_rgb(colors[i][1:])

    drawer = GraphDrawer(int(json['width']),
                         int(json['height']),
                         1 / float(json['pixel_per_unit']),
                         float(json['center_x']),
                         float(json['center_y']))
    try:
        img = drawer.draw(json['formulas'], colors)

        image_file = BytesIO()
        img.save(image_file, format='PNG')
        imagedata = image_file.getvalue()
        return flask.make_response(base64.b64encode(imagedata), 200)
    except SyntaxError:
        return flask.make_response(flask.jsonify({'error': 'Bad request'}), 400)


@blueprint.route('/api/user_info/<int:id>', methods=['GET'])
def user_info(id):
    user = db_sess.query(users.User).get(id)
    if user:
        if current_user.is_authenticated and current_user.id == user.id:
            return flask.jsonify(current_user.to_dict(only=(
                'id', 'name', 'email', 'created_date', 'avatar', 'about')))
        else:
            return flask.jsonify(user.to_dict(only=(
                'id', 'name', 'created_date', 'avatar', 'about')))
    else:
        return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)


@blueprint.route('/api/update_user', methods=['POST'])
def update_user():
    if not current_user.is_authenticated:
        return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)
    req = flask.request.json
    if req['id'] != current_user.id:
        return flask.make_response(flask.jsonify({'error': 'Bad request'}), 400)

    user = db_sess.query(users.User).get(current_user.id)
    if "avatar" in req.keys():
        avatar_file = req['avatar']
        avatar = avatar_to_bytes(avatar_file)
        user.avatar = avatar
    if "about" in req.keys():
        about = req['about']
        user.about = about
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})
