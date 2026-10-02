import streamlit as st


# 페이지 설정
st.set_page_config(
    page_title="구름 종류 알아보기",
    page_icon="☁️",
    layout="wide"
)


# 페이지 설정
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


# 왼쪽 사이드바 메뉴
pg = st.navigation(
    [home_page, result_page],
    position="sidebar",
    expanded=True
)


# 선택한 페이지 실행
pg.run()
