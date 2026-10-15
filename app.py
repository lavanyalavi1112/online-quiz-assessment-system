import streamlit as st

st.set_page_config(
    page_title="Online Quiz System",
    page_icon="📝",
    layout="centered"
)

st.title("📝 Online Quiz and Assessment System")
st.write("Test your knowledge and check your results!")

# Questions and correct answers
questions = [
    {
        "question": "1. Which language are we using for this project?",
        "options": ["Java", "Python", "C++", "HTML"],
        "answer": "Python"
    },
    {
        "question": "2. Which keyword is used to check a condition in Python?",
        "options": ["for", "while", "if", "def"],
        "answer": "if"
    },
    {
        "question": "3. Which data type stores True or False?",
        "options": ["int", "bool", "str", "float"],
        "answer": "bool"
    },
    {
        "question": "4. Which function displays output in Python?",
        "options": ["input()", "print()", "type()", "range()"],
        "answer": "print()"
    },
    {
        "question": "5. Which language is commonly used to style web pages?",
        "options": ["SQL", "Python", "CSS", "Java"],
        "answer": "CSS"
    },
    {
        "question": "6. Which SQL command retrieves data from a table?",
        "options": ["SELECT", "DELETE", "DROP", "INSERT"],
        "answer": "SELECT"
    },
    {
        "question": "7. Which symbol starts a comment in Python?",
        "options": ["//", "<!--", "#", "/*"],
        "answer": "#"
    },
    {
        "question": "8. Which collection stores multiple items in Python?",
        "options": ["list", "if", "print", "input"],
        "answer": "list"
    },
    {
        "question": "9. Which loop is useful for iterating over a list?",
        "options": ["if", "for", "def", "class"],
        "answer": "for"
    },
    {
        "question": "10. What does HTML mainly define?",
        "options": [
            "Web page structure",
            "Database queries",
            "Computer hardware",
            "Operating system settings"
        ],
        "answer": "Web page structure"
    }
]

# Keep the quiz result during the current session
if "result" not in st.session_state:
    st.session_state.result = None

if st.session_state.result is None:

    with st.form("quiz_form"):
        name = st.text_input("Enter your name")

        st.subheader("Answer all 10 questions")

        selected_answers = []

        for i, q in enumerate(questions):
            selected = st.radio(
                q["question"],
                q["options"],
                index=None,
                key=f"question_{i}"
            )
            selected_answers.append(selected)

        submitted = st.form_submit_button("Submit Quiz")

    if submitted:
        if not name.strip():
            st.error("Please enter your name.")
        elif any(answer is None for answer in selected_answers):
            st.warning("Please answer every question before submitting.")
        else:
            score = sum(
                selected_answers[i] == q["answer"]
                for i, q in enumerate(questions)
            )

            percentage = (score / len(questions)) * 100

            st.session_state.result = {
                "name": name.strip(),
                "answers": selected_answers,
                "score": score,
                "percentage": percentage
            }

            st.rerun()

else:
    result = st.session_state.result

    st.success("Quiz submitted successfully!")

    st.subheader("Your Results")
    st.write("**Student Name:**", result["name"])
    st.metric("Total Score", f'{result["score"]} / {len(questions)}')
    st.metric("Percentage", f'{result["percentage"]:.0f}%')

    if result["percentage"] >= 50:
        st.success("Result: PASS")
    else:
        st.error("Result: FAIL")

    st.subheader("Answer Review")

    for i, q in enumerate(questions):
        chosen = result["answers"][i]
        correct = q["answer"]

        st.write(q["question"])
        st.write("Your answer:", chosen)
        st.write("Correct answer:", correct)

        if chosen == correct:
            st.success("Correct answer")
        else:
            st.error("Incorrect answer")

        st.divider()

    if st.button("Restart Quiz"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
