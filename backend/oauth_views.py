import flask
from lib import oauth2, flask_db
from urllib.parse import urlencode
blueprint = flask.Blueprint('oauth', __name__, url_prefix='/oauth')


@blueprint.route('/')
def consent_prompt():
    errors = []

    required_args = ['redirect_uri', 'client_id', 'scope', 'state']
    errors = [
        f'Argument \'{argname}\' is not specified'
        for argname in required_args if argname not in flask.request.args
    ]

    if errors:
        return flask.render_template('oauth_error.html.j2', errors=errors)


    if 'user_id' not in flask.session:
        forward_args = {name: flask.request.args[name] for name in required_args}
        self_url = flask.url_for('oauth.consent_prompt', **forward_args)

        fwd_params = {
            'scopes': '',
            'client_id': '',
            'redirect_url': '',
            'state': '',
        }

        return flask.redirect(flask.url_for(
            'login', after_redirect=self_url,
            **fwd_params
        ))

    ctx = {
        'redirect_uri': 'http://localhost:3000',
        'state': flask.request.args['state'],
        'scopes': ['test1', 'test2', 'test3']
    }
    return flask.render_template('oauth_prompt.html.j2', **ctx)


@blueprint.route('/build-tokens', methods=['POST'])
def build_token():
    params = {
        'state': flask.request.form['state'],
    }

    if 'grant' not in flask.request.form:
        params['error'] = 'no consent given'
    else:
        permissions = flask_db.fetch_all('''
        select name from permissions
        where id in (
            select up.permission from user_permissions up
            where up.user = %s
        )
        ''', (flask.session['user_id'],))
        permissions_names = {p.name for p in permissions}

        claims = {
            'auths': ' '.join(permissions_names)
        }

        jwt = oauth2.create_jwt('/home/web/.ssh/id_rsa', claims=claims)
        # create client id
        params['access_token'] = jwt
        pass

    redirect_url = flask.request.form['redirect_uri'] + '?' + urlencode(params)
    print(redirect_url, flush=True)
    return flask.redirect(redirect_url)


@blueprint.route('/.well-known/jwks.json')
def public_certs():
    key = oauth2.pubkey_info('/home/web/.ssh/id_rsa.pub')

    response = flask.Response(
        flask.json.dumps({
        'keys': [ key ]
    }), mimetype='application/json'
    )
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response
