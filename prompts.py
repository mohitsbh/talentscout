def generate_questions_prompt(tech_keywords):
    tech_list = ', '.join(tech_keywords)
    return f"Generate 5 technical interview questions for a candidate familiar with: {tech_list}. Make them relevant to job interviews."
