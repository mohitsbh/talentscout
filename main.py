import streamlit as st
from prompts import generate_questions_prompt
from utils import extract_tech_keywords
import requests
import os
import sqlite3
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()
MISTRAL_API_KEY = os.getenv("FIREWORKS_API_KEY")
MISTRAL_API_URL = os.getenv("MISTRAL_API_URL", "https://api.fireworks.ai/inference/v1/chat/completions")

# Initialize DB
def init_db():
    conn = sqlite3.connect("candidates.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, email TEXT, phone TEXT,
            exp INTEGER, position TEXT, location TEXT, tech_stack TEXT,
            consent TEXT, timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Save data
def save_candidate_data(data):
    conn = sqlite3.connect("candidates.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO candidates (name, email, phone, exp, position, location, tech_stack, consent, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data["name"], data["email"], data["phone"], data["exp"],
        data["position"], data["location"], data["tech_stack"],
        data["consent"], data["timestamp"]
    ))
    conn.commit()
    conn.close()

# Delete data
def delete_user_data(email):
    conn = sqlite3.connect("candidates.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM candidates WHERE email = ?", (email,))
    conn.commit()
    conn.close()

# Call Mistral API
def ask_gpt(prompt):
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "accounts/fireworks/models/llama-v3p1-8b-instruct",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(MISTRAL_API_URL, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']

# Streamlit app setup
st.set_page_config(page_title="TalentScout Hiring Assistant")
st.title("🤖 TalentScout Hiring Assistant")

with st.expander("🔐 GDPR Privacy Notice"):
    st.markdown("""
    We collect your data to assess your fit for technical roles:
    - **Retention**: Max 6 months.
    - **Rights**: Access, correction, or deletion upon request.
    - **Contact**: gdpr@talentscout.com
    """)

# Stage handling
if 'stage' not in st.session_state:
    st.session_state.stage = 'info_gathering'
    st.session_state.candidate_info = {}

# Form
if st.session_state.stage == 'info_gathering':
    with st.form("Candidate Info"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        exp = st.number_input("Years of Experience", 0, 50, 1)
        position = st.text_input("Desired Position(s)")
        location = st.text_input("Current Location")
        tech_stack = st.text_area("Tech Stack (Languages, Frameworks, Tools)")
        consent = st.checkbox("I consent to the processing of my personal data in accordance with the GDPR.", value=False)
        submitted = st.form_submit_button("Submit")

        if submitted:
            if not consent:
                st.warning("You must agree to the GDPR policy to proceed.")
            elif not all([name, email, phone, position]):
                st.warning("Please fill in all required fields.")
            else:
                candidate = {
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "exp": exp,
                    "position": position,
                    "location": location,
                    "tech_stack": tech_stack,
                    "consent": "yes",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state.candidate_info = candidate
                save_candidate_data(candidate)
                st.session_state.stage = 'generate_questions'

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

# GDPR data deletion section
with st.expander("🧹 Request Data Deletion"):
    delete_email = st.text_input("Enter your email to delete your data")
    if st.button("Delete My Data"):
        delete_user_data(delete_email)
        st.success("Your data has been successfully deleted.")

# Ensure DB is ready
init_db()