
import streamlit as st

st.title("☁️ 하늘 사진으로 구름 종류 알아보기")

st.write(
    "하늘 사진을 업로드하면 생성형 AI가 "
    "사진 속 구름의 종류를 분석합니다."
)

st.divider()

st.subheader("📸 하늘 사진 업로드")

# 업로더 초기화에 사용할 번호
if "uploader_version" not in st.session_state:
    st.session_state["uploader_version"] = 0

uploaded_file = st.file_uploader(
    "분석할 하늘 사진을 선택하세요.",
    type=["jpg", "jpeg", "png"],
    key=f"cloud_image_uploader_{st.session_state['uploader_version']}"
)

if uploaded_file is not None:

    st.session_state["uploaded_image"] = uploaded_file

    st.image(
        uploaded_file,
        caption="업로드한 하늘 사진",
        use_container_width=True
    )

    st.success("사진이 업로드되었습니다!")

    if st.button("🗑️ 사진 초기화"):

        st.session_state.pop("uploaded_image", None)

        # 이전 분석 결과도 초기화
        st.session_state.pop("cloud_analysis_result", None)
        st.session_state.pop("cloud_analysis", None)
        st.session_state.pop("analysis_result", None)

        # 업로더를 새로 만들어 선택한 사진 지우기
        st.session_state["uploader_version"] += 1

        st.rerun()

    st.info(
        "왼쪽 메뉴에서 '구름 분석 결과'를 선택하세요."
    )

else:

    st.session_state.pop("uploaded_image", None)

    st.info("먼저 하늘 사진을 업로드해주세요.")

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
