import sqlite3
import pandas as pd

DB_FILE = "work_orders.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS work_orders (
            wo_id TEXT PRIMARY KEY,
            product_id TEXT NOT NULL,
            issue TEXT NOT NULL,
            priority TEXT NOT NULL,
            technician TEXT NOT NULL,
            due_date TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def add_work_order(wo_id, product_id, issue, priority, technician, due_date, status):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        INSERT INTO work_orders (wo_id, product_id, issue, priority, technician, due_date, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (wo_id, product_id, issue, priority, technician, due_date, status))
    conn.commit()
    conn.close()

def get_work_orders():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM work_orders ORDER BY created_at DESC", conn)
    conn.close()
    return df

def update_work_order_status(wo_id, new_status):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE work_orders SET status = ? WHERE wo_id = ?", (new_status, wo_id))
    conn.commit()
    conn.close()

def delete_work_order(wo_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM work_orders WHERE wo_id = ?", (wo_id,))
    conn.commit()
    conn.close()