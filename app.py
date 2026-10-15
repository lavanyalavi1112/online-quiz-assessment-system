
import streamlit as st

st.set_page_config(
    page_title="Online Quiz System",
    page_icon="📝",
    layout="centered"
)

st.title("📝 Online Quiz and Assessment System")
st.write("Choose your interested domain and test your knowledge!")

# Questions for each domain
quiz_data = {
    "Python": [
        {
            "question": "Which symbol is used for comments in Python?",
            "options": ["//", "#", "/*", "<!--"],
            "answer": "#"
        },
        {
            "question": "Which keyword is used to define a function?",
            "options": ["function", "def", "fun", "define"],
            "answer": "def"
        },
        {
            "question": "Which data type stores whole numbers?",
            "options": ["str", "int", "list", "bool"],
            "answer": "int"
        },
        {
            "question": "Which function displays output?",
            "options": ["input()", "print()", "show()", "display()"],
            "answer": "print()"
        },
        {
            "question": "Which collection uses key-value pairs?",
            "options": ["List", "Tuple", "Dictionary", "Set"],
            "answer": "Dictionary"
        }
    ],

    "Java": [
        {
            "question": "Which keyword creates a class in Java?",
            "options": ["class", "define", "struct", "create"],
            "answer": "class"
        },
        {
            "question": "Which method is the entry point of a Java program?",
            "options": ["start()", "run()", "main()", "execute()"],
            "answer": "main()"
        },
        {
            "question": "Which type stores whole numbers?",
            "options": ["String", "int", "boolean", "char"],
            "answer": "int"
        },
        {
            "question": "Which keyword creates an object?",
            "options": ["class", "new", "this", "void"],
            "answer": "new"
        },
        {
            "question": "Which statement prints output in Java?",
            "options": [
                "System.out.println()",
                "Console.read()",
                "print.line()",
                "echo()"
            ],
            "answer": "System.out.println()"
        }
    ],

    "SQL": [
        {
            "question": "Which command retrieves data from a table?",
            "options": ["INSERT", "SELECT", "DELETE", "UPDATE"],
            "answer": "SELECT"
        },
        {
            "question": "Which key uniquely identifies a row?",
            "options": ["Foreign key", "Primary key", "Duplicate key", "Sort key"],
            "answer": "Primary key"
        },
        {
            "question": "Which command adds a new row?",
            "options": ["INSERT", "ALTER", "DROP", "SELECT"],
            "answer": "INSERT"
        },
        {
            "question": "Which clause filters rows?",
            "options": ["ORDER BY", "WHERE", "GROUP BY", "JOIN"],
            "answer": "WHERE"
        },
        {
            "question": "Which command changes existing data?",
            "options": ["UPDATE", "CREATE", "SELECT", "DROP"],
            "answer": "UPDATE"
        }
    ],

    "HTML and CSS": [
        {
            "question": "What does HTML stand for?",
            "options": [
                "Hyper Text Markup Language",
                "High Text Machine Language",
                "Hyper Transfer Main Language",
                "Home Tool Markup Language"
            ],
            "answer": "Hyper Text Markup Language"
        },
        {
            "question": "Which HTML tag creates a hyperlink?",
            "options": ["<p>", "<a>", "<h1>", "<img>"],
            "answer": "<a>"
        },
        {
            "question": "Which language styles a webpage?",
            "options": ["SQL", "CSS", "Python", "Java"],
            "answer": "CSS"
        },
        {
            "question": "Which CSS property changes text color?",
            "options": ["margin", "font-size", "color", "padding"],
            "answer": "color"
        },
        {
            "question": "Which HTML tag displays an image?",
            "options": ["<image>", "<pic>", "<img>", "<src>"],
            "answer": "<img>"
        }
    ],

    "JavaScript": [
        {
            "question": "Which keyword declares a variable?",
            "options": ["var", "define", "int", "variable"],
            "answer": "var"
        },
        {
            "question": "Which symbol is used for strict equality?",
            "options": ["=", "==", "===", "!="],
            "answer": "==="
        },
        {
            "question": "Which method displays a message in the console?",
            "options": [
                "console.log()",
                "print()",
                "System.out.println()",
                "show.console()"
            ],
            "answer": "console.log()"
        },
        {
            "question": "Which keyword declares a block-scoped variable?",
            "options": ["let", "echo", "integer", "define"],
            "answer": "let"
        },
        {
            "question": "Which language adds interactivity to webpages?",
            "options": ["SQL", "HTML", "JavaScript", "CSS"],
            "answer": "JavaScript"
        }
    ],

    "Aptitude": [
        {
            "question": "What is 15 + 25?",
            "options": ["30", "35", "40", "45"],
            "answer": "40"
        },
        {
            "question": "What is 12 × 5?",
            "options": ["50", "55", "60", "65"],
            "answer": "60"
        },
        {
            "question": "Find the next number: 2, 4, 6, 8, ?",
            "options": ["9", "10", "11", "12"],
            "answer": "10"
        },
        {
            "question": "What is half of 100?",
            "options": ["25", "40", "50", "75"],
            "answer": "50"
        },
        {
            "question": "If one pen costs ₹10, what do 3 pens cost?",
            "options": ["₹20", "₹25", "₹30", "₹40"],
            "answer": "₹30"
        }
    ]
}

