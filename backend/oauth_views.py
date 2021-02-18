import flask
from lib import oauth2
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
        jwt = oauth2.create_jwt('/home/web/apps/.ssh/id_rsa', claims=[])
        # create client id
        params['access_token'] = jwt
        pass

    redirect_url = flask.request.form['redirect_uri'] + '?' + urlencode(params)
    print(redirect_url, flush=True)
    return flask.redirect(redirect_url)


@blueprint.route('/certs')
def public_certs():
    return flask.jsonify({
        'keys': [
        ]
    })