import streamlit as st
from google import genai
from PIL import Image
import io
import json
import re


# ==========================================
# 기본 설정
# ==========================================

st.set_page_config(
    page_title="하늘 사진으로 구름 종류 알아보기",
    page_icon="☁️",
    layout="centered"
)

st.title("☁️ 하늘 사진으로 구름 종류 알아보기")

st.write(
    "하늘 사진을 업로드하면 생성형 AI가 사진 속 구름의 종류와 특징을 분석해 줍니다."
)


# ==========================================
# API 키 불러오기
# ==========================================

try:
    api_key = st.secrets["GEMINI_API_KEY"]

except Exception:
    st.error("⚠️ Gemini API 키를 찾을 수 없습니다.")

    st.info(
        """
        Streamlit Cloud의 Secrets에 다음과 같이 입력했는지 확인하세요.

        GEMINI_API_KEY = "발급받은_API_키"
        """
    )

    st.stop()


# Gemini 연결
client = genai.Client(api_key=api_key)


# ==========================================
# 구름 종류별 기본 정보
# ==========================================

cloud_info = {

    "권운": {
        "english": "Cirrus",
        "description": "높은 고도에서 나타나는 가늘고 실처럼 보이는 구름입니다.",
        "weather": "날씨 변화가 나타나기 전에 관찰되는 경우가 있습니다."
    },

    "권적운": {
        "english": "Cirrocumulus",
        "description": "작은 구름 알갱이가 물결처럼 배열되어 있는 높은 고도의 구름입니다.",
        "weather": "높은 고도의 대기 상태를 파악하는 데 참고할 수 있습니다."
    },

    "권층운": {
        "english": "Cirrostratus",
        "description": "하늘을 얇게 덮는 높은 고도의 구름입니다.",
        "weather": "전선이 접근할 때 나타나는 경우가 있습니다."
    },

    "고적운": {
        "english": "Altocumulus",
        "description": "중간 높이에서 작은 덩어리들이 모여 있는 형태의 구름입니다.",
        "weather": "대기의 불안정 정도를 판단하는 데 참고할 수 있습니다."
    },

    "고층운": {
        "english": "Altostratus",
        "description": "중간 고도에서 넓은 영역을 회색빛으로 덮는 구름입니다.",
        "weather": "비나 눈이 내리기 전에 나타나는 경우가 있습니다."
    },

    "층적운": {
        "english": "Stratocumulus",
        "description": "낮은 고도에서 넓게 퍼진 덩어리 형태의 구름입니다.",
        "weather": "흐린 날씨나 약한 강수와 관련될 수 있습니다."
    },

    "층운": {
        "english": "Stratus",
        "description": "낮은 하늘을 안개처럼 넓게 덮는 층 형태의 구름입니다.",
        "weather": "흐린 날씨와 관련이 있습니다."
    },

    "난층운": {
        "english": "Nimbostratus",
        "description": "두껍고 어두운 층 형태의 구름입니다.",
        "weather": "넓은 지역에 지속적인 비나 눈이 내릴 때 나타날 수 있습니다."
    },

    "적운": {
        "english": "Cumulus",
        "description": "하얗고 둥근 솜털처럼 보이는 구름입니다.",
        "weather": "작은 적운은 맑은 날씨에서 흔하게 관찰됩니다."
    },

    "적란운": {
        "english": "Cumulonimbus",
        "description": "수직으로 매우 크게 발달하는 구름입니다.",
        "weather": "강한 소나기나 천둥·번개와 관련될 수 있습니다."
    }
}


# ==========================================
# 사진 업로드
# ==========================================

uploaded_file = st.file_uploader(
    "📸 하늘 사진을 업로드하세요",
    type=["jpg", "jpeg", "png"]
)


# ==========================================
# 사진이 업로드되었을 때
# ==========================================