# Initialize session state
if "started" not in st.session_state:
    st.session_state.started = False

if "result" not in st.session_state:
    st.session_state.result = None

if "attempt" not in st.session_state:
    st.session_state.attempt = 0

# Step 1: Student details and domain selection
if not st.session_state.started:
    st.subheader("Step 1: Student Details")

    with st.form("student_form"):
        student_name = st.text_input("Enter your name")

        domain = st.selectbox(
            "Select your interested test domain",
            list(quiz_data.keys())
        )

        start = st.form_submit_button("Start Test")

    if start:
        if not student_name.strip():
            st.warning("Please enter your name.")
        else:
            st.session_state.student_name = student_name.strip()
            st.session_state.domain = domain
            st.session_state.started = True
            st.session_state.result = None
            st.session_state.attempt += 1
            st.rerun()

# Step 2: Display questions for the selected domain
if st.session_state.started:
    name = st.session_state.student_name
    domain = st.session_state.domain
    questions = quiz_data[domain]

    st.subheader(f"Welcome, {name}!")
    st.write(f"**Selected Domain:** {domain}")
    st.write(f"**Total Questions:** {len(questions)}")
    st.divider()

    # Show the test only until it is submitted
    if st.session_state.result is None:
        with st.form(f"quiz_form_{st.session_state.attempt}"):
            answers = []

            for i, question in enumerate(questions):
                selected = st.radio(
                    f"Q{i + 1}. {question['question']}",
                    question["options"],
                    index=None,
                    key=f"answer_{st.session_state.attempt}_{i}"
                )
                answers.append(selected)

            submitted = st.form_submit_button("Submit Test")

        if submitted:
            if any(answer is None for answer in answers):
                st.warning("Please answer all questions before submitting.")
            else:
                score = sum(
                    answers[i] == questions[i]["answer"]
                    for i in range(len(questions))
                )

                percentage = score / len(questions) * 100

                st.session_state.result = {
                    "answers": answers,
                    "score": score,
                    "percentage": percentage
                }
                st.rerun()

    # Step 3: Display results
    if st.session_state.result is not None:
        result = st.session_state.result

        st.divider()
        st.subheader("📊 Test Results")

        st.write(f"**Student:** {name}")
        st.write(f"**Domain:** {domain}")

        st.metric(
            "Score",
            f"{result['score']} / {len(questions)}"
        )
        st.metric(
            "Percentage",
            f"{result['percentage']:.0f}%"
        )

        if result["percentage"] >= 50:
            st.success("Congratulations! You passed the test.")
        else:
            st.info("Keep practising. You can improve your score!")

        st.subheader("Answer Review")

        for i, question in enumerate(questions):
            st.write(f"**Q{i + 1}. {question['question']}**")
            st.write(f"Your answer: {result['answers'][i]}")
            st.write(f"Correct answer: {question['answer']}")

            if result["answers"][i] == question["answer"]:
                st.write("✅ Correct")
            else:
                st.write("❌ Incorrect")

        if st.button("Take Another Test"):
            st.session_state.started = False
            st.session_state.result = None
            st.session_state.attempt += 1
            st.rerun()

st.caption("Online Quiz and Assessment System")
