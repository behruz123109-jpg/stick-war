import sqlite3

DB_NAME = "game_data.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Foydalanuvchilar jadvali
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            google_id TEXT UNIQUE,
            username TEXT,
            gems INTEGER DEFAULT 0,
            gold INTEGER DEFAULT 500,
            ads_watched_chest INTEGER DEFAULT 0,
            ads_watched_gem INTEGER DEFAULT 0
        )
    ''')
    
    # Admin sozlamalari jadvali
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_config (
            key TEXT PRIMARY KEY,
            value INTEGER
        )
    ''')
    
    # Boshlang'ich limitlarni o'rnatish
    cursor.execute("INSERT OR IGNORE INTO admin_config VALUES ('daily_chest_limit', 5)")
    cursor.execute("INSERT OR IGNORE INTO admin_config VALUES ('daily_gem_limit', 10)")
    cursor.execute("INSERT OR IGNORE INTO admin_config VALUES ('gem_reward_amount', 15)")
    
    conn.commit()
    conn.close()

def get_config():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT key, value FROM admin_config")
    rows = cursor.fetchall()
    conn.close()
    return {row[0]: row[1] for row in rows}

def update_config(key: str, value: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE admin_config SET value = ? WHERE key = ?", (value, key))
    conn.commit()
    conn.close()

init_db()
