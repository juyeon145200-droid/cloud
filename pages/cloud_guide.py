
import streamlit as st
from datetime import date
from io import BytesIO
from PIL import Image


# -----------------------------
# 페이지 설정
# -----------------------------
st.title("☁️ 나만의 구름 도감")
st.write(
    "직접 관찰하거나 촬영한 하늘 사진을 등록하고 "
    "나만의 구름 도감을 만들어 보세요!"
)

st.info(
    "사진과 정보는 현재 세션에서만 보관됩니다. "
    "새로고침하거나 세션이 초기화되면 사라질 수 있습니다."
)


# -----------------------------
# 세션에 도감 목록 만들기
# -----------------------------
if "cloud_guide_entries" not in st.session_state:
    st.session_state["cloud_guide_entries"] = []


# -----------------------------
# 사진과 구름 정보 등록
# -----------------------------
st.subheader("📸 새 구름 등록")

with st.form("cloud_guide_form", clear_on_submit=True):
    uploaded_photo = st.file_uploader(
        "하늘 사진을 업로드하세요.",
        type=["jpg", "jpeg", "png"]
    )

    cloud_name = st.selectbox(
        "구름 종류를 선택하세요.",
        [
            "적운",
            "층운",
            "권운",
            "층적운",
            "고적운",
            "고층운",
            "난층운",
            "권층운",
            "권적운",
            "적란운",
            "잘 모르겠음"
        ]
    )

    observed_date = st.date_input(
        "관측 날짜",
        value=date.today()
    )

    weather_feature = st.text_area(
        "구름의 특징과 관찰한 날씨를 적어 주세요.",
        placeholder="예: 솜사탕처럼 뭉게뭉게 보였고 하늘이 맑았다."
    )

    submitted = st.form_submit_button(
        "☁️ 도감에 등록하기",
        use_container_width=True
    )


# -----------------------------
# 등록 버튼을 눌렀을 때
# -----------------------------
if submitted:
    if uploaded_photo is None:
        st.warning("먼저 하늘 사진을 업로드해 주세요.")

    elif not weather_feature.strip():
        st.warning("구름의 특징을 한 문장 이상 적어 주세요.")

    else:
        try:
            # 사진 파일을 세션에 보관할 수 있는 바이트로 변환
            photo_bytes = uploaded_photo.getvalue()

            # 이미지 파일인지 확인
            Image.open(BytesIO(photo_bytes)).verify()

            # 도감에 등록할 정보 만들기
            new_entry = {
                "name": cloud_name,
                "date": observed_date.strftime("%Y-%m-%d"),
                "feature": weather_feature.strip(),
                "image": photo_bytes,
                "filename": uploaded_photo.name
            }

            # 세션의 도감 목록에 추가
            st.session_state["cloud_guide_entries"].append(new_entry)

            st.success("도감에 구름 사진과 정보가 등록되었습니다!")

        except Exception:
            st.error(
                "사진을 읽을 수 없습니다. "
                "다른 JPG 또는 PNG 사진을 선택해 주세요."
            )


st.divider()


# -----------------------------
# 등록된 구름 도감 보여 주기
# -----------------------------
entries = st.session_state["cloud_guide_entries"]

st.subheader("📚 나의 구름 도감")
st.write(f"현재 등록된 구름: **{len(entries)}개**")

if not entries:
    st.info(
        "아직 등록된 구름이 없어요. "
        "위에서 사진을 업로드하고 첫 번째 구름을 등록해 보세요!"
    )

else:
    # 이름으로 도감 검색
    search_name = st.text_input(
        "🔍 구름 이름 검색",
        placeholder="예: 적운"
    )

    # 검색어에 맞는 구름만 표시
    filtered_entries = [
        entry for entry in entries
        if search_name.strip() in entry["name"]
    ]

    if not filtered_entries:
        st.warning("검색어와 일치하는 구름이 없습니다.")

    else:
        # 두 개씩 카드 형태로 배치
        for start in range(0, len(filtered_entries), 2):
            cols = st.columns(2)

            for offset, col in enumerate(cols):
                index = start + offset

                if index >= len(filtered_entries):
                    break

                entry = filtered_entries[index]

                with col:
                    with st.container(border=True):
                        st.image(
                            entry["image"],
                            use_container_width=True
                        )

                        st.subheader(entry["name"])
                        st.caption(f"📅 관측 날짜: {entry['date']}")
                        st.write("**관찰한 특징**")
                        st.write(entry["feature"])

                        st.caption(
                            f"📁 원본 파일명: {entry['filename']}"
                        )


# -----------------------------
# 도감 초기화
# -----------------------------
st.divider()

with st.expander("⚙️ 도감 관리"):
    st.write("현재 세션에 등록된 도감 내용을 모두 지울 수 있어요.")

    confirm_delete = st.checkbox(
        "등록된 모든 구름을 삭제하는 것에 동의합니다.",
        key="confirm_cloud_guide_delete"
    )

    if st.button("🗑️ 도감 전체 초기화"):
        if confirm_delete:
            st.session_state["cloud_guide_entries"] = []
            st.success("도감을 초기화했습니다.")
            st.rerun()
        else:
            st.warning("먼저 삭제 확인 항목을 체크해 주세요.")
