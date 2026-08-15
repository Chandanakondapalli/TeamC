import sqlite3


# =====================================================
# DATABASE CONNECTION
# =====================================================

conn = sqlite3.connect(
    "preventive_maintenance.db",
    check_same_thread=False
)

cursor = conn.cursor()


# =====================================================
# CREATE TABLE
# =====================================================

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS preventive_schedule (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        schedule_id TEXT,

        product_id TEXT,

        machine_id INTEGER,

        technician TEXT,

        frequency TEXT,

        task TEXT,

        status TEXT,

        next_date TEXT,

        created_date TEXT

    )
    """
)

conn.commit()


# =====================================================
# CREATE SCHEDULE
# =====================================================

def create_schedule(
        schedule_id,
        product_id,
        machine_id,
        technician,
        frequency,
        task,
        status,
        next_date,
        created_date
):

    cursor.execute(
        """
        INSERT INTO preventive_schedule
        VALUES (
            NULL,
            ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        """,
        (
            schedule_id,
            product_id,
            machine_id,
            technician,
            frequency,
            task,
            status,
            next_date,
            created_date
        )
    )

    conn.commit()


# =====================================================
# GET ALL SCHEDULES
# =====================================================

def get_schedules():

    cursor.execute(
        """
        SELECT * FROM preventive_schedule
        """
    )

    rows = cursor.fetchall()

    columns = [

        "id",
        "schedule_id",
        "product_id",
        "machine_id",
        "technician",
        "frequency",
        "task",
        "status",
        "next_date",
        "created_date"
    ]

    return rows, columns


# =====================================================
# UPDATE STATUS
# =====================================================

def update_schedule(schedule_id, status):

    cursor.execute(
        """
        UPDATE preventive_schedule
        SET status = ?
        WHERE schedule_id = ?
        """,
        (
            status,
            schedule_id
        )
    )

    conn.commit()


# =====================================================
# DELETE SCHEDULE
# =====================================================

def delete_schedule(schedule_id):

    cursor.execute(
        """
        DELETE FROM preventive_schedule
        WHERE schedule_id = ?
        """,
        (
            schedule_id,
        )
    )

    conn.commit()
def create_history_table():

    conn = sqlite3.connect(
        "preventive.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS maintenance_history (

            history_id TEXT,

            schedule_id TEXT,

            technician TEXT,

            status TEXT,

            completion_date TEXT,

            remarks TEXT

        )
        """
    )

    conn.commit()

    conn.close()    
def add_history(
        schedule_id,
        technician,
        status,
        completion_date,
        remarks
):

    conn = sqlite3.connect(
        "preventive.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO maintenance_history
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            str(uuid.uuid4()),
            schedule_id,
            technician,
            status,
            completion_date,
            remarks
        )
    )

    conn.commit()

    conn.close()    
    