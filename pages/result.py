
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
        제공된 하늘 사진을 보고 사진 속 구름을 분석해 줘.

        다음 항목을 포함해 한국어 JSON으로 답해.
        다른 설명이나 마크다운 없이 JSON만 출력해.

        {
          "cloud_type": "구름 종류",
          "english_name": "영어 이름",
          "confidence": 70,
          "features": "구름의 모양과 특징",
          "formation_cause": "구름이 생성되는 원인과 형성 과정",
          "altitude": "주로 나타나는 고도와 대략적인 고도 범위",
          "weather": "관련될 수 있는 날씨 특징",
          "explanation": "이 구름이라고 판단한 이유"
        }

        작성 시 다음 사항을 지켜.

        1. 생성 원인은 공기의 상승, 냉각, 수증기 응결,
           대기 상태 등 해당 구름의 일반적인 형성 과정에 맞게 설명해.
        2. 고도는 구름의 종류에 맞춰 낮은 구름, 중간 구름,
           높은 구름 또는 수직 발달 구름 등으로 설명해.
        3. 고도 범위는 일반적으로 알려진 대략적인 범위를 사용해.
           지역과 기상 조건에 따라 달라질 수 있음을 고려해.
        4. 구름의 밑면 높이와 구름이 수직으로 발달하는 높이를
           혼동하지 마.
        5. 사진만으로 구름 종류를 확실히 판단하기 어렵다면
           불확실성을 설명해.
        6. 날씨는 구름만으로 확정할 수 없으므로 가능성으로 설명해.
        7. 사진만으로 확인할 수 없는 대기 상태를 실제로 관측한
           것처럼 단정하지 말고, 일반적인 형성 원리로 설명해.

        confidence는 분석 신뢰도를 나타내는 0~100 사이의 정수야.
        사진만으로 확실하게 판단하기 어려우면 낮은 값으로 표시해.
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

        # 새 항목이 누락된 경우를 위한 기본값
        result.setdefault("formation_cause", "정보 없음")
        result.setdefault("altitude", "정보 없음")

        # 분석 결과를 세션에 저장
        st.session_state["cloud_analysis_result"] = result

        # 관측 기록표에 자동 추가
        record = {
            "관측 일시": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "구름 종류": str(result.get("cloud_type", "알 수 없음")),
            "영어 이름": str(result.get("english_name", "")),
            "신뢰도(%)": result.get("confidence", 0),
            "구름 특징": str(result.get("features", "")),
            "생성 원인": str(result.get("formation_cause", "정보 없음")),
            "주요 고도": str(result.get("altitude", "정보 없음")),
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

    # 추가 기능 1: 구름 생성 원인
    st.subheader("🌱 구름의 생성 원인")
    st.write(result.get("formation_cause", "정보 없음"))

    # 추가 기능 2: 주로 나타나는 고도
    st.subheader("📏 주로 나타나는 고도")
    st.write(result.get("altitude", "정보 없음"))

    st.info(
        "구름의 고도는 종류와 대기 조건에 따라 달라질 수 있어요. "
        "특히 수직으로 발달하는 구름은 여러 고도에 걸쳐 나타날 수 있어요."
    )

    st.subheader("🌦️ 관련 날씨")
    st.write(result.get("weather", "정보 없음"))

    st.subheader("💡 판단 이유")
    st.write(result.get("explanation", "정보 없음"))

    st.caption(
        "AI 분석은 참고용입니다. 구름의 종류나 실제 날씨를 "
        "확정적으로 판단하는 자료로 사용하지 마세요."
    )
