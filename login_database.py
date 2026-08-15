import sqlite3
import hashlib
import os
import streamlit as st


# =====================================================
# DATABASE LOCATION
# =====================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(
    BASE_DIR,
    "login.db"
)


# =====================================================
# DATABASE CONNECTION
# =====================================================

def get_connection():

    return sqlite3.connect(DB_PATH)


# =====================================================
# HASH PASSWORD
# =====================================================

def hash_password(password):

    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# =====================================================
# CREATE TABLE
# =====================================================

def create_table():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL,

            role TEXT NOT NULL

        )
        """
    )

    conn.commit()

    conn.close()


# =====================================================
# CREATE / UPDATE USER
# =====================================================

def create_user(
    username,
    password,
    role
):

    conn = get_connection()

    cursor = conn.cursor()

    hashed_password = hash_password(password)

    cursor.execute(
        """
        INSERT OR REPLACE INTO users
        (
            username,
            password,
            role
        )
        VALUES (?, ?, ?)
        """,
        (
            username,
            hashed_password,
            role
        )
    )

    conn.commit()

    conn.close()


# =====================================================
# AUTHENTICATE
# =====================================================

def authenticate(
    username,
    password
):

    conn = get_connection()

    cursor = conn.cursor()

    hashed_password = hash_password(password)

    cursor.execute(
        """
        SELECT username, role

        FROM users

        WHERE username = ?

        AND password = ?
        """,
        (
            username,
            hashed_password
        )
    )

    user = cursor.fetchone()

    conn.close()

    return user


# =====================================================
# CREATE USERS FROM STREAMLIT SECRETS
# =====================================================

def create_default_users():

    create_table()

    users = st.secrets["users"]

    for username in users:

        password = users[username]["password"]

        role = users[username]["role"]

        create_user(
            username,
            password,
            role
        )


# =====================================================
# INITIALIZE DATABASE
# =====================================================

create_default_users()