import streamlit as st


# =====================================================
# CHECK LOGIN
# =====================================================

def require_login():

    if "logged_in" not in st.session_state:

        st.session_state.logged_in = False

    if not st.session_state.logged_in:

        st.warning(
            "🔒 Please login to access this page."
        )

        st.stop()


# =====================================================
# GET CURRENT USER
# =====================================================

def get_current_user():

    return st.session_state.get(
        "username",
        ""
    )


# =====================================================
# GET CURRENT ROLE
# =====================================================

def get_current_role():

    return st.session_state.get(
        "role",
        ""
    )


# =====================================================
# GET TECHNICIAN NAME
# =====================================================

def get_technician_name():

    return st.session_state.get(
        "technician_name",
        ""
    )


# =====================================================
# ADMIN ONLY
# =====================================================

def require_admin():

    require_login()

    if get_current_role() != "Admin":

        st.error(
            "🚫 Access denied. Admin access required."
        )

        st.stop()


# =====================================================
# TECHNICIAN ONLY
# =====================================================

def require_technician():

    require_login()

    if get_current_role() != "Technician":

        st.error(
            "🚫 This page is available only for technicians."
        )

        st.stop()