alter table oauth_apps add column client_type enum("public", "confidential") default "public" after client_secret;
