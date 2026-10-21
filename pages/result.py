
import streamlit as st
from google import genai
from PIL import Image
import io
import json
import re

st.set_page_config(
    page_title="구름 분석 결과",
    page_icon="☁️"
)

st.title("🔎 구름 분석 결과")

st.write(
    "업로드한 하늘 사진을 생성형 AI가 분석하여 "
    "구름의 종류와 특징을 알려줍니다."
)

st.divider()

# 업로드한 사진 확인
uploaded_file = st.session_state.get("uploaded_image")

if uploaded_file is None:
    st.warning(
        "먼저 메인 페이지에서 하늘 사진을 업로드해주세요."
    )
    st.stop()

# 사진 표시
st.subheader("📸 분석할 사진")
st.image(
    uploaded_file,
    caption="업로드한 하늘 사진",
    use_container_width=True
)

st.divider()

# Gemini API 키 확인
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)

except Exception:
    st.error(
        "Gemini API 키를 불러오지 못했습니다. "
        "Streamlit Secrets 설정을 확인해주세요."
    )
    st.stop()


# 구름 분석 버튼
if st.button("☁️ 구름 종류 분석하기", type="primary"):

    with st.spinner("AI가 구름 사진을 분석하고 있습니다..."):

        try:
            # 업로드한 이미지 읽기
            image = Image.open(uploaded_file).convert("RGB")

            image_bytes = io.BytesIO()
            image.save(image_bytes, format="JPEG")
            image_data = image_bytes.getvalue()

            # AI에게 전달할 분석 요청
            prompt = """
            당신은 기상 관측을 돕는 AI입니다.
            사진 속 구름을 관찰하고 한국어로 분석하세요.

            다음 10가지 구름 종류 중 가장 적합한 것을 선택하세요.

            1. 권운
            2. 권적운
            3. 권층운
            4. 고적운
            5. 고층운
            6. 층적운
            7. 층운
            8. 난층운
            9. 적운
            10. 적란운

            사진에서 구름이 명확하게 보이지 않으면
            억지로 구름 종류를 단정하지 말고 불확실하다고 설명하세요.

            다음 항목을 포함한 JSON만 출력하세요.
            마크다운 코드 블록은 사용하지 마세요.

            {
                "cloud_type": "구름 종류",
                "english_name": "영어 이름",
                "confidence": 75,
                "features": "사진에서 관찰되는 특징",
                "weather": "관련될 수 있는 날씨 특징",
                "explanation": "이 구름으로 판단한 이유"
            }

            confidence는 0부터 100 사이의 정수로 작성하세요.
            이 값은 AI의 추정 신뢰도이며 실제 정답 확률이
            검증된 수치라고 표현하지 마세요.
            """

            # Gemini 모델을 이용한 사진 분석
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=[
                    prompt,
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": image_data
                        }
                    }
                ]
            )

            response_text = response.text or ""

            # JSON 데이터 추출
            json_match = re.search(
                r"\{.*\}",
                response_text,
                re.DOTALL
            )

            if json_match is None:
                st.error(
                    "분석 결과를 읽을 수 없습니다. "
                    "다시 분석해주세요."
                )
                st.stop()

            result = json.loads(json_match.group())

            # 분석 결과 저장
            st.session_state["cloud_analysis_result"] = result

        except Exception as e:
            st.error(
                "구름 분석 중 오류가 발생했습니다. "
                "잠시 후 다시 시도해주세요."
            )
            st.caption(f"오류 내용: {e}")
            st.stop()


# 분석 결과 표시
result = st.session_state.get("cloud_analysis_result")

if result is not None:

    st.divider()
    st.subheader("🌤️ AI 구름 분석 결과")

    cloud_type = result.get("cloud_type", "알 수 없음")
    english_name = result.get("english_name", "Unknown")
    features = result.get("features", "정보 없음")
    weather = result.get("weather", "정보 없음")
    explanation = result.get("explanation", "정보 없음")

    # 신뢰도 값 확인
    try:
        confidence = int(result.get("confidence", 0))
        confidence = max(0, min(100, confidence))
    except (ValueError, TypeError):
        confidence = 0

    st.success(f"분석된 구름 종류: {cloud_type}")

    st.write(f"**영어 이름:** {english_name}")

    st.write(f"**AI 추정 신뢰도:** {confidence}%")
    st.progress(confidence / 100)

    # 신뢰도에 따른 사용자 안내
    if confidence < 60:
        st.warning(
            "⚠️ AI의 분석 신뢰도가 낮습니다. "
            "사진 속 구름이 선명하게 보이는지 확인하고 "
            "다른 사진으로 다시 분석해 보세요."
        )

    elif confidence < 80:
        st.info(
            "💡 분석 결과는 참고용으로 확인하세요. "
            "사진의 상태에 따라 결과가 달라질 수 있습니다."
        )

    else:
        st.success(
            "구름의 특징을 비교적 명확하게 확인했습니다. "
            "다만 AI 분석 결과가 실제 관측과 일치한다는 "
            "보장은 없습니다."
        )

    st.divider()

    st.subheader("☁️ 구름의 특징")
    st.write(features)

    st.subheader("🌦️ 관련 기상 특징")
    st.write(weather)

    st.subheader("🔍 AI가 판단한 이유")
    st.write(explanation)

    st.divider()

    st.caption(
        "※ AI가 제시한 신뢰도는 검증된 정답 확률이 아닙니다. "
        "구름 사진만으로 실제 날씨를 확정할 수 없으며, "
        "정확한 예보는 공식 기상 정보를 함께 확인하세요."
    )

else:
    st.info(
        "위의 '구름 종류 분석하기' 버튼을 눌러 "
        "사진을 분석해주세요."
    )
