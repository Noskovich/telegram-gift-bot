import sqlite3

# Подключение к базе данных
def get_db_connection():
    conn = sqlite3.connect('data/wishlist.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# Инициализация базы данных
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            username TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wishlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            link TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    conn.commit()
    conn.close()

# Регистрация пользователя
def register_user(user_id, username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)', (user_id, username))
    conn.commit()
    conn.close()

# Проверка, зарегистрирован ли пользователь
def is_user_registered(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user is not None

# Добавление ссылки в базу данных
def add_link_to_db(user_id, link):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO wishlist (user_id, link) VALUES (?, ?)', (user_id, link))
    conn.commit()
    conn.close()

# Получение случайной ссылки из списка пользователя
def get_random_link(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT link FROM wishlist WHERE user_id = ?', (user_id,))
    links = cursor.fetchall()
    conn.close()
    return links[0]['link'] if links else None

# Получение всех зарегистрированных пользователей
def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, username FROM users')
    users = [{'user_id': row['user_id'], 'username': row['username']} for row in cursor.fetchall()]
    conn.close()
    return users


def get_user_links(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT link FROM wishlist WHERE user_id = ?', (user_id,))
    links = [row['link'] for row in cursor.fetchall()]
    conn.close()
    return links

def delete_link(user_id, link):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM wishlist WHERE user_id = ? AND link = ?', (user_id, link))
    conn.commit()
    conn.close()
