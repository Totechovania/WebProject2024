import base64
from random import randint
from io import BytesIO
import flask
from data import db_session, graphs, users, news, codes
import datetime
from GraphDrawer.GraphDrawer import GraphDrawer
from utilities.draw import hex_to_rgb
from flask_login import current_user, login_required
from utilities.avatar_to_bytes import avatar_to_bytes
from utilities.generate_graph_preview import generate_graph_preview
from utilities.message_sender import send_email

blueprint = flask.Blueprint(
    'api',
    __name__,
    template_folder='templates'
)



@blueprint.route('/api/user_graphs/<int:user_id>', methods=['GET'])
def user_graphs(user_id):
    with db_session.create_session() as db_sess:
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
    with db_session.create_session() as db_sess:
        if current_user.is_authenticated and current_user.id == user_id:
            news_lst = db_sess.query(news.News).filter(news.News.user == current_user)
        else:
            news_lst = db_sess.query(news.News).filter(news.News.user_id == user_id)
        user = db_sess.query(users.User).filter(users.User.id == user_id).first()
        res = []
        for news_elem in news_lst:
            res.append({
                'news': news_elem.to_dict(
                    only=('id', 'title', 'content', 'updated_date', 'is_private', 'votes', 'graph_id', 'user_id')),
                'graph': db_sess.query(graphs.Graph).filter(graphs.Graph.id == news_elem.graph_id).first().to_dict(
                    only=('id', 'private', 'name', 'preview', 'user_id', 'update_date', 'created_date')),
                'user': user.to_dict(only=('id', 'name', 'about', 'avatar'))
            })

        return flask.jsonify(res)


@blueprint.route('/api/delete_graph/<int:graph_id>', methods=['DELETE'])
@login_required
def delete_graph(graph_id):
    with db_session.create_session() as db_sess:
        graph = db_sess.query(graphs.Graph).get(graph_id)
        if not graph:
            return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)

        if current_user.id != graph.user_id:
            return flask.make_response(flask.jsonify({'error': 'Not Enough Rights'}), 401)

        db_sess.delete(graph)
        db_sess.commit()
        return flask.jsonify({'success': 'OK'})


@blueprint.route('/api/delete_user<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    with db_session.create_session() as db_sess:
        user = db_sess.query(users.User).get(user_id)
        if not user:
            return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)
        if current_user.id != users.User.id:
            return flask.make_response(flask.jsonify({'error': 'Not Enough Rights'}), 401)
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

    with db_session.create_session() as db_sess:

        db_sess.add(graph)
        db_sess.commit()
        return flask.jsonify({'id': graph.id})


@blueprint.route('/api/open_graph/<int:graph_id>', methods=['GET'])
def open_graph(graph_id):
    with db_session.create_session() as db_sess:
        graph = db_sess.query(graphs.Graph).get(graph_id)
        if not graph:
            return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)
        if graph.private and (not current_user.is_authenticated or current_user.id != graph.user_id):
            return flask.make_response('Not found', 404)

        return flask.jsonify(
            {
                'graph': graph.to_dict(only=('name', 'function', 'created_date', 'preview', 'private', 'user_id', 'id'))
            }
        )


@blueprint.route('/api/update_graph/<int:graph_id>', methods=['PUT'])
@login_required
def update_graph(graph_id):
    with db_session.create_session() as db_sess:
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
    with db_session.create_session() as db_sess:
        graph = db_sess.query(graphs.Graph).filter(graphs.Graph.is_private != True).all()
        return flask.jsonify(
            {
                'graphs':
                    [item.to_dict(only=('name', 'function', 'created_date'))
                     for item in graph]
            }
        )


@blueprint.route('/api/draw', methods=['POST'])
def draw():
    json = flask.request.get_json()
    colors = json['colors']
    for i in range(len(colors)):
        colors[i] = hex_to_rgb(colors[i][1:])
    try:
        drawer = GraphDrawer(int(json['width']),
                         int(json['height']),
                         1 / float(json['pixel_per_unit']),
                         float(json['center_x']),
                         float(json['center_y']))
    except ValueError as e:
        return flask.make_response(flask.jsonify({'error': 'Bad request ' + str(e)}), 400)
    except TypeError as e:
        return flask.make_response(flask.jsonify({'error': 'Bad request ' + str(e)}), 400)
    except ZeroDivisionError as e:
        return flask.make_response(flask.jsonify({'error': 'Bad request ' + str(e)}), 400)

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
    with db_session.create_session() as db_sess:
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
    with db_session.create_session() as db_sess:
        if not current_user.is_authenticated:
            return flask.make_response(flask.jsonify({'error': 'Not Authenticated'}), 401)
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


