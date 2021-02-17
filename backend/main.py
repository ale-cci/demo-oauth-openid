import flask
import auth
from lib import flask_db
import mysql.connector.errors

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
    del flask.session['user_id']
    return flask.redirect(flask.url_for('login'))


@app.route('/login/auth', methods=['POST'])
def perform_login():
    if 'user_id' in flask.session:
        return flask.redirect(flask.url_for('index'))

    email = flask.request.form['email']
    passwd = flask.request.form['password']

    try:
        if user_id := auth.check_password(email, passwd):
            flask.session['user_id'] = user_id
            return flask.redirect(flask.url_for('index'))

    except auth.AuthException as e:
        flask.flash(('danger', str(e)))

    return flask.redirect(flask.url_for('login'))


@app.route('/users')
def users():
    email_like = flask.request.args.get('email', '')
    email_like = f'%{email_like}%'

    users = flask_db.fetch_all('''
    select id, email from users where email like %s limit 100
    ''', (email_like,))


    ctx = dict(flask.request.args)
    ctx.update({
        'users': users,
    })
    return flask.render_template('users.html.j2', **ctx)


@app.route('/users/<int:user_id>')
def user_detail(user_id):
    user_data = flask_db.fetch_one('''
    select id, email, ins_ts, upd_ts from users where id=%s
    ''', (user_id,))

    permissions = flask_db.fetch_all('''
    select p.id, p.name
    from user_permissions up
    join permissions p
    on up.permission = p.id
    where up.user = %s
    ''', (user_id,))
    ctx = {
        'details': user_data,
        'permissions': permissions,
    }
    return flask.render_template('user_detail.html.j2', **ctx)


@app.route('/users/<int:user_id>/permissions', methods=['POST'])
def add_user_permission(user_id):
    permission_name = flask.request.form['permision_name']

    permission_id = flask_db.insert('''
    insert into permissions (name)
    values (UPPER(%s))
    on duplicate key update id=id
    ''', (permission_name,))

    flask_db.insert('''
    insert into user_permissions (user, permission)
    values (%s, %s)
    ''', (user_id, permission_id))

    return flask.redirect(
        flask.url_for('user_detail', user_id=user_id)
    )


@app.route('/users/<int:user_id>/permissions/<int:permission_id>/delete', methods=['GET'])
def delete_user_permissions(user_id, permission_id):
    flask_db.delete('''
    delete from user_permissions where user = %s and permission = %s
    ''', (user_id, permission_id))
    return flask.redirect(flask.url_for('user_detail', user_id=user_id))


@app.route('/users/create', methods=['POST'])
def create_users():
    email = flask.request.form['email']
    password = flask.request.form['password']

    hashed_pass = auth.hash_password(password)

    try:
        flask_db.insert('''
        insert into users (email, passwd)
        values (%s, %s)
        ''', (email, hashed_pass))
    except mysql.connector.errors.IntegrityError:
        flask.flash(('danger', f'User with email {email} already registered'))

    return flask.redirect(flask.url_for('users'))


@app.route('/users/<int:user_id>/delete', methods=['GET'])
def delete_user(user_id):
    flask_db.delete('''
    delete from users where id=%s
    ''', (user_id,))
    return flask.redirect(flask.url_for('users'))
