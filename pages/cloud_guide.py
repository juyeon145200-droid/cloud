
import streamlit as st
from datetime import date

st.title("☁️ 나만의 구름 도감")

st.write(
    "구름 분석 결과 페이지에서 자동으로 저장된 "
    "사진과 분석 결과를 모아 볼 수 있어요!"
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
# 자동 저장된 구름 도감 보여 주기
# -----------------------------
entries = st.session_state["cloud_guide_entries"]

st.subheader("📚 나의 구름 도감")
st.write(f"현재 등록된 구름: **{len(entries)}개**")

if not entries:
    st.info(
        "아직 저장된 구름이 없어요. "
        "'구름 분석 결과' 페이지에서 사진을 분석해 주세요."
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
        if search_name.strip() in entry.get("name", "")
    ]

    if not filtered_entries:
        st.warning("검색어와 일치하는 구름이 없습니다.")

    else:
        # 최신 기록부터 표시
        filtered_entries = list(reversed(filtered_entries))

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
                        # 자동 저장된 사진 표시
                        photo = entry.get("image")

                        if photo:
                            st.image(
                                photo,
                                use_container_width=True
                            )
                        else:
                            st.info("저장된 사진이 없습니다.")

                        st.subheader(entry.get("name", "구름 종류 미확인"))

                        st.caption(
                            f"📅 관측 날짜: "
                            f"{entry.get('date', '날짜 정보 없음')}"
                        )

                        # 자동 분석 결과 추가 표시
                        if entry.get("english_name"):
                            st.write(
                                f"**영어 이름:** {entry['english_name']}"
                            )

                        if entry.get("confidence") is not None:
                            st.write(
                                f"**분석 신뢰도:** "
                                f"{entry['confidence']}%"
                            )

                        st.write("**구름의 특징**")
                        st.write(
                            entry.get("feature", "정보 없음")
                        )

                        if entry.get("formation_cause"):
                            st.write("**생성 원인**")
                            st.write(entry["formation_cause"])

                        if entry.get("altitude"):
                            st.write("**주로 나타나는 고도**")
                            st.write(entry["altitude"])

                        if entry.get("weather"):
                            st.write("**관련 날씨**")
                            st.write(entry["weather"])

                        if entry.get("explanation"):
                            with st.expander("💡 AI가 판단한 이유"):
                                st.write(entry["explanation"])

                        if entry.get("filename"):
                            st.caption(
                                f"📁 원본 파일명: {entry['filename']}"
                            )

                        if entry.get("analysis_time"):
                            st.caption(
                                f"🕒 분석 일시: {entry['analysis_time']}"
                            )

# -----------------------------
# 도감 초기화
# -----------------------------
st.divider()

with st.expander("⚙️ 도감 관리"):
    st.write(
        "현재 세션에 등록된 도감 내용을 모두 지울 수 있어요."
    )

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
