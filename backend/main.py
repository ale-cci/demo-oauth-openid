import flask
import auth

app = flask.Flask(__name__)
app.config.update(
    SECRET_KEY='test'
)

@app.route('/')
def index():
    if 'user_id' not in flask.session:
        return flask.redirect(flask.url_for('login'))

    return flask.render_template('index.html.j2')


@app.route('/login')
def login():
    return flask.render_template('login.html.j2')

@app.route('/logout')
def logout():
    del flask.session.user_id
    return flask.redirect(flask.url_for('login'))


@app.route('/login/auth', methods=['POST'])
def perform_login():
    if 'user_id' in flask.session:
        return flask.redirect(flask.url_for('index'))

    email = flask.request.form['email']
    passwd = flask.request.form['password']

    if user_id := auth.check_password(email, passwd):
        flask.session['user_id'] = user_id
        return flask.redirect(flask.url_for('index'))

    return flask.redirect(flask.url_for('login'))
