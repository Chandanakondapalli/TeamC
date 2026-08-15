import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

DB_PATH = Path("data/facilityops.db")
DB_PATH.parent.mkdir(exist_ok=True)


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS work_orders(
            work_order_id TEXT PRIMARY KEY,
            machine_id TEXT,
            machine_type TEXT,
            priority TEXT,
            maintenance_type TEXT,
            technician TEXT,
            status TEXT,
            created_date TEXT,
            due_date TEXT,
            estimated_cost REAL,
            estimated_time TEXT,
            description TEXT
        )
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS preventive_schedules(
            schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_id TEXT NOT NULL,
            machine_type TEXT,
            maintenance_type TEXT,
            frequency TEXT,
            start_date TEXT,
            next_due_date TEXT,
            technician TEXT,
            priority TEXT,
            status TEXT DEFAULT 'Upcoming',
            created_date TEXT,
            work_order_created INTEGER DEFAULT 0
        )       
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS maintenance_history(
            history_id INTEGER PRIMARY KEY AUTOINCREMENT,
            schedule_id INTEGER,
            machine_id TEXT,
            completion_date TEXT,
            technician TEXT,
            time_taken TEXT,
            cost REAL,
            remarks TEXT,
            status TEXT
        )
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS maintenance_checklists(
            checklist_id INTEGER PRIMARY KEY AUTOINCREMENT,
            schedule_id INTEGER,
            task TEXT,
            completed INTEGER DEFAULT 0,
            completed_by TEXT,
            completed_on TEXT
        )
        """)
        conn.commit()

    create_users_table()
    seed_users()




def generate_work_order_id():
    with get_connection() as conn:
        row = conn.execute(
            "SELECT work_order_id FROM work_orders ORDER BY work_order_id DESC LIMIT 1"
        ).fetchone()

    if row is None:
        return "WO1001"

    number = int(row["work_order_id"][2:])
    return f"WO{number+1}"


def insert_work_order(
    machine_id,
    machine_type,
    priority,
    maintenance_type,
    technician,
    due_date,
    estimated_cost,
    estimated_time,
    description,
):

    work_order_id = generate_work_order_id()

    created_date = datetime.now().strftime("%Y-%m-%d")

    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO work_orders
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                work_order_id,
                machine_id,
                machine_type,
                priority,
                maintenance_type,
                technician,
                "Open",
                created_date,
                due_date,
                float(estimated_cost),
                estimated_time,
                description,
            ),
        )
        conn.commit()

    return work_order_id


def get_all_work_orders():

    with get_connection() as conn:
        return pd.read_sql_query(
            "SELECT * FROM work_orders ORDER BY created_date DESC",
            conn,
        )


def update_work_order(
    work_order_id,
    machine_id,
    machine_type,
    priority,
    maintenance_type,
    technician,
    status,
    due_date,
    estimated_cost,
    estimated_time,
    description,
):

    with get_connection() as conn:
        conn.execute(
            """
            UPDATE work_orders
            SET
                machine_id=?,
                machine_type=?,
                priority=?,
                maintenance_type=?,
                technician=?,
                status=?,
                due_date=?,
                estimated_cost=?,
                estimated_time=?,
                description=?
            WHERE work_order_id=?
            """,
            (
                machine_id,
                machine_type,
                priority,
                maintenance_type,
                technician,
                status,
                due_date,
                estimated_cost,
                estimated_time,
                description,
                work_order_id,
            ),
        )
        conn.commit()


def delete_work_order(work_order_id):

    with get_connection() as conn:
        conn.execute(
            "DELETE FROM work_orders WHERE work_order_id=?",
            (work_order_id,),
        )
        conn.commit()


def get_kpis():

    df = get_all_work_orders()

    return {
        "Total": len(df),
        "Open": len(df[df["status"] == "Open"]),
        "Completed": len(df[df["status"] == "Completed"]),
        "High": len(df[df["priority"] == "High"]),
    }

def get_work_order(work_order_id):

    with get_connection() as conn:

        row = conn.execute(
            "SELECT * FROM work_orders WHERE work_order_id=?",
            (work_order_id,)
        ).fetchone()

    return dict(row) if row else None


def update_work_order_status(work_order_id, status):

    with get_connection() as conn:
        conn.execute(
            """
            UPDATE work_orders
            SET status=?
            WHERE work_order_id=?
            """,
            (status, work_order_id)
        )
        conn.commit()

def insert_preventive_schedule(
    machine_id,
    machine_type,
    maintenance_type,
    frequency,
    start_date,
    technician,
    priority,
):

    # Convert string/date to datetime object
    if isinstance(start_date, str):
        start = datetime.strptime(start_date, "%Y-%m-%d")
    else:
        start = datetime.combine(start_date, datetime.min.time())

    # Calculate next due date
    if frequency == "Weekly":
        next_due = start + timedelta(days=7)
    elif frequency == "Monthly":
        next_due = start + timedelta(days=30)
    elif frequency == "Quarterly":
        next_due = start + timedelta(days=90)
    elif frequency == "Half-Yearly":
        next_due = start + timedelta(days=180)
    elif frequency == "Yearly":
        next_due = start + timedelta(days=365)
    else:
        next_due = start

    created_date = datetime.now().strftime("%Y-%m-%d")

    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO preventive_schedules(
                machine_id,
                machine_type,
                maintenance_type,
                frequency,
                start_date,
                next_due_date,
                technician,
                priority,
                status,
                created_date
            )
            VALUES(?,?,?,?,?,?,?,?,?,?)
            """,
            (
                machine_id,
                machine_type,
                maintenance_type,
                frequency,
                start.strftime("%Y-%m-%d"),
                next_due.strftime("%Y-%m-%d"),
                technician,
                priority,
                "Upcoming",
                created_date,
            ),
        )
        conn.commit()


