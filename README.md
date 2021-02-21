## OpenID & OAuth2 Demo
> Author: ale-cci

NOTE: this is only a demo, therefore you could see included in git test credentials,
this is not ment to go in production (at least for now).

[License](./LICENSE.md)


### Interested in the Database description?
Check out [./doc.md](./doc.md)

### Getting started
The sole depenencies of this project are [docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/).
As soon as you have them downloaded on your system you could start the project
by:

```bash
# 1. Download the project
git clone git@bitbucket.org:ale-cci/demo-oauth-openid.git
cd demo-oauth-openid


# 2. Booting up mysql and the flask server
docker-compose up -d


# 3. Go to your browser on http://localhost:4000 and perform the login with
#    username: test@email.com
#    password: test


# 4. (Optional) Start JWT playground
cd frontend
yarn start

# 5. Done, you are all set up!
```

#### How does it work
1. Project boots up from the docker image, creating a RSA keypair
2. User logs in and creates a public client, and optionally adds new users on the platform
3. Client secrets are used by external application to allow registered users to perform single signon
via OAuth2 & OpenID connect
4. the generated JWT contains user authorizations and are signed with the generated RSA private key
5. Client uses the http://localhost:4000/.well-known/jwks.json endpoint to validate the signed JWT

NOTE: since this is only a demo, all the users could create clients and new users.

##### Additional notes
- At the moment this project is not ready, and it has been tested only on linux.
- More informations on OAuth2 and OpenID could be found in [my academic dissertion](https://bitbucket.org/ale-cci/tesi-oauth2/src/master/)