@blueprint.route('/api/all_news', methods=['GET'])
def all_news():
    with db_session.create_session() as db_sess:
        news_lst = db_sess.query(news.News)
        res = []
        for news_elem in news_lst:
            res.append({
                'news': news_elem.to_dict(
                    only=('id', 'title', 'content', 'updated_date', 'updated_date', 'graph_id', 'user_id')),
                'graph': db_sess.query(graphs.Graph).filter(graphs.Graph.id == news_elem.graph_id).first().to_dict(
                    only=('id', 'name', 'preview', 'private')),
                'user': db_sess.query(users.User).filter(users.User.id == news_elem.user_id).first().to_dict(
                    only=('id', 'name', 'avatar', 'about')),
            })

        return flask.jsonify(res)


@blueprint.route('/api/update_news/<int:news_id>', methods=['POST'])
@login_required
def update_news(news_id):
    with db_session.create_session() as db_sess:
        new = db_sess.query(news.News).filter(news.News.id == news_id, news.News.user == current_user).first()
        if not current_user.is_authenticated:
            return flask.make_response(flask.jsonify({'error': 'Not Authenticated'}), 401)
        if not new:
            return flask.make_response(flask.jsonify({'error': 'Not Found or Not Enough Rights'}), 404)
        if not all(key in flask.request.json.keys() for key in ['title', 'content', 'graph_id']):
            return flask.make_response(flask.jsonify({'error': 'Bad request'}), 400)

        new.title = flask.request.json['title']
        new.content = flask.request.json['content']
        new.graph_id = int(flask.request.json['graph_id'])
        new.updated_date = datetime.datetime.now()
        db_sess.commit()
        return flask.jsonify({'success': 'OK'})


@blueprint.route('/api/delete_news/<int:news_id>', methods=['DELETE'])
def delete_news(news_id):
    with db_session.create_session() as db_sess:
        new = db_sess.query(news.News).filter(news.News.id == news_id,
                                              news.News.user == current_user).first()
        if not current_user.is_authenticated:
            return flask.make_response(flask.jsonify({'error': 'Not Authenticated'}), 401)
        if not new:
            return flask.make_response(flask.jsonify({'error': 'Not Found or Not Enough Rights'}), 404)
        db_sess.delete(new)
        db_sess.commit()
        return flask.jsonify({'success': 'OK'})


@blueprint.route('/api/new_news', methods=['POST'])
def new_news():
    with db_session.create_session() as db_sess:
        if not current_user.is_authenticated:
            return flask.make_response(flask.jsonify({'error': 'Not Authenticated'}), 401)
        if not all(key in flask.request.json.keys() for key in ['title', 'content', 'graph_id']):
            return flask.make_response(flask.jsonify({'error': 'Bad request'}), 400)
        new = news.News()
        new.title = flask.request.json['title']
        new.content = flask.request.json['content']
        new.graph_id = flask.request.json['graph_id']
        new.user_id = current_user.id
        db_sess.add(new)
        db_sess.commit()

        return flask.jsonify({'success': 'OK'})


@blueprint.route('/api/open_news/<int:news_id>', methods=['GET'])
def open_news(news_id):
    with db_session.create_session() as db_sess:
        new = db_sess.query(news.News).filter(news.News.id == news_id).first()

        if not new:
            return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)

        graph = db_sess.query(graphs.Graph).filter(graphs.Graph.id == new.graph_id).first()
        user = db_sess.query(users.User).filter(users.User.id == new.id).first()

        if new.is_private and new.user_id != current_user.id:
            if new.user_id == current_user.id:
                return flask.make_response(flask.jsonify({'error': 'Not Enough Rights'}), 401)

        return flask.jsonify({'news': new.to_dict(
            only=('id', 'title', 'content', 'updated_date', 'is_private', 'votes', 'graph_id', 'user_id')),
            'graph': graph.to_dict(
                only=('id', 'private', 'name', 'preview', 'user_id', 'update_date', 'created_date')),
            'user': user.to_dict(only=('id', 'name', 'about', 'avatar'))})


@blueprint.route('/api/generate_code/<email>', methods=['POST'])
def generate_code(email):
    with db_session.create_session() as db_sess:
        validation_object = db_sess.query(codes.Codes).filter(codes.Codes.email == email).first()
        if validation_object:
            db_sess.delete(validation_object)
            db_sess.commit()
        code = randint(100000, 999999)
        send_email(code, email)

        validation_object = codes.Codes()
        validation_object.email = email
        validation_object.code = code

        db_sess.add(validation_object)
        db_sess.commit()
        return flask.make_response(flask.jsonify({'success': 'OK'}), 200)