def get_all_preventive_schedules():

    with get_connection() as conn:
        return pd.read_sql_query(
            """
            SELECT *
            FROM preventive_schedules
            ORDER BY next_due_date
            """,
            conn,
        )



def get_preventive_kpis():

    df = get_all_preventive_schedules()

    if df.empty:
        return {
            "Total": 0,
            "Upcoming": 0,
            "Completed": 0,
            "Overdue": 0
        }

    today = datetime.now().date()

    df["next_due_date"] = pd.to_datetime(df["next_due_date"]).dt.date

    overdue = len(
        df[
            (df["next_due_date"] < today) &
            (df["status"] != "Completed")
        ]
    )

    return {
        "Total": len(df),
        "Upcoming": len(df[df["status"] == "Upcoming"]),
        "Completed": len(df[df["status"] == "Completed"]),
        "Overdue": overdue
    }


def get_upcoming_maintenance(days=7):

    with get_connection() as conn:

        return pd.read_sql_query(
            """
            SELECT *
            FROM preventive_schedules
            WHERE
                date(next_due_date)
                BETWEEN date('now')
                AND date('now', ?)
            ORDER BY next_due_date
            """,
            conn,
            params=(f"+{days} day",)
        )

def get_overdue_maintenance():

    with get_connection() as conn:

        return pd.read_sql_query(
            """
            SELECT *
            FROM preventive_schedules
            WHERE
                date(next_due_date) < date('now')
                AND status!='Completed'
            ORDER BY next_due_date
            """,
            conn,
        )

def update_schedule_status(schedule_id, status):

    with get_connection() as conn:
        conn.execute(
            """
            UPDATE preventive_schedules
            SET status=?
            WHERE schedule_id=?
            """,
            (status, schedule_id)
        )
        conn.commit()

def mark_work_order_created(schedule_id):

    with get_connection() as conn:
        conn.execute(
            """
            UPDATE preventive_schedules
            SET work_order_created=1
            WHERE schedule_id=?
            """,
            (schedule_id,)
        )
        conn.commit()


def add_maintenance_history(
    schedule_id,
    machine_id,
    technician,
):

    completion_date = datetime.now().strftime("%Y-%m-%d")

    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO maintenance_history(
                schedule_id,
                machine_id,
                completion_date,
                technician,
                time_taken,
                cost,
                remarks,
                status
            )
            VALUES(?,?,?,?,?,?,?,?)
            """,
            (
                schedule_id,
                machine_id,
                completion_date,
                technician,
                "2 Hours",
                2500,
                "Preventive maintenance completed.",
                "Completed"
            )
        )

        conn.commit()


def get_maintenance_history():

    with get_connection() as conn:

        return pd.read_sql_query(
            """
            SELECT *
            FROM maintenance_history
            ORDER BY completion_date DESC
            """,
            conn
        )

def update_preventive_schedule(
    schedule_id,
    maintenance_type,
    frequency,
    start_date,
    technician,
    priority
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE preventive_schedules
        SET maintenance_type = ?,
            frequency = ?,
            start_date = ?,
            technician = ?,
            priority = ?
        WHERE schedule_id = ?
    """, (
        maintenance_type,
        frequency,
        start_date,
        technician,
        priority,
        schedule_id
    ))

    conn.commit()
    conn.close()

def delete_preventive_schedule(schedule_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM preventive_schedules
        WHERE schedule_id = ?
    """, (schedule_id,))

    conn.commit()
    conn.close()


# ============================================================
# USERS / AUTHENTICATION
# ============================================================

def create_users_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def seed_users():
    conn = get_connection()
    cursor = conn.cursor()

    users = [
        ("employee", "employee123", "Facility Employee", "Employee"),
        ("sarah", "tech123", "Sarah Wilson", "Technician"),
        ("john", "tech123", "John Smith", "Technician"),
        ("michael", "tech123", "Michael Brown", "Technician"),
        ("david", "tech123", "David Lee", "Technician"),
    ]

    for user in users:
        try:
            cursor.execute("""
                INSERT INTO users
                (username, password, name, role)
                VALUES (?, ?, ?, ?)
            """, user)
        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()


def authenticate_user(username, password, role):

    username = username.strip()
    password = password.strip()
    role = role.strip()

    with get_connection() as conn:

        row = conn.execute(
            """
            SELECT username, name, role
            FROM users
            WHERE LOWER(username) = LOWER(?)
              AND password = ?
              AND role = ?
            """,
            (
                username,
                password,
                role
            )
        ).fetchone()

    if row:

        return {
            "username": row["username"],
            "name": row["name"],
            "role": row["role"]
        }

    return None


def get_technicians():
    conn = get_connection()

    df = pd.read_sql_query("""
        SELECT id, username, name
        FROM users
        WHERE role = 'Technician'
        ORDER BY name
    """, conn)

    conn.close()

    return df


def add_user(username, password, name, role):

    username = username.strip()
    name = name.strip()
    password = password.strip()
    role = role.strip()

    if not username or not password or not name:
        return False, "All fields are required."

    if role not in ["Employee", "Technician"]:
        return False, "Invalid role."

    try:
        with get_connection() as conn:

            conn.execute(
                """
                INSERT INTO users
                (username, password, name, role)
                VALUES (?, ?, ?, ?)
                """,
                (
                    username,
                    password,
                    name,
                    role
                )
            )

            conn.commit()

        return True, "User added successfully."

    except sqlite3.IntegrityError:
        return False, "Username already exists."

    except Exception as e:
        return False, f"Database error: {e}"