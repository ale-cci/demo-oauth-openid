drop table if exists permissions;
create table permissions (
  id integer not null auto_increment,
  name varchar(32) not null unique,
  primary key (`id`)
);


drop table if exists user_permissions;
create table user_permissions (
  id integer not null auto_increment primary key,
  user integer not null,
  permission integer not null,
  unique key (`user`, `permission`),
);
