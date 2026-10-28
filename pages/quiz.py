
import streamlit as st

st.set_page_config(
    page_title="구름 종류 맞히기 퀴즈",
    page_icon="☁️"
)

st.title("☁️ 구름 종류 맞히기 퀴즈")
st.write("구름의 특징을 읽고 어떤 구름인지 맞혀 보세요!")
st.divider()

# 퀴즈 문제와 정답
questions = [
    {
        "question": "1. 솜처럼 하얗고 뭉게뭉게 피어오르는 구름은?",
        "options": ["권운", "적운", "층운", "권층운"],
        "answer": "적운",
        "explanation": "적운은 솜처럼 뭉친 모양이 특징이며, 대기가 불안정하면 크게 발달할 수 있습니다."
    },
    {
        "question": "2. 높은 하늘에 나타나며 깃털처럼 가늘고 흩어진 구름은?",
        "options": ["층운", "난층운", "적운", "권운"],
        "answer": "권운",
        "explanation": "권운은 높은 하늘에 나타나는 가늘고 섬유 같은 구름으로, 주로 얼음 결정으로 이루어집니다."
    },
    {
        "question": "3. 하늘을 넓게 덮으며 안개처럼 층을 이루는 구름은?",
        "options": ["층운", "적운", "권운", "적란운"],
        "answer": "층운",
        "explanation": "층운은 낮은 하늘에 넓고 균일한 층을 이루며 나타나는 구름입니다."
    },
    {
        "question": "4. 강한 상승 기류로 크게 발달하고 천둥과 번개를 동반할 수 있는 구름은?",
        "options": ["권운", "층운", "적란운", "권층운"],
        "answer": "적란운",
        "explanation": "적란운은 수직으로 크게 발달하며 소나기, 천둥, 번개 등을 동반할 수 있습니다."
    },
    {
        "question": "5. 하늘을 두껍게 덮으며 오랜 시간 비나 눈을 내리게 할 수 있는 구름은?",
        "options": ["권운", "난층운", "적운", "권층운"],
        "answer": "난층운",
        "explanation": "난층운은 넓은 지역에 걸쳐 비나 눈을 지속적으로 내리게 할 수 있는 구름입니다."
    }
]

# 퀴즈 시작
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False

if not st.session_state.quiz_submitted:

    with st.form("cloud_quiz_form"):
        answers = {}

        for i, q in enumerate(questions):
            answers[i] = st.radio(
                q["question"],
                q["options"],
                index=None,
                key=f"cloud_quiz_{i}"
            )

        submitted = st.form_submit_button("정답 확인")

    if submitted:
        if any(answer is None for answer in answers.values()):
            st.warning("모든 문제에 답을 선택해 주세요!")
        else:
            st.session_state.quiz_answers = answers
            st.session_state.quiz_submitted = True
            st.rerun()

else:
    answers = st.session_state.quiz_answers
    score = 0

    for i, q in enumerate(questions):
        user_answer = answers[i]

        if user_answer == q["answer"]:
            score += 1

    st.subheader("📊 퀴즈 결과")
    st.metric("최종 점수", f"{score} / {len(questions)}")

    if score == len(questions):
        st.success("완벽해요! 구름 박사네요! ☁️")
    elif score >= 3:
        st.success("잘했어요! 조금만 더 공부하면 완벽하겠어요.")
    else:
        st.info("괜찮아요! 해설을 읽으며 구름의 특징을 익혀 보세요.")

    st.divider()
    st.subheader("📝 정답 및 해설")

    for i, q in enumerate(questions):
        user_answer = answers[i]

        st.markdown(f"**{q['question']}**")

        if user_answer == q["answer"]:
            st.success(f"정답: {q['answer']}")
        else:
            st.error(
                f"내 답: {user_answer} / 정답: {q['answer']}"
            )

        st.write(q["explanation"])
        st.divider()

    if st.button("다시 풀기", use_container_width=True):
        for i in range(len(questions)):
            st.session_state.pop(f"cloud_quiz_{i}", None)

        st.session_state.quiz_submitted = False
        st.session_state.pop("quiz_answers", None)
        st.rerun()
