"""Database models — SQLite setup for AI Navigator."""
import sqlite3, os

DB = os.path.join(os.path.dirname(__file__), 'ai_tools.db')

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def create_tables():
    db = get_db()
    db.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            theme TEXT DEFAULT 'dark',
            language TEXT DEFAULT 'en',
            notify_email TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            icon TEXT DEFAULT '🤖',
            description TEXT DEFAULT '',
            tool_count INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS tools (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            tagline TEXT DEFAULT '',
            description TEXT DEFAULT '',
            category TEXT DEFAULT '',
            rating REAL DEFAULT 4.0,
            pricing TEXT DEFAULT 'Free',
            url TEXT DEFAULT '',
            logo TEXT DEFAULT '🤖',
            features TEXT DEFAULT '',
            use_cases TEXT DEFAULT '',
            is_trending INTEGER DEFAULT 0,
            is_new INTEGER DEFAULT 0,
            source TEXT DEFAULT 'seed',
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            tool_id INTEGER,
            rating INTEGER DEFAULT 5,
            comment TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            query TEXT,
            results_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            message TEXT,
            page TEXT DEFAULT '',
            rating INTEGER DEFAULT 5,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            message TEXT,
            is_read INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS discovery_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT,
            tools_found INTEGER DEFAULT 0,
            tools_added INTEGER DEFAULT 0,
            status TEXT DEFAULT 'ok',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS site_stats (
            key TEXT PRIMARY KEY,
            value TEXT DEFAULT '',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    # Add columns to existing tools table if missing (safe migration)
    try: db.execute('ALTER TABLE tools ADD COLUMN source TEXT DEFAULT "seed"')
    except: pass
    try: db.execute('ALTER TABLE tools ADD COLUMN last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
    except: pass
    db.commit()
    db.close()

if __name__ == '__main__':
    create_tables()
    print("[OK] Database tables created!")
