import sqlite3


# =====================================================
# DATABASE FILE
# =====================================================

DATABASE_NAME = "maintenance.db"


# =====================================================
# CREATE DATABASE TABLE
# =====================================================

def create_database():

    connection = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = connection.cursor()


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


    connection.commit()

    connection.close()


# =====================================================
# INSERT WORK ORDER
# =====================================================

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


    connection = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = connection.cursor()


    cursor.execute(

        """
        INSERT INTO work_orders (

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


    connection.commit()

    connection.close()


# =====================================================
# GET ALL WORK ORDERS
# =====================================================

def get_all_work_orders():

    connection = sqlite3.connect(
        DATABASE_NAME
    )


    cursor = connection.cursor()


    cursor.execute(

        """
        SELECT *

        FROM work_orders

        ORDER BY id DESC

        """

    )


    rows = cursor.fetchall()


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


    connection.close()


    return rows, columns


# =====================================================
# UPDATE WORK ORDER STATUS
# =====================================================

def update_work_order_status(

    work_order_id,

    new_status

):


    connection = sqlite3.connect(
        DATABASE_NAME
    )


    cursor = connection.cursor()


    cursor.execute(

        """

        UPDATE work_orders

        SET status = ?

        WHERE work_order_id = ?

        """,

        (

            new_status,

            work_order_id

        )

    )


    connection.commit()

    connection.close()


# =====================================================
# DELETE WORK ORDER
# =====================================================

def delete_work_order(

    work_order_id

):


    connection = sqlite3.connect(

        DATABASE_NAME

    )


    cursor = connection.cursor()


    cursor.execute(

        """

        DELETE FROM work_orders

        WHERE work_order_id = ?

        """,

        (

            work_order_id,

        )

    )


    connection.commit()

    connection.close()


# =====================================================
# INITIALIZE DATABASE
# =====================================================

create_database()