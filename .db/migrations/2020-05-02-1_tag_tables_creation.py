def update():
    return """CREATE TABLE IF NOT EXISTS tags (
        id integer PRIMARY KEY,
        name text NOT NULL,
        user_id text NOT NULL,
        color text NOT NULL
    );

    CREATE TABLE IF NOT EXISTS mails_tag (
        id integer PRIMARY KEY,
        mail text NOT NULL,
        user_id text NOT NULL,
        tag integer NOT NULL
    );"""