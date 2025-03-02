import google.generativeai as genai
import os
import streamlit as st
from app.audio_processing import generate_and_play_audio, transcribe_user_response
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_questions(resume_text):
    """Extract key skills and generate interview questions using AI."""
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Extract key skills
    skill_prompt = f"Extract key skills from the following resume:\n{resume_text}\nProvide a comma-separated list."
    key_skills = model.generate_content(skill_prompt).text.strip()

    # Generate questions
    question_prompt = f"Generate 10 skill-based interview questions based on this resume with no extra text and each question on one line:\n{resume_text}"
    questions = model.generate_content(question_prompt).text.strip()

    return key_skills, questions

def conduct_interview(question):
    """Ask one question and capture user response."""
    generate_and_play_audio(question, "question_temp")
    response = transcribe_user_response()
    return response
