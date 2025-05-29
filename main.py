import streamlit as st
from prompts import generate_questions_prompt
from utils import extract_tech_keywords
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env

MISTRAL_API_KEY = os.getenv("FIREWORKS_API_KEY")
MISTRAL_API_URL = os.getenv("MISTRAL_API_URL", "https://api.fireworks.ai/inference/v1/chat/completions")

st.set_page_config(page_title="TalentScout Hiring Assistant")
st.title("🤖 TalentScout Hiring Assistant")
st.markdown("Hello! I'm here to help you with your application. Let's get started!")

# Session state initialization
if 'stage' not in st.session_state:
    st.session_state.stage = 'info_gathering'
    st.session_state.candidate_info = {}

def ask_gpt(prompt):
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model":"accounts/fireworks/models/llama-v3p1-8b-instruct",  # Recommended working model
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(MISTRAL_API_URL, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data['choices'][0]['message']['content']

def gather_candidate_info():
    with st.form("Candidate Info"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        exp = st.number_input("Years of Experience", 0, 50, 1)
        position = st.text_input("Desired Position(s)")
        location = st.text_input("Current Location")
        tech_stack = st.text_area("Tech Stack (Languages, Frameworks, Tools)")
        submitted = st.form_submit_button("Submit")

        if submitted:
            errors = []
            if not name.strip():
                errors.append("Name is required.")
            if not email.strip() or "@" not in email:
                errors.append("Valid email is required.")
            if not phone.strip().isdigit() or len(phone.strip()) < 10:
                errors.append("Valid phone number is required (at least 10 digits).")
            if not position.strip():
                errors.append("Position is required.")
            if not location.strip():
                errors.append("Location is required.")
            if not tech_stack.strip():
                errors.append("Tech stack is required.")

            if errors:
                for err in errors:
                    st.error(err)
            else:
                st.session_state.candidate_info = {
                    "name": name, "email": email, "phone": phone, "exp": exp,
                    "position": position, "location": location, "tech_stack": tech_stack
                }
                st.session_state.stage = 'generate_questions'


if st.session_state.stage == 'info_gathering':
    gather_candidate_info()

elif st.session_state.stage == 'generate_questions':
    st.subheader("Thanks! Generating technical questions based on your tech stack...")
    tech_stack = extract_tech_keywords(st.session_state.candidate_info["tech_stack"])
    prompt = generate_questions_prompt(tech_stack)
    try:
        questions = ask_gpt(prompt)
        st.write(questions)
    except Exception as e:
        st.error(f"Error generating questions: {e}")
    st.session_state.stage = 'end'

elif st.session_state.stage == 'end':
    st.success("Thanks for sharing your details! Our team will get back to you soon.")
