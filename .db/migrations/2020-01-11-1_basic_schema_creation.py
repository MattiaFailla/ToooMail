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
        id integer PRIMARY KEY,         -- unique setting entry id
        service_name text NOT NULL,     -- display name of the service
        server_smtp text,               -- smtp server address
        server_imap text,               -- imap server address
        ssl text,                       -- ssl setting
        ssl_context text,               -- ssl_context setting
        starttls text                   -- starttls setting
    );
    
    CREATE TABLE IF NOT EXISTS mails (
        id integer PRIMARY KEY,         -- the entry id
        uuid text NOT NULL,             -- the mail uuid
        subject text,                   -- the mail subject
        user_id text,                   -- the user id
        folder text,                    -- the folder name
        opened integer,                 -- flag to check if email has been opened
        received text                   -- datetime from the imap server
    );
    
    CREATE TABLE IF NOT EXISTS notes (
        id integer PRIMARY KEY,         -- the note entry id
        uuid text NOT NULL,             -- the mail uuid
        note text,                      -- the note body
        files text,                     -- attached file, must contain fs reference
        saved text                      -- datetime of the last saved note
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
        uuid text NOT NULL,             -- the mail uuid
        subject text,                   -- the mail subject (redundant)
        real_filename text,             -- real filename
        saved_as text,                  -- filename in the local fs
        user_id text,                   -- the user id (owner of the file)
        deleted text,                   -- flag to indicate if the file has been gracefully deleted
        added text                      -- datetime from server
    );"""

