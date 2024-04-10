import flask
from data import db_session, graphs, users
import datetime

blueprint = flask.Blueprint(
    'api',
    __name__,
    template_folder='templates'
)

db_sess = db_session.create_session()


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


@blueprint.route('/api/delete_graph<int:graph_id>', methods=['DELETE'])
def delete_graph(graph_id):
    graph = db_sess.query(users.User).get(graph_id)
    if not graph:
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
def new_graph():
    if not flask.request.json:
        return flask.make_response(flask.jsonify({'error': 'Empty request'}), 400)
    elif not all(key in flask.request.json for key in
                 ['name', 'function', 'created_date', 'private']):
        return flask.make_response(flask.jsonify({'error': 'Bad request'}), 400)
    graph = graphs.Graph(
        name=flask.request.json['name'],
        function=flask.request.json['function'],
        created_date=flask.request.json['created_date'],
        private=flask.request.json['private']
    )
    db_sess.add(graph)
    db_sess.commit()
    return flask.jsonify({'id': graph.id})


@blueprint.route('/api/open_graph/<int:graph_id>', methods=['GET'])
def open_graph(graph_id):
    graph = db_sess.query(graphs.Graph).get(graph_id)
    if not graph:
        return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)
    return flask.jsonify(
        {
            'graph': graph.to_dict(only=(
                'name', 'function', 'created_date', 'private'))
        }
    )


@blueprint.route('/api/update_graph<int:graph_id>', methods=['PUT'])
def update_graph(graph_id):
    graph = db_sess.query(graphs.Graph).get(graph_id)
    req = flask.request.json
    if not graph:
        return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)
    db_sess.query(graphs.Graph).update(graph_id, req)
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


@blueprint.route('/api/all_users', methods=['GET'])
def all_users():
    user = db_sess.query(users.User).all()
    return flask.jsonify(
        {
            'users':
                [item.to_dict(only=('name', 'email', 'password', 'created_date'))
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
                'name', 'email', 'password', 'created_date'))
        }
    )

@blueprint.route('/api/draw', methods=['POST'])
def draw():
    json = flask.request.get_json()

    drawer = GraphDrawer(img_w=json['img_w'], img_h=json['img_h'], units_per_pixel=json['units_per_pixel'], c_x=json['c_x'], c_y=json['c_y'])