alter table permissions
  add column ins_ts timestamp default current_timestamp after name,
  add column upd_ts timestamp default current_timestamp on update current_timestamp after ins_ts;

