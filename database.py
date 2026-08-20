import os
import asyncio
from libsql_client import create_client

# Turso URL va Token'ni Environment Variables orqali olamiz
TURSO_URL = os.environ.get("TURSO_URL", "libsql://stick-war-behruz123109-jpg.aws-us-east-1.turso.io")
TURSO_TOKEN = os.environ.get("TURSO_TOKEN", "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJhIjoicnciLCJpYXQiOjE3ODcyNDEwODEsImlkIjoiMDFhMDFmZDYtMmMwMS03OTg1LTgwZWItODcyMmQ0NmMxM2I3Iiwia2lkIjoiSm5ENE53Nnp0ZUt0RDVoOGRZWW00YlEtcDNYdGNqT1l2MWh1b2hBQnNmTSIsInJpZCI6IjZkMjg0MjE5LTllOGQtNDVjMC1hMTZiLThlNTc1MjVkMzYzNSJ9.tEcKwsZuvhcSTTXgWDg8ZRlwJQ0IhPxV51-JaErAy2Ghm2XNbb6w4ijVahtOANUrKRZqisuk5nP-Fhcf_i0HAQ")

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
