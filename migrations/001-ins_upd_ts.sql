alter table users
  add column ins_ts timestamp default current_timestamp after passwd,
  add column upd_ts timestamp default current_timestamp on update current_timestamp after ins_ts;

