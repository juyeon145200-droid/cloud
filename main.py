
import streamlit as st

# 기본 페이지 설정
st.set_page_config(
    page_title="구름 종류 알아보기",
    page_icon="☁️",
    layout="wide"
)

# 1. 메인 화면: 하늘 사진 업로드
home_page = st.Page(
    "main_page.py",
    title="하늘 사진 업로드",
    icon="☁️",
    default=True
)

# 2. 구름 분석 결과 화면
result_page = st.Page(
    "pages/result.py",
    title="구름 분석 결과",
    icon="🔎"
)

# 3. 구름 관측 기록표 화면
history_page = st.Page(
    "pages/history.py",
    title="구름 관측 기록표",
    icon="📋"
)

# 4. 물방울 레이스 게임 화면
race_page = st.Page(
    "pages/race.py",
    title="물방울 레이스",
    icon="💧"
)

# 페이지 메뉴 구성
pg = st.navigation(
    [
        home_page,
        result_page,
        history_page,
        race_page
    ],
    position="sidebar",
    expanded=True
)

# 선택한 페이지 실행
pg.run()
