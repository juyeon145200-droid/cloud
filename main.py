
import streamlit as st


# -----------------------------
# 페이지 기본 설정
# -----------------------------
st.set_page_config(
    page_title="날씨와 구름 탐구",
    page_icon="☁️",
    layout="wide"
)


# -----------------------------
# 사이드바 제목 및 안내
# -----------------------------
st.sidebar.title("☁️ 날씨와 구름 탐구")

st.sidebar.write(
    "구름을 관찰하고 날씨를 알아봐요!"
)

st.sidebar.divider()

st.sidebar.caption(
    "하늘 사진을 분석하고, "
    "구름 도감을 만들며, "
    "물방울 레이스도 즐겨 보세요."
)


# -----------------------------
# 페이지 구성
# -----------------------------
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
        "pages/cloud_guide.py",
        title="나만의 구름 도감",
        icon="📚"
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
    )
]


# -----------------------------
# 페이지 이동 메뉴 생성
# -----------------------------
navigation = st.navigation(pages)


# -----------------------------
# 선택한 페이지 실행
# -----------------------------
navigation.run()
