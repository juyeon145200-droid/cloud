
import streamlit as st
import random

# 메인 화면 제목
st.title("☁️ 하늘 사진으로 구름 종류 알아보기")

st.write(
    "하늘 사진을 업로드하면 생성형 AI가 "
    "사진 속 구름의 종류를 분석합니다."
)

st.divider()

# 하늘 사진 업로드
st.subheader("📸 하늘 사진 업로드")

uploaded_file = st.file_uploader(
    "분석할 하늘 사진을 선택하세요.",
    type=["jpg", "jpeg", "png"]
)

# 업로드한 사진 저장 및 표시
if uploaded_file is not None:
    st.session_state["uploaded_image"] = uploaded_file

    st.success("사진이 성공적으로 업로드되었습니다!")

    st.image(
        uploaded_file,
        caption="업로드한 하늘 사진",
        use_container_width=True
    )

    st.write(
        "왼쪽 메뉴에서 '구름 분석 결과'를 선택한 후 "
        "구름 분석을 시작하세요."
    )

else:
    st.info("분석할 하늘 사진을 업로드해 주세요.")

# 기상 명언 목록
weather_quotes = [
    {
        "quote": "하늘을 관찰하는 것은 자연의 변화를 읽는 첫걸음이다.",
        "author": "기상 관측의 의미를 담은 문구"
    },
    {
        "quote": "날씨를 이해하는 것은 지구의 이야기를 읽는 것이다.",
        "author": "기상 과학의 의미를 담은 문구"
    },
    {
        "quote": "작은 구름의 변화도 날씨를 알려주는 단서가 된다.",
        "author": "기상 관측의 의미를 담은 문구"
    },
    {
        "quote": "하늘은 매일 새로운 모습으로 우리에게 신호를 보낸다.",
        "author": "자연 관찰의 의미를 담은 문구"
    },
    {
        "quote": "정확한 예보는 세심한 관찰에서 시작된다.",
        "author": "기상 예보의 의미를 담은 문구"
    },
    {
        "quote": "구름은 대기의 움직임을 보여주는 자연의 기록이다.",
        "author": "기상 과학의 의미를 담은 문구"
    },
    {
        "quote": "자연의 변화를 이해하면 미래의 날씨를 예측할 수 있다.",
        "author": "기상 예측의 의미를 담은 문구"
    },
    {
        "quote": "하늘을 읽는 눈이 날씨를 이해하는 힘이 된다.",
        "author": "기상 관측의 의미를 담은 문구"
    },
    {
        "quote": "오늘의 하늘을 관찰하면 내일의 날씨를 생각할 수 있다.",
        "author": "기상 관측의 의미를 담은 문구"
    },
    {
        "quote": "날씨는 끊임없이 변하고, 관측은 그 변화를 기록한다.",
        "author": "기상 과학의 의미를 담은 문구"
    }
]

st.divider()

# 오늘의 기상 명언
st.subheader("☁️ 오늘의 기상 한마디")

# 처음 접속했을 때 명언 무작위 선택
if "weather_quote" not in st.session_state:
    st.session_state["weather_quote"] = random.choice(
        weather_quotes
    )

# 선택된 명언 출력
quote = st.session_state["weather_quote"]

st.info(
    f"💬 \"{quote['quote']}\"\n\n"
    f"— {quote['author']}"
)

# 다른 명언 보기
if st.button("🔄 다른 명언 보기"):
    current_quote = st.session_state["weather_quote"]

    other_quotes = [
        q for q in weather_quotes
        if q != current_quote
    ]

    st.session_state["weather_quote"] = random.choice(
        other_quotes
    )

    st.rerun()
