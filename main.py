import streamlit as st

st.set_page_config(
    page_title="구름 종류 알아보기",
    page_icon="☁️",
    layout="wide"
)

home_page = st.Page(
    "main_page.py",
    title="main",
    icon="☁️",
    default=True
)

result_page = st.Page(
    "pages/result.py",
    title="구름 분석 결과",
    icon="🔎"
)

pg = st.navigation(
    [home_page, result_page],
    position="sidebar",
    expanded=True
)

pg.run()
