
import streamlit as st
import pandas as pd
from PIL import Image
from io import BytesIO

st.title("📋 구름 관측 기록표")

# 관측 기록 목록 초기화
if "cloud_history" not in st.session_state:
    st.session_state["cloud_history"] = []

history = st.session_state["cloud_history"]

if not history:
    st.info(
        "아직 저장된 관측 기록이 없어요. "
        "구름 분석 결과 페이지에서 먼저 사진을 분석해 주세요."
    )

else:
    # 기록표에 표시할 항목
    columns = [
        "관측 일시",
        "구름 종류",
        "영어 이름",
        "신뢰도(%)",
        "구름 특징",
        "생성 원인",
        "주요 고도",
        "관련 날씨",
        "판단 이유"
    ]

    # 이전 기록에 일부 항목이 없어도 오류가 나지 않도록 처리
    normalized_history = []

    for record in history:
        normalized_record = {
            column: record.get(
                column,
                "이전 기록에는 정보가 없어요."
            )
            for column in columns
        }
        normalized_history.append(normalized_record)

    df = pd.DataFrame(
        normalized_history,
        columns=columns
    )

    st.write(f"총 관측 기록: **{len(df)}개**")

    # 1. 전체 관측 기록표
    st.subheader("🗂️ 전체 관측 기록")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # 2. 관측 사진과 상세 정보
    st.subheader("📸 관측 사진 및 상세 정보")

    # 최신 기록부터 표시
    for index, record in enumerate(reversed(history)):
        cloud_name = record.get("구름 종류", "구름 종류 미확인")
        observation_time = record.get("관측 일시", "시간 정보 없음")
        photo_bytes = record.get("사진")
        filename = record.get("사진 파일명", "관측 사진")

        with st.expander(
            f"☁️ {cloud_name} | {observation_time}"
        ):
            if photo_bytes:
                try:
                    image = Image.open(
                        BytesIO(photo_bytes)
                    )
                    st.image(
                        image,
                        caption=filename,
                        use_container_width=True
                    )
                except Exception:
                    st.warning("사진을 표시할 수 없어요.")
            else:
                st.info(
                    "이 기록에는 사진이 저장되어 있지 않아요. "
                    "이전에 생성된 기록일 수 있어요."
                )

            st.write(
                f"**영어 이름:** {record.get('영어 이름', '정보 없음')}"
            )
            st.write(
                f"**분석 신뢰도:** {record.get('신뢰도(%)', '정보 없음')}%"
            )
            st.write(
                f"**구름 특징:** {record.get('구름 특징', '정보 없음')}"
            )
            st.write(
                f"**생성 원인:** {record.get('생성 원인', '정보 없음')}"
            )
            st.write(
                f"**주요 고도:** {record.get('주요 고도', '정보 없음')}"
            )
            st.write(
                f"**관련 날씨:** {record.get('관련 날씨', '정보 없음')}"
            )
            st.write(
                f"**판단 이유:** {record.get('판단 이유', '정보 없음')}"
            )

    st.divider()

    # 3. 구름 종류별 관측 횟수 그래프
    st.subheader("📊 구름 종류별 관측 횟수")

    cloud_counts = df["구름 종류"].value_counts()

    st.bar_chart(
        cloud_counts,
        x_label="구름 종류",
        y_label="관측 횟수",
        color="#66B3FF"
    )

    st.caption(
        "사진을 분석해 기록한 구름 종류별 관측 횟수를 보여 줍니다."
    )

    st.divider()

    # 4. CSV 다운로드
    st.subheader("📥 관측 기록 다운로드")

    csv = df.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        label="📥 관측 기록 CSV 다운로드",
        data=csv,
        file_name="구름_관측_기록.csv",
        mime="text/csv"
    )
