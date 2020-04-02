def update():
    return """
    
    ALTER TABLE mail_server_settings RENAME TO tmp_mail_server_settings;

    CREATE TABLE IF NOT EXISTS mail_server_settings (
            id integer PRIMARY KEY,
            service_name text NOT NULL,
            server_smtp text,
            server_imap text,
            ssl integer,
            ssl_context integer,
            starttls integer
        );

    DROP TABLE tmp_mail_server_settings;
    """