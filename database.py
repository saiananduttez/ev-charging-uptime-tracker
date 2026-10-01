import sqlite3

def init_db(db_name="ev_network.db"):
    """Creates tables for EV charging stations and status ping events."""
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS station_heartbeats (
        ping_id TEXT PRIMARY KEY,
        station_id TEXT,
        station_name TEXT,
        location_zone TEXT,
        charger_type TEXT,
        power_output_kw REAL,
        status TEXT,
        error_code TEXT,
        recorded_at TIMESTAMP
    );
    """)
    conn.commit()
    conn.close()

def insert_heartbeats(events, db_name="ev_network.db"):
    """Batch inserts station status records."""
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.executemany("""
    INSERT OR IGNORE INTO station_heartbeats 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, events)
    conn.commit()
    conn.close()