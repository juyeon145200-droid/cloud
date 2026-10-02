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


# API 키
try:
    api_key = st.secrets["GEMINI_API_KEY"]

except Exception:
    st.error("Gemini API 키를 찾을 수 없습니다.")
    st.stop()


client = genai.Client(
    api_key=api_key
)


# main.py에서 업로드한 사진 가져오기
uploaded_file = st.session_state.get(
    "uploaded_image"
)


# 사진이 없는 경우
if uploaded_file is None:

    st.warning(
        "먼저 메인 페이지에서 하늘 사진을 업로드해주세요."
    )

    st.info(
        "왼쪽 메뉴의 'main'을 눌러 사진을 업로드하세요."
    )

    st.stop()


# 사진 표시
image = Image.open(uploaded_file)

st.subheader("📷 분석할 사진")

st.image(
    image,
    use_container_width=True
)


# 분석 버튼
if st.button(
    "☁️ 구름 종류 분석하기",
    use_container_width=True
):

    with st.spinner(
        "AI가 구름을 분석하고 있습니다..."
    ):

        try:

            # 이미지 변환
            image_buffer = io.BytesIO()

            image.convert("RGB").save(
                image_buffer,
                format="JPEG"
            )

            image_bytes = image_buffer.getvalue()


            # AI 분석 요청
            prompt = """
사용자가 업로드한 하늘 사진을 분석해줘.

다음 10가지 구름 중 가장 가능성이 높은
구름 종류 하나를 선택해.

권운, 권적운, 권층운, 고적운, 고층운,
층적운, 층운, 난층운, 적운, 적란운

다음 형식의 JSON으로 답해.

{
    "cloud_type": "구름 종류",
    "english_name": "영어 이름",
    "confidence": 0,
    "features": [
        "사진에서 보이는 특징 1",
        "사진에서 보이는 특징 2",
        "사진에서 보이는 특징 3"
    ],
    "weather": "관련된 날씨 특징",
    "explanation": "판단 근거"
}

confidence는 0~100 사이 숫자로 작성해.
"""


            # Gemini 분석
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


            result_text = response.text


            # JSON 추출
            match = re.search(
                r"\{.*\}",
                result_text,
                re.DOTALL
            )


            if not match:

                st.error(
                    "AI 분석 결과를 읽지 못했습니다."
                )

                st.write(result_text)

                st.stop()


            result = json.loads(
                match.group()
            )


            # 결과
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


            # 결과 출력
            st.success(
                "☁️ 분석이 완료되었습니다!"
            )

            st.divider()

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


            st.subheader(
                "🔬 사진에서 발견한 특징"
            )

            for feature in features:

                st.write(
                    f"• {feature}"
                )


            st.subheader(
                "🌦️ 날씨와의 관련성"
            )

            st.write(weather)


            st.subheader(
                "💡 AI의 판단 근거"
            )

            st.write(explanation)


        except Exception as e:

            st.error(
                "❌ 구름 분석 중 오류가 발생했습니다."
            )

            st.caption(
                f"오류 정보: {str(e)}"
            )
