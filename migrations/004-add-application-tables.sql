create table oauth_apps (
    id integer primary key auto_increment;
    appname varchar(256) not null;
    redirect_uri varchar(2048) not null;
    client_id varchar(256) not null;
    client_secret varchar(1024) not null;
);
