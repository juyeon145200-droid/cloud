import streamlit as st


st.title("☁️ 하늘 사진으로 구름 종류 알아보기")

st.write(
    "하늘 사진을 업로드하면 생성형 AI가 "
    "사진 속 구름의 종류를 분석합니다."
)

st.divider()

st.subheader("📸 하늘 사진 업로드")

uploaded_file = st.file_uploader(
    "분석할 하늘 사진을 선택하세요.",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    st.session_state["uploaded_image"] = uploaded_file

    st.image(
        uploaded_file,
        caption="업로드한 하늘 사진",
        use_container_width=True
    )

    st.success(
        "사진이 업로드되었습니다!"
    )

    st.info(
        "왼쪽 메뉴에서 '구름 분석 결과'를 선택하세요."
    )

else:

    st.info(
        "먼저 하늘 사진을 업로드해주세요."
    )

st.divider()

st.markdown(
    """
    ### 🔎 프로그램 이용 방법

    **① 하늘 사진 업로드**

    ↓

    **② 왼쪽 메뉴에서 '구름 분석 결과' 선택**

    ↓

    **③ 생성형 AI가 구름 종류 분석**

    ↓

    **④ 구름의 특징과 날씨 정보 확인**
    """
)
