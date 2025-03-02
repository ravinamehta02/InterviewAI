import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))

from app.resume_parser import extract_text_from_pdf
from app.interview import generate_questions, conduct_interview
from app.database import init_db, save_candidate_to_database, save_interview_to_database

# Initialize database
init_db()

st.title("📝 AI-Powered Resume Interview Assistant")

# User input for name
name = st.text_input("Enter your name:")

# File uploader for resume
uploaded_file = st.file_uploader("Upload your resume (PDF format)", type="pdf")

if uploaded_file and name:
    resume_text = extract_text_from_pdf(uploaded_file)
    st.subheader("Extracted Resume Text:")
    st.text(resume_text)

    # Generate interview questions
    key_skills, questions = generate_questions(resume_text)
    st.subheader("Extracted Key Skills:")
    st.text(key_skills)

    st.subheader("Generated Interview Questions:")
    st.text(questions)

    # Save candidate details to the database
    candidate_id = save_candidate_to_database(name, key_skills)

    if st.button("Start Interview"):
        responses = []

        # Create UI placeholders
        question_placeholder = st.empty()
        response_placeholder = st.empty()

        # Conduct the interview, updating UI in real-time
        for i, question in enumerate(questions.split("\n")):
            question_placeholder.markdown(f"### **Question {i+1}:** {question}")
            response = conduct_interview(question)  # Ask one question at a time
            responses.append(response)

            response_placeholder.markdown(f"**Your Answer:** {response}")

        # Save interview results to the database
        save_interview_to_database(candidate_id, questions.split("\n"), responses)

        # Display final interview summary
        st.subheader("Interview Summary")
        for i, (q, r) in enumerate(zip(questions.split("\n"), responses)):
            st.write(f"**Question {i+1}:** {q}")
            st.write(f"**Your Answer:** {r}")

        # Save results to a text file
        output_filename = f"{name}_interview_results.txt"
        with open(output_filename, "w", encoding="utf-8") as file:
            file.write(f"Candidate Name: {name}\n")
            file.write(f"Extracted Skills: {key_skills}\n\n")
            for i, (q, r) in enumerate(zip(questions.split("\n"), responses)):
                file.write(f"Question {i+1}: {q}\n")
                file.write(f"Answer {i+1}: {r}\n\n")

        # Provide download link
        with open(output_filename, "rb") as file:
            st.download_button("Download Interview Results", file, file_name=output_filename, mime="text/plain")

        st.success("Interview completed and results saved!")

else:
    st.warning("Please enter your name and upload a resume.")
