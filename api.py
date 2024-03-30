import flask

blueprint = flask.Blueprint(
    'api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/sign_up', methods=['POST'])
def sign_up():
    return


@blueprint.route('/api/sign_in', methods=['POST'])
def sign_in():
    return


@blueprint.route('/api/delete_user', methods=['DELETE'])
def delete_user():
    return


@blueprint.route('/api/new_graph', methods=['POST'])
def new_graph():
    return


@blueprint.route('/api/open_graph', methods=['GET'])
def open_graph():
    return


@blueprint.route('/api/update_graph', methods=['PUT'])
def update_graph():
    return


@blueprint.route('/api/all_graphs', methods=['GET'])
def all_graphs():
    return
