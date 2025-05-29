def extract_tech_keywords(tech_stack_text):
    # Very basic parser – could be improved with keyword extraction libraries
    return [kw.strip() for kw in tech_stack_text.split(",") if kw.strip()]
