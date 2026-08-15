import sqlite3


# =========================================================
# DATABASE CONNECTION
# =========================================================

DATABASE_NAME = "work_orders.db"


def get_connection():

    return sqlite3.connect(
        DATABASE_NAME,
        check_same_thread=False
    )


# =========================================================
# CREATE TABLE
# =========================================================

def create_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS work_orders (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            work_order_id TEXT UNIQUE,

            product_id TEXT,

            machine_id INTEGER,

            machine_type TEXT,

            technician TEXT,

            priority TEXT,

            task TEXT,

            status TEXT,

            created_date TEXT

        )
        """
    )

    conn.commit()
    conn.close()


# Create table when this file is imported
create_table()


# =========================================================
# CREATE WORK ORDER
# =========================================================

def create_work_order(
    work_order_id,
    product_id,
    machine_id,
    machine_type,
    technician,
    priority,
    task,
    status,
    created_date
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO work_orders
        (
            work_order_id,
            product_id,
            machine_id,
            machine_type,
            technician,
            priority,
            task,
            status,
            created_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            work_order_id,
            product_id,
            machine_id,
            machine_type,
            technician,
            priority,
            task,
            status,
            created_date
        )
    )

    conn.commit()
    conn.close()


# =========================================================
# GET ALL WORK ORDERS
# =========================================================

def get_work_orders():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            work_order_id,
            product_id,
            machine_id,
            machine_type,
            technician,
            priority,
            task,
            status,
            created_date

        FROM work_orders

        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    conn.close()

    columns = [
        "id",
        "work_order_id",
        "product_id",
        "machine_id",
        "machine_type",
        "technician",
        "priority",
        "task",
        "status",
        "created_date"
    ]

    return rows, columns


# =========================================================
# GET TECHNICIAN WORK ORDERS
# =========================================================

def get_technician_work_orders(technician):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            work_order_id,
            product_id,
            machine_id,
            machine_type,
            technician,
            priority,
            task,
            status,
            created_date

        FROM work_orders

        WHERE LOWER(TRIM(technician))
              =
              LOWER(TRIM(?))

        ORDER BY id DESC
        """,
        (technician,)
    )

    rows = cursor.fetchall()

    conn.close()

    columns = [
        "id",
        "work_order_id",
        "product_id",
        "machine_id",
        "machine_type",
        "technician",
        "priority",
        "task",
        "status",
        "created_date"
    ]

    return rows, columns


# =========================================================
# UPDATE WORK ORDER
# =========================================================

def update_work_order(
    work_order_id,
    status
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE work_orders

        SET status = ?

        WHERE work_order_id = ?
        """,
        (
            status,
            work_order_id
        )
    )

    conn.commit()
    conn.close()


# =========================================================
# DELETE WORK ORDER
# =========================================================

def delete_work_order(work_order_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM work_orders

        WHERE work_order_id = ?
        """,
        (work_order_id,)
    )

    conn.commit()
    conn.close()