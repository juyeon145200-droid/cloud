import streamlit as st
from google import genai
from PIL import Image
import io
import json
import re

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="하늘 사진으로 구름 종류 알아보기",
    page_icon="☁️",
    layout="centered"
)

st.title("☁️ 하늘 사진으로 구름 종류 알아보기")
st.write(
    "하늘 사진을 업로드하면 생성형 AI가 사진 속 구름의 종류를 분석해 줍니다."
)

st.info(
    "☁️ 구름 사진을 JPG, JPEG 또는 PNG 형식으로 업로드해 주세요."
)

# -----------------------------
# API 키 확인
# -----------------------------
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("⚠️ Gemini API 키를 찾을 수 없습니다.")
    st.markdown(
        """
        ### Streamlit Cloud 설정 방법

        Streamlit Cloud의

        **Settings → Secrets**

        에 들어가 다음과 같이 입력하세요.

        ```toml
        GEMINI_API_KEY = "여기에_API_키"
        ```
        """
    )
    st.stop()

# Gemini 클라이언트
client = genai.Client(api_key=api_key)

# -----------------------------
# 구름 종류 설명
# -----------------------------
cloud_info = {
    "권운": {
        "english": "Cirrus",
        "description": "높은 고도에서 나타나는 가늘고 실처럼 보이는 구름입니다.",
        "weather": "대체로 맑은 날씨에서 나타나지만 날씨 변화의 전조가 될 수 있습니다."
    },
    "권적운": {
        "english": "Cirrocumulus",
        "description": "작은 구름 알갱이가 물결처럼 배열되어 있는 높은 고도의 구름입니다.",
        "weather": "고도가 높은 곳의 기상 상태를 보여주는 단서가 될 수 있습니다."
    },
    "권층운": {
        "english": "Cirrostratus",
        "description": "하늘을 얇게 덮는 높은 고도의 구름으로 태양이나 달 주변에 후광이 나타나기도 합니다.",
        "weather": "전선이 접근할 때 나타나는 경우가 있습니다."
    },
    "고적운": {
        "english": "Altocumulus",
        "description": "중간 높이에서 작은 덩어리들이 모여 있는 형태의 구름입니다.",
        "weather": "대기의 불안정 정도를 판단하는 데 참고할 수 있습니다."
    },
    "고층운": {
        "english": "Altostratus",
        "description": "중간 고도에서 넓은 영역을 회색 또는 푸른빛으로 덮는 구름입니다.",
        "weather": "비나 눈이 내리기 전 나타나는 경우가 있습니다."
    },
    "층적운": {
        "english": "Stratocumulus",
        "description": "낮은 고도에서 넓게 퍼진 덩어리 형태로 나타나는 구름입니다.",
        "weather": "약한 비가 내리거나 흐린 날씨와 관련될 수 있습니다."
    },
    "층운": {
        "english": "Stratus",
        "description": "낮은 하늘을 안개처럼 넓게 덮는 층 형태의 구름입니다.",
        "weather": "흐린 날씨나 안개와 비슷한 분위기를 만들 수 있습니다."
    },
    "난층운": {
        "english": "Nimbostratus",
        "description": "두껍고 어두운 층 형태의 구름으로 넓은 지역을 덮습니다.",
        "weather": "지속적인 비나 눈과 관련이 있습니다."
    },
    "적운": {
        "english": "Cumulus",
        "description": "하얗고 둥근 솜털처럼 보이며 수직으로 발달하는 구름입니다.",
        "weather": "작은 적운은 맑은 날씨에서 흔하게 볼 수 있습니다."
    },
    "적란운": {
        "english": "Cumulonimbus",
        "description": "수직으로 매우 크게 발달하는 구름으로 강한 대류 현상과 관련됩니다.",
        "weather": "강한 소나기나 천둥·번개가 발생할 수 있는 구름입니다."
    }
}