if uploaded_file is not None:

    # 이미지 열기
    image = Image.open(uploaded_file)

    st.subheader("📷 업로드한 사진")

    st.image(
        image,
        caption="분석할 하늘 사진",
        use_container_width=True
    )

    st.write("")


    # ======================================
    # 분석 버튼
    # ======================================

    if st.button(
        "☁️ 구름 종류 분석하기",
        use_container_width=True
    ):

        with st.spinner(
            "☁️ AI가 구름의 모양과 특징을 분석하고 있습니다..."
        ):

            try:

                # ----------------------------------
                # 이미지를 JPEG 형식으로 변환
                # ----------------------------------

                image_buffer = io.BytesIO()

                image.convert("RGB").save(
                    image_buffer,
                    format="JPEG"
                )

                image_bytes = image_buffer.getvalue()


                # ----------------------------------
                # AI에게 전달할 질문
                # ----------------------------------

                prompt = """
너는 기상학과 구름 분류를 공부한 AI야.

사용자가 업로드한 하늘 사진을 분석하고
대표적인 10가지 구름 분류를 기준으로
가장 가능성이 높은 구름 종류를 하나 선택해.

분류 후보는 다음과 같아.

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

사진에서 실제로 관찰되는 특징을 중심으로 판단해.

사진만으로 실제 기상 상황을 정확하게 판단할 수는 없으므로
확실하지 않은 경우에는 낮은 신뢰도를 사용해.

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

confidence는 0부터 100 사이의 숫자로 작성해.
"""


                # ----------------------------------
                # Gemini AI 이미지 분석
                # ----------------------------------
                # ⭐ 수정된 부분
                # gemini-3.5-flash-lite 사용
                # ----------------------------------

                response = client.models.generate_content(

                    model="gemini-3.5-flash-lite",

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


                # ----------------------------------
                # AI 응답 가져오기
                # ----------------------------------

                result_text = response.text


                # JSON 부분 찾기
                match = re.search(
                    r"\{.*\}",
                    result_text,
                    re.DOTALL
                )


                if not match:

                    st.error(
                        "⚠️ AI의 분석 결과를 읽지 못했습니다."
                    )

                    st.write(
                        "AI 응답:"
                    )

                    st.write(result_text)

                    st.stop()


                # JSON으로 변환
                result = json.loads(
                    match.group()
                )


                # ----------------------------------
                # 분석 결과 가져오기
                # ----------------------------------

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


                # ==================================
                # 결과 표시
                # ==================================

                st.success(
                    "☁️ 구름 분석이 완료되었습니다!"
                )

                st.markdown(
                    "## 🔎 분석 결과"
                )


                # 구름 종류 / 신뢰도
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


                # 영어 이름
                if english_name:

                    st.caption(
                        f"영어 명칭: {english_name}"
                    )


                st.divider()


                # ==================================
                # 사진 특징
                # ==================================

                st.subheader(
                    "🔬 사진에서 발견한 특징"
                )


                if isinstance(features, list):

                    for feature in features:

                        st.write(
                            f"• {feature}"
                        )

                else:

                    st.write(features)


                # ==================================
                # 날씨 관련 정보
                # ==================================

                st.subheader(
                    "🌦️ 날씨와의 관련성"
                )

                st.write(weather)


                # ==================================
                # AI 판단 근거
                # ==================================

                st.subheader(
                    "💡 AI의 판단 근거"
                )

                st.write(explanation)


                # ==================================
                # 구름 종류 추가 정보
                # ==================================

                if cloud_type in cloud_info:

                    st.divider()

                    st.subheader(
                        f"📚 {cloud_type} 알아보기"
                    )


                    info = cloud_info[
                        cloud_type
                    ]


                    st.write(
                        f"**영어:** {info['english']}"
                    )

                    st.write(
                        f"**특징:** {info['description']}"
                    )

                    st.write(
                        f"**날씨:** {info['weather']}"
                    )


            # ======================================
            # 오류 처리
            # ======================================

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

                st.write(
                    "4. Gemini API를 사용할 수 있는 상태인지 확인"
                )

                st.caption(
                    f"오류 정보: {str(e)}"
                )


# ==========================================
# 사진을 아직 올리지 않았을 때
# ==========================================

else:

    st.markdown(
        """
        ### ☁️ 이런 프로젝트예요

        이 프로그램은 생성형 AI의 이미지 인식 기능을 이용하여
        하늘 사진에 나타난 구름을 분석합니다.

        ### 📌 사용 방법

        **① 하늘 사진 업로드**

        ↓

        **② 「구름 종류 분석하기」 클릭**

        ↓

        **③ AI가 구름의 형태와 특징 분석**

        ↓

        **④ 구름 종류와 날씨 관련 정보 확인**

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


# ==========================================
# 안내 문구
# ==========================================

st.divider()

st.caption(
    "⚠️ 이 프로그램은 교육 및 탐구 목적으로 제작되었으며 "
    "실제 기상 관측이나 일기예보를 대신하지 않습니다."
)
