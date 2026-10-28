
import streamlit as st

st.set_page_config(
    page_title="날씨와 구름 탐구",
    page_icon="☁️",
    layout="wide"
)

# 사이드바 제목
st.sidebar.title("☁️ 날씨와 구름 탐구")
st.sidebar.write("구름을 관찰하고 날씨를 알아봐요!")

# 페이지 구성
pages = [
    st.Page(
        "main_page.py",
        title="구름 사진 분석",
        icon="📸",
        default=True
    ),
    st.Page(
        "pages/result.py",
        title="구름 분석 결과",
        icon="🔎"
    ),
    st.Page(
        "pages/history.py",
        title="관측 기록",
        icon="📊"
    ),
    st.Page(
        "pages/race.py",
        title="물방울 레이스",
        icon="💧"
    ),
    st.Page(
        "pages/quiz.py",
        title="구름 종류 맞히기 퀴즈",
        icon="🧠"
    )
]

# 페이지 이동 메뉴 생성
navigation = st.navigation(pages)

# 선택한 페이지 실행
navigation.run()
