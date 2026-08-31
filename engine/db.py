import os
import sqlite3

DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "shinobu.db"
)

DEFAULT_SETTINGS = {
    "assistant_name": "Shinobu",
    "voice_index": "1",
    "rate": "190",
}


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS sys_command("
        "id INTEGER PRIMARY KEY, name VARCHAR(100), path VARCHAR(1000))"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS web_command("
        "id INTEGER PRIMARY KEY, name VARCHAR(100), url VARCHAR(1000))"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS settings("
        "key VARCHAR(50) PRIMARY KEY, value VARCHAR(500))"
    )
    conn.commit()

    for key, value in DEFAULT_SETTINGS.items():
        cur.execute("INSERT OR IGNORE INTO settings(key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()


# ---------------- Settings ----------------

def get_all_settings():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT key, value FROM settings")
    rows = cur.fetchall()
    conn.close()

    settings = dict(DEFAULT_SETTINGS)
    settings.update({key: value for key, value in rows})
    return settings


def save_settings(data):
    conn = get_conn()
    cur = conn.cursor()
    for key, value in (data or {}).items():
        cur.execute(
            "INSERT INTO settings(key, value) VALUES (?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (key, str(value)),
        )
    conn.commit()
    conn.close()


# ---------------- App shortcuts (sys_command) ----------------

def get_sys_commands():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, path FROM sys_command ORDER BY name COLLATE NOCASE")
    rows = cur.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "path": r[2]} for r in rows]


def add_sys_command(name, path):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO sys_command(name, path) VALUES (?, ?)", (name.strip(), path.strip()))
    conn.commit()
    conn.close()


def get_sys_command_path(name):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT path FROM sys_command WHERE LOWER(name) = LOWER(?)", (name,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None


def delete_sys_command(item_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM sys_command WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()


# ---------------- Website shortcuts (web_command) ----------------

def get_web_commands():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, url FROM web_command ORDER BY name COLLATE NOCASE")
    rows = cur.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "url": r[2]} for r in rows]


def add_web_command(name, url):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO web_command(name, url) VALUES (?, ?)", (name.strip(), url.strip()))
    conn.commit()
    conn.close()


def get_web_command_url(name):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT url FROM web_command WHERE LOWER(name) = LOWER(?)", (name,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None


def delete_web_command(item_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM web_command WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()


init_db()