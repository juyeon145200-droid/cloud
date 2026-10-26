
import streamlit as st
import pandas as pd

st.title("📋 구름 관측 기록표")

# 기록 목록 초기화
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

    # 기존 기록에 새 항목이 없더라도 오류가 발생하지 않도록 처리
    normalized_history = []

    for record in history:
        normalized_record = {
            column: record.get(column, "이전 기록에는 정보가 없어요.")
            for column in columns
        }
        normalized_history.append(normalized_record)

    df = pd.DataFrame(normalized_history, columns=columns)

    st.write(f"총 관측 기록: **{len(df)}개**")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # CSV 다운로드
    csv = df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        label="📥 관측 기록 CSV 다운로드",
        data=csv,
        file_name="구름_관측_기록.csv",
        mime="text/csv"
    )
