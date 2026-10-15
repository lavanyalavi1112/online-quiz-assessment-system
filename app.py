
import json
import secrets
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="AI Online Quiz System",
    page_icon="📝",
    layout="centered"
)

st.title("📝 AI Online Quiz and Assessment System")
st.write(
    "Choose your domain and difficulty. "
    "AI will generate 10 questions and analyze your performance."
)

DOMAINS = [
    "Python",
    "Java",
    "SQL",
    "HTML and CSS",
    "JavaScript",
    "Aptitude"
]

DIFFICULTIES = ["Easy", "Medium", "Hard", "Mixed"]


def get_api_key():
    # Read the key securely from Streamlit Secrets
    try:
        return st.secrets["GEMINI_API_KEY"]
    except (KeyError, FileNotFoundError):
        return ""


def generate_questions(domain, difficulty):
    api_key = get_api_key()

    if not api_key:
        raise ValueError(
            "Gemini API key is missing. Add GEMINI_API_KEY "
            "in Streamlit Cloud app Secrets."
        )

    client = genai.Client(api_key=api_key)

    # A different random seed prompt for each new test
    unique_id = secrets.token_hex(8)

    prompt = f"""
You are an expert technical assessment question creator.

Create exactly 10 original multiple-choice questions.

Selected domain: {domain}
Difficulty: {difficulty}
Unique test identifier: {unique_id}

Requirements:
1. All questions must belong to the selected domain.
2. Generate a fresh, varied question set for this test.
3. Avoid repeating questions within this set.
4. Questions must test understanding and problem-solving,
   not just memorization.
5. For Easy: basic concepts.
6. For Medium: application and reasoning.
7. For Hard: advanced concepts, debugging, or complex scenarios.
8. For Mixed: include easy, medium, and hard questions.
9. Every question must have exactly 4 answer options.
10. There must be exactly one correct answer per question.
11. The answer must exactly match one of the 4 options.
12. Give a short explanation for the correct answer.
13. Give each question a topic label for improvement analysis.
14. Do not include the answer in the question text.

Return ONLY valid JSON in this exact structure:
{{
  "questions": [
    {{
      "question": "Question text",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": "Option B",
      "explanation": "Why this answer is correct.",
      "topic": "Topic name",
      "difficulty": "Easy"
    }}
  ]
}}
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.9
        )
    )

    data = json.loads(response.text)
    questions = data.get("questions", [])

    # Validate the AI response before showing the test
    if len(questions) != 10:
        raise ValueError(
            "AI did not generate exactly 10 questions. Please try again."
        )

    for question in questions:
        if not all(
            field in question
            for field in [
                "question", "options", "answer",
                "explanation", "topic", "difficulty"
            ]
        ):
            raise ValueError("AI returned an incomplete question.")

        if len(question["options"]) != 4:
            raise ValueError("A question does not have 4 options.")

        if question["answer"] not in question["options"]:
            raise ValueError("An answer does not match its options.")

    return questions


# Initialize application state
defaults = {
    "questions": None,
    "student_name": "",
    "domain": "",
    "difficulty": "",
    "result": None,
    "test_id": 0
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# STEP 1: Student details and test preferences
if st.session_state.questions is None:
    st.subheader("Step 1: Choose Your Test")

    with st.form("student_details"):
        name = st.text_input("Enter your name")

        domain = st.selectbox(
            "Choose your interested domain",
            DOMAINS
        )

        difficulty = st.selectbox(
            "Choose difficulty level",
            DIFFICULTIES
        )

        generate = st.form_submit_button(
            "✨ Generate 10 AI Questions"
        )

    if generate:
        if not name.strip():
            st.warning("Please enter your name.")
        else:
            try:
                with st.spinner(
                    "AI is preparing your questions. Please wait..."
                ):
                    questions = generate_questions(
                        domain, difficulty
                    )

                st.session_state.student_name = name.strip()
                st.session_state.domain = domain
                st.session_state.difficulty = difficulty
                st.session_state.questions = questions
                st.session_state.result = None
                st.session_state.test_id += 1
                st.rerun()

            except Exception as error:
                st.error(
                    "Could not generate the test. "
                    "Check your API key, internet connection, "
                    "API availability, and usage limits."
                )
                st.caption(f"Details: {error}")


# STEP 2: Display the generated test
if st.session_state.questions is not None:
    questions = st.session_state.questions

    st.subheader(
        f"Welcome, {st.session_state.student_name}!"
    )
    st.write(f"**Domain:** {st.session_state.domain}")
    st.write(f"**Difficulty:** {st.session_state.difficulty}")
    st.write("**Total questions:** 10")

    if st.session_state.result is None:
        with st.form(f"test_{st.session_state.test_id}"):
            answers = []

            for i, question in enumerate(questions):
                st.markdown(
                    f"**Question {i + 1}: "
                    f"{question['question']}**"
                )

                selected = st.radio(
                    "Choose one answer:",
                    question["options"],
                    index=None,
                    key=f"answer_{st.session_state.test_id}_{i}"
                )

                answers.append(selected)
                st.divider()

            submit = st.form_submit_button("Submit Test")

        if submit:
            if any(answer is None for answer in answers):
                st.warning("Please answer all 10 questions.")
            else:
                score = sum(
                    answers[i] == questions[i]["answer"]
                    for i in range(len(questions))
                )

                percentage = score * 10

                st.session_state.result = {
                    "answers": answers,
                    "score": score,
                    "percentage": percentage
                }
                st.rerun()


# STEP 3: Score, answer review, and improvement analysis
if (
    st.session_state.questions is not None
    and st.session_state.result is not None
):
    questions = st.session_state.questions
    result = st.session_state.result

    st.divider()
    st.subheader("📊 Your Assessment Results")

    st.write(f"**Student:** {st.session_state.student_name}")
    st.write(f"**Domain:** {st.session_state.domain}")
    st.write(f"**Difficulty:** {st.session_state.difficulty}")

    col1, col2 = st.columns(2)
    col1.metric("Score", f"{result['score']} / 10")
    col2.metric("Percentage", f"{result['percentage']}%")

    if result["percentage"] >= 50:
        st.success("Good work! You passed this assessment.")
    else:
        st.info(
            "Keep practising. Review the topics below "
            "to strengthen your understanding."
        )

    # Analyze topics where answers were incorrect
    weak_topics = {}

    for i, question in enumerate(questions):
        user_answer = result["answers"][i]
        correct_answer = question["answer"]
        topic = question["topic"]

        if user_answer != correct_answer:
            weak_topics[topic] = weak_topics.get(topic, 0) + 1

    st.subheader("🎯 Areas for Improvement")

    if weak_topics:
        st.write(
            "Based on the questions you answered incorrectly, "
            "focus on these topics:"
        )

        for topic, count in sorted(
            weak_topics.items(),
            key=lambda item: item[1],
            reverse=True
        ):
            st.write(f"- **{topic}** — {count} incorrect answer(s)")

        st.info(
            "Practice these topics and review the explanations "
            "below. This analysis is based on your answers."
        )
    else:
        st.success(
            "Excellent! You answered every question correctly. "
            "Try a harder difficulty to challenge yourself."
        )

    st.subheader("📝 Answer Review")

    for i, question in enumerate(questions):
        user_answer = result["answers"][i]
        correct_answer = question["answer"]

        with st.expander(
            f"Question {i + 1}: {question['topic']}"
        ):
            st.write(question["question"])
            st.write(f"**Your answer:** {user_answer}")
            st.write(f"**Correct answer:** {correct_answer}")
            st.write(
                f"**Difficulty:** {question['difficulty']}"
            )
            st.write(
                f"**Explanation:** {question['explanation']}"
            )

            if user_answer == correct_answer:
                st.success("Correct")
            else:
                st.error("Incorrect")

    if st.button("Take Another Test"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

st.caption("AI-powered Online Quiz and Assessment System")
