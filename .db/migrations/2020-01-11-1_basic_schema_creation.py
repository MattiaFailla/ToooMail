def update():
    return """CREATE TABLE IF NOT EXISTS user (
        id integer PRIMARY KEY,
        name text NOT NULL,
        surname text,
        nickname text,
        bio text,
        mail text,
        password text,
        app_password text,
        profilepic text,
        imapserver text,
        smtpserver text,
        is_logged_in integer,
        mail_server_setting,
        created texts
    );
    
    CREATE TABLE IF NOT EXISTS mail_server_settings (
        id integer PRIMARY KEY,
        service_name text NOT NULL,
        server_smtp text,
        server_imap text,
        ssl text,
        ssl_context text,
        starttls text
    );
    
    CREATE TABLE IF NOT EXISTS mails (
        id integer PRIMARY KEY,
        uuid text NOT NULL,
        subject text,
        user_id text,
        folder text,
        opened integer,
        received text
    );
    
    CREATE TABLE IF NOT EXISTS notes (
        id integer PRIMARY KEY,
        uuid text NOT NULL,
        note text,
        files text,
        saved text
    );
    
    CREATE TABLE IF NOT EXISTS contacts (
        id integer PRIMARY KEY, asdf
        name text NOT NULL,
        surname text,
        nick text,
        mail text NOT NULL,
        note text,
        added text
    );
    
    CREATE TABLE IF NOT EXISTS files (
        id integer PRIMARY KEY,
        uuid text NOT NULL,
        subject text,
        real_filename text,
        saved_as text,
        user_id text,
        deleted text,
        added text
    );"""