# -----------------------------
# 이미지 업로드
# -----------------------------
uploaded_file = st.file_uploader(
    "📸 하늘 사진을 업로드하세요",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.subheader("📷 업로드한 사진")

    st.image(
        image,
        caption="분석할 하늘 사진",
        use_container_width=True
    )

    st.write("")

    if st.button("☁️ 구름 종류 분석하기", use_container_width=True):

        with st.spinner("AI가 구름의 모양과 특징을 분석하고 있습니다..."):

            try:
                # 이미지를 JPEG로 변환
                image_buffer = io.BytesIO()
                image.convert("RGB").save(
                    image_buffer,
                    format="JPEG"
                )

                image_bytes = image_buffer.getvalue()

                # AI에게 전달할 분석 요청
                prompt = """
너는 기상학과 구름 분류를 공부한 AI야.

사용자가 업로드한 하늘 사진을 분석하고
세계기상기구(WMO)의 대표적인 10가지 구름 분류를 기준으로
가장 가능성이 높은 구름 종류를 하나 선택해.

분류 후보:
- 권운 (Cirrus)
- 권적운 (Cirrocumulus)
- 권층운 (Cirrostratus)
- 고적운 (Altocumulus)
- 고층운 (Altostratus)
- 층적운 (Stratocumulus)
- 층운 (Stratus)
- 난층운 (Nimbostratus)
- 적운 (Cumulus)
- 적란운 (Cumulonimbus)

사진만으로 정확한 기상 관측을 할 수 없다는 점을 고려하고,
사진에서 실제로 관찰되는 특징을 중심으로 판단해.

반드시 다음 JSON 형식으로만 답해.

{
    "cloud_type": "구름의 한글 이름",
    "english_name": "영어 이름",
    "confidence": 0,
    "features": [
        "사진에서 관찰되는 특징 1",
        "사진에서 관찰되는 특징 2",
        "사진에서 관찰되는 특징 3"
    ],
    "weather": "이 구름과 관련해 일반적으로 알려진 날씨 특징",
    "explanation": "왜 이 구름으로 판단했는지 설명"
}

confidence는 0~100 사이의 숫자로 작성해.
"""

                # Gemini 이미지 분석
                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=[
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": image_bytes
                            }
                        },
                        prompt
                    ]
                )

                result_text = response.text

                # JSON 부분만 추출
                match = re.search(
                    r"\{.*\}",
                    result_text,
                    re.DOTALL
                )

                if not match:
                    st.error(
                        "AI의 분석 결과를 읽지 못했습니다. 다시 시도해 주세요."
                    )
                    st.stop()

                result = json.loads(match.group())

                cloud_type = result.get(
                    "cloud_type",
                    "알 수 없음"
                )

                english_name = result.get(
                    "english_name",
                    ""
                )

                confidence = result.get(
                    "confidence",
                    0
                )

                features = result.get(
                    "features",
                    []
                )

                weather = result.get(
                    "weather",
                    ""
                )

                explanation = result.get(
                    "explanation",
                    ""
                )

                # -----------------------------
                # 결과 출력
                # -----------------------------
                st.success("☁️ 구름 분석이 완료되었습니다!")

                st.markdown("## 🔎 분석 결과")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "구름 종류",
                        cloud_type
                    )

                with col2:
                    st.metric(
                        "AI 판단 신뢰도",
                        f"{confidence}%"
                    )

                if english_name:
                    st.caption(
                        f"영어 명칭: {english_name}"
                    )

                st.divider()

                st.subheader("🔬 사진에서 발견한 특징")

                for feature in features:
                    st.write(f"• {feature}")

                st.subheader("🌦️ 날씨와의 관련성")

                st.write(weather)

                st.subheader("💡 AI의 판단 근거")

                st.write(explanation)

                # 기존 구름 정보와 연결
                if cloud_type in cloud_info:

                    st.divider()

                    st.subheader(
                        f"📚 {cloud_type} 알아보기"
                    )

                    info = cloud_info[cloud_type]

                    st.write(
                        f"**영어:** {info['english']}"
                    )

                    st.write(
                        f"**특징:** {info['description']}"
                    )

                    st.write(
                        f"**날씨:** {info['weather']}"
                    )

            except Exception as e:

                st.error(
                    "❌ 구름 분석 중 오류가 발생했습니다."
                )

                st.write(
                    "다음 사항을 확인해 주세요."
                )

                st.write(
                    "1. Streamlit Secrets에 API 키가 정확하게 입력되어 있는지 확인"
                )

                st.write(
                    "2. 이미지가 JPG, JPEG 또는 PNG 파일인지 확인"
                )

                st.write(
                    "3. 인터넷 연결 상태 확인"
                )

                st.caption(
                    f"오류 정보: {str(e)}"
                )

else:

    st.markdown(
        """
        ### ☁️ 이런 프로젝트예요

        이 프로그램은 **생성형 AI의 이미지 인식 기능**을 이용하여
        하늘 사진에 나타난 구름을 분석합니다.

        **사용 방법**

        ① 하늘 사진 업로드  
        ↓  
        ② 「구름 종류 분석하기」 클릭  
        ↓  
        ③ AI가 구름의 형태와 특징 분석  
        ↓  
        ④ 구름 종류와 날씨 관련 정보 확인

        ### 🔭 분석 가능한 대표적인 구름

        - 권운
        - 권적운
        - 권층운
        - 고적운
        - 고층운
        - 층적운
        - 층운
        - 난층운
        - 적운
        - 적란운
        """
    )

st.divider()

st.caption(
    "⚠️ 이 프로그램은 교육 및 탐구 목적으로 제작되었으며 "
    "실제 기상 관측이나 일기예보를 대신하지 않습니다."
)
