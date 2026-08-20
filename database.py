import os
import asyncio
from libsql_client import create_client

# Turso URL va Token'ni Environment Variables orqali olamiz
TURSO_URL = os.environ.get("TURSO_URL", "libsql://stick-war-behruz123109-jpg.aws-us-east-1.turso.io")
TURSO_TOKEN = os.environ.get("TURSO_TOKEN", "libsql://stick-war-behruz123109-jpg.aws-us-east-1.turso.io")

async def init_db():
    async with create_client(TURSO_URL, auth_token=TURSO_TOKEN) as client:
        # Foydalanuvchilar jadvali
        await client.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                gold INTEGER DEFAULT 500,
                gems INTEGER DEFAULT 0,
                daily_ads_watched INTEGER DEFAULT 0
            )
        ''')
        
        # Admin sozlamalari
        await client.execute('''
            CREATE TABLE IF NOT EXISTS admin_settings (
                setting_key TEXT PRIMARY KEY,
                setting_value INTEGER
            )
        ''')
        
        # Boshlang'ich sozlamalar (IGNORE xatosi LibSQL'da INSERT OR IGNORE orqali qilinadi)
        await client.execute("INSERT OR IGNORE INTO admin_settings VALUES ('daily_ad_limit', 5)")
        await client.execute("INSERT OR IGNORE INTO admin_settings VALUES ('gem_reward', 10)")

async def get_setting(key: str) -> int:
    async with create_client(TURSO_URL, auth_token=TURSO_TOKEN) as client:
        result = await client.execute("SELECT setting_value FROM admin_settings WHERE setting_key = ?", [key])
        if result.rows:
            return result.rows[0][0]
        return 0
