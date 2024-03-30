from utilities.system import init_all
from flask import redirect

app = init_all(__name__)


@app.route('/sign_up', methods=['GET'])
def sign_up_page():
    return redirect('/')


@app.route('/sign_in', methods=['GET'])
def sign_in_page():
    return redirect('/')


@app.route('/', methods=['GET'])
def main_page():
    return redirect('/sign_in')


@app.route('/profile/<int:id>', methods=['GET'])
def profile_page(id):
    return


@app.route('/graphs', methods=['GET'])
def graphs_page():
    return


@app.route('/new_graph', methods=['GET', 'PUT'])
def new_graph_page():
    return


@app.route('/settings', methods=['GET', 'POST'])
def settings_page():
    return


@app.route('/projects', methods=['GET'])
def projects_page():
    return


@app.errorhandler(404)
def error_404(_):
    return


@app.errorhandler(401)
def error_401(_):
    return redirect('/sign_in')


app.run(port=2000, host='127.0.0.1')
