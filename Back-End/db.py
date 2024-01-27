import sqlite3

def create_database_and_tables():
    conn = sqlite3.connect('blog.db')

    c = conn.cursor()

    # Create User table
    c.execute('''
        CREATE TABLE User (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Create Articles table
    c.execute('''
        CREATE TABLE Articles (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            content TEXT NOT NULL,
            slug TEXT NOT NULL,
            date TEXT NOT NULL,
            user_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES User(id)
        )
    ''')

    # Create Comments table
    c.execute('''
        CREATE TABLE Comments (
            id INTEGER PRIMARY KEY,
            content TEXT NOT NULL,
            date TEXT NOT NULL,
            user_id INTEGER,
            article_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES User(id),
            FOREIGN KEY(article_id) REFERENCES Articles(id)
        )
    ''')

    conn.commit()
    conn.close()

create_database_and_tables()