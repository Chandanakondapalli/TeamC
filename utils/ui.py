import streamlit as st


def load_css():
    with open("style.css", "r") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

def hero(title, subtitle):
    st.markdown(
        f'''
        <div class="hero">
            <h1 style="color: #FFFFFF !important;">{title}</h1>
            <span style="color: #E2E8F0 !important; font-size: 21px !important;">
                {subtitle}
            </span>
        </div>
        ''',
        unsafe_allow_html=True
    )


def page_header(icon, title, description):
    html = f"""
<div class="hero">
<h2 style="color:#FFFFFF !important;">{icon} {title}</h2>
<div style="color:#E2E8F0 !important; font-size:21px;">{description}</div>
</div>
"""
    st.markdown(html, unsafe_allow_html=True)


def section(title):
    st.markdown(
        f'<div class="section-title">{title}</div>',
        unsafe_allow_html=True
    )


def divider():
    st.markdown("<hr>", unsafe_allow_html=True)
