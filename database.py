import sqlite3

DB_NAME = "game.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Foydalanuvchilar jadvali
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            gold INTEGER DEFAULT 500,
            gems INTEGER DEFAULT 0,
            daily_ads_watched INTEGER DEFAULT 0
        )
    ''')
    
    # Admin sozlamalari
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_settings (
            setting_key TEXT PRIMARY KEY,
            setting_value INTEGER
        )
    ''')
    
    # Boshlang'ich sozlamalar
    cursor.execute("INSERT OR IGNORE INTO admin_settings VALUES ('daily_ad_limit', 5)")
    cursor.execute("INSERT OR IGNORE INTO admin_settings VALUES ('gem_reward', 10)")
    
    # Test admin foydalanuvchi
    cursor.execute("INSERT OR IGNORE INTO users (username, gold, gems) VALUES ('admin', 9999, 9999)")
    
    conn.commit()
    conn.close()

def get_setting(key: str) -> int:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT setting_value FROM admin_settings WHERE setting_key = ?", (key,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

def update_user_gems(username: str, amount: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET gems = gems + ? WHERE username = ?", (amount, username))
    conn.commit()
    conn.close()

init_db()
