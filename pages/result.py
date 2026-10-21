
import streamlit as st
from google import genai
from PIL import Image
from datetime import datetime
import json
import re

st.title("🔎 구름 분석 결과")

# 기록 목록 초기화
if "cloud_history" not in st.session_state:
    st.session_state["cloud_history"] = []

# 이전 분석 결과 불러오기
if "cloud_analysis_result" not in st.session_state:
    st.session_state["cloud_analysis_result"] = None

uploaded_file = st.session_state.get("uploaded_image")

if uploaded_file is None:
    st.warning("먼저 '하늘 사진 업로드' 화면에서 사진을 올려 주세요.")
    st.stop()

st.image(
    uploaded_file,
    caption="분석할 하늘 사진",
    use_container_width=True
)

st.write("사진 속 구름의 종류와 특징을 AI가 분석합니다.")

if st.button("🔍 구름 분석 시작", type="primary"):

    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        client = genai.Client(api_key=api_key)

        uploaded_file.seek(0)
        image = Image.open(uploaded_file).convert("RGB")

        prompt = """
        너는 기상 관측을 돕는 AI야.
        제공된 하늘 사진을 보고 구름을 분석해 줘.

        다음 항목을 포함해 한국어 JSON으로 답해.
        다른 설명이나 마크다운 없이 JSON만 출력해.

        {
          "cloud_type": "구름 종류",
          "english_name": "영어 이름",
          "confidence": 70,
          "features": "구름의 모양과 특징",
          "weather": "관련될 수 있는 날씨 특징",
          "explanation": "이 구름이라고 판단한 이유"
        }

        confidence는 분석 신뢰도를 나타내는 0~100 사이의 정수야.
        사진만으로 확실하게 판단하기 어려우면 낮은 값으로 표시해.
        날씨는 구름만으로 확정할 수 없으므로 가능성으로 설명해.
        """

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=[prompt, image]
        )

        answer = response.text.strip()

        # AI가 JSON 앞뒤에 설명을 붙인 경우에도 JSON 추출 시도
        answer = re.sub(r"^```(?:json)?\s*", "", answer)
        answer = re.sub(r"\s*```$", "", answer)

        match = re.search(r"\{.*\}", answer, re.DOTALL)

        if not match:
            raise ValueError("AI 응답에서 분석 결과를 읽지 못했습니다.")

        result = json.loads(match.group())

        # 분석 결과를 세션에 저장
        st.session_state["cloud_analysis_result"] = result

        # 관측 기록표에 자동 추가
        record = {
            "관측 일시": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "구름 종류": str(result.get("cloud_type", "알 수 없음")),
            "영어 이름": str(result.get("english_name", "")),
            "신뢰도(%)": result.get("confidence", 0),
            "구름 특징": str(result.get("features", "")),
            "관련 날씨": str(result.get("weather", "")),
            "판단 이유": str(result.get("explanation", ""))
        }

        st.session_state["cloud_history"].append(record)

        st.success("분석 결과가 저장되어 관측 기록표에 추가되었습니다!")

    except Exception as e:
        st.error(f"분석 중 오류가 발생했습니다: {e}")

# 저장된 최신 분석 결과 표시
result = st.session_state.get("cloud_analysis_result")

if result:
    st.divider()
    st.subheader("☁️ 분석 결과")

    st.markdown(
        f"### {result.get('cloud_type', '구름 종류 미확인')}"
    )

    st.write(
        f"**영어 이름:** {result.get('english_name', '정보 없음')}"
    )

    confidence = result.get("confidence", 0)

    try:
        confidence = max(0, min(100, int(confidence)))
    except (TypeError, ValueError):
        confidence = 0

    st.write(f"**분석 신뢰도: {confidence}%**")
    st.progress(confidence)

    if confidence < 60:
        st.warning(
            "사진만으로 구름을 판단하기 어려운 결과예요. "
            "참고 자료로 활용해 주세요."
        )
    elif confidence < 80:
        st.info(
            "분석 결과는 참고용이에요. "
            "실제 구름 종류와 다를 수 있어요."
        )
    else:
        st.success(
            "AI가 비교적 높은 신뢰도로 판단했어요. "
            "그래도 결과가 항상 정확한 것은 아니에요."
        )

    st.subheader("🔎 구름의 특징")
    st.write(result.get("features", "정보 없음"))

    st.subheader("🌦️ 관련 날씨")
    st.write(result.get("weather", "정보 없음"))

    st.subheader("💡 판단 이유")
    st.write(result.get("explanation", "정보 없음"))

    st.caption(
        "AI 분석은 참고용입니다. 구름의 종류나 실제 날씨를 "
        "확정적으로 판단하는 자료로 사용하지 마세요."
    )
