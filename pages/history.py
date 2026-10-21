
import streamlit as st
import pandas as pd

st.title("📋 구름 관측 기록표")

st.write(
    "AI가 분석한 구름의 종류와 특징이 자동으로 기록됩니다."
)

# 저장된 기록 가져오기
if "cloud_history" not in st.session_state:
    st.session_state["cloud_history"] = []

history = st.session_state["cloud_history"]

if not history:
    st.info(
        "아직 저장된 관측 기록이 없습니다. "
        "먼저 하늘 사진을 업로드하고 구름 분석을 진행해 주세요."
    )

else:
    df = pd.DataFrame(history)

    st.subheader("📊 관측 기록")

    st.write(f"총 관측 횟수: **{len(df)}회**")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # CSV 파일 다운로드
    csv_data = df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        label="📥 관측 기록 CSV 다운로드",
        data=csv_data,
        file_name="구름_관측_기록.csv",
        mime="text/csv"
    )

    st.divider()

    st.subheader("☁️ 구름 종류별 관측 횟수")

    counts = df["구름 종류"].value_counts()

    st.bar_chart(counts)

    st.caption(
        "이 기록은 현재 앱 세션에 저장됩니다. "
        "세션이 초기화되면 기록이 사라질 수 있으므로 "
        "필요한 기록은 CSV 파일로 다운로드해 주세요."
    )
