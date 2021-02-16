## OpenID & OAuth2 Demo
> Author: ale-cci

NOTE: this is only a demo, therefore you could see included in git test credentials,
this is not ment to go in production (at least for now).

[License](./LICENSE.md)


### Getting started
The sole depenencies of this project are [docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/).
As soon as you have them downloaded on your system you could start the project
by:

1. Downloading it
```
git clone git@bitbucket.org:ale-cci/demo-oauth-openid.git
cd demo-oauth-openid
```

2. Booting up mysql and the flask server
```
docker-compose up -d
```

3. Go to your browser and perform the login with credentials `test@email.com`
   and `test`



##### Additional notes
- At the moment this project is not ready, and it has been tested only on linux.
- More informations on OAuth2 and OpenID could be found in [my academic dissertion](https://bitbucket.org/ale-cci/tesi-oauth2/src/master/)

