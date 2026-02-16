import sqlite3
import time

conn = sqlite3.connect("casino.db", check_same_thread=False)
cursor = conn.cursor()

# USERS TABLOSU
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    balance INTEGER DEFAULT 1000,
    last_claim INTEGER DEFAULT 0,
    total_won INTEGER DEFAULT 0,
    total_lost INTEGER DEFAULT 0,
    total_games INTEGER DEFAULT 0
)
""")
conn.commit()


# KULLANICI VAR MI KONTROL
def get_user(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = cursor.fetchone()

    if not user:
        cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        conn.commit()

    return user


# BAKİYE
def get_balance(user_id):
    get_user(user_id)
    cursor.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
    return cursor.fetchone()[0]


def update_balance(user_id, amount):
    get_user(user_id)
    cursor.execute(
        "UPDATE users SET balance = balance + ? WHERE user_id=?",
        (amount, user_id)
    )
    conn.commit()



# 📊 İSTATİSTİK
def add_win(user_id, amount):
    cursor.execute("""
        UPDATE users
        SET total_won = total_won + ?,
            total_games = total_games + 1
        WHERE user_id=?
    """, (amount, user_id))
    conn.commit()


def add_loss(user_id, amount):
    cursor.execute("""
        UPDATE users
        SET total_lost = total_lost + ?,
            total_games = total_games + 1
        WHERE user_id=?
    """, (amount, user_id))
    conn.commit()


def get_stats(user_id):
    cursor.execute("""
        SELECT total_won, total_lost, total_games
        FROM users
        WHERE user_id=?
    """, (user_id,))
    return cursor.fetchone()




