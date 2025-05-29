🤖 TalentScout Hiring Assistant
📌 Project Overview
TalentScout Hiring Assistant is an AI-powered chatbot built with Streamlit that helps collect candidate information and generates personalized technical interview questions based on their tech stack. It integrates with Fireworks AI (Mistral/LLaMA models) and stores data in a GDPR-compliant manner using SQLite.


⚙️ Installation Instructions
1.Clone the repository

git clone https://github.com/yourusername/talentscout-assistant.git
cd talentscout-assistant

2.Create and activate a virtual environment

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3.Install dependencies

pip install -r requirements.txt

4.Set up environment variables

Create a .env file in the root directory:
FIREWORKS_API_KEY=your_fireworks_api_key
MISTRAL_API_URL=https://api.fireworks.ai/inference/v1/chat/completions

5.Run the application

streamlit run app.py




🚀 Usage Guide

1.Fill in the candidate information form.

2.Accept the GDPR data handling notice.

3.Submit your details.

4.The assistant will generate relevant technical interview questions.

5.You may choose to delete your data after completion for compliance.



🛠️ Technical Details

1.Frontend & App Framework: Streamlit

2.LLM Integration: Fireworks AI (Mistral / LLaMA models)

3.Database: SQLite (via Python sqlite3 module)

4.Environment Variables: python-dotenv

5.Prompt Templates: Custom crafted for question generation

6.GDPR Compliance: Explicit consent check and data deletion option




#Project Structure

├── app.py                  # Main Streamlit app
├── prompts.py              # Prompt generation logic
├── utils.py                # Utility functions (e.g. keyword extraction)
├── database.py             # SQLite data handling
├── .env                    # Environment variables
├── requirements.txt
└── README.md



🧠 Prompt Design
Information Gathering: Candidates input their personal and professional details (name, experience, tech stack).

Technical Question Prompt:
A prompt like "Generate 5 technical questions for a candidate with 3 years of experience in React and Node.js" is created dynamically using generate_questions_prompt().

Prompts are concise, context-aware, and optimized for short completions from instruction-tuned models.


🚧 Challenges & Solutions

| Challenge                                       | Solution                                                                  |
| ----------------------------------------------- | ------------------------------------------------------------------------- |
| 🔐 Unauthorized or incorrect Fireworks API URLs | Used officially documented endpoints and ensured bearer token was correct |
| 🧾 GDPR compliance in a stateless Streamlit app | Implemented consent checkbox and manual data deletion via SQLite          |
| ❌ Input validation                              | Added client-side validation for required fields and email formats        |
| 🧠 Prompt hallucination or vague results        | Improved prompt engineering with specific context and constraints         |

