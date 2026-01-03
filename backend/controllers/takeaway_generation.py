import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key = os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash-lite")

def extract_takeaways(comments:list[str],sentiment:str)->list[str]:
    """
    Generate concise takeaways from the group comments of a giben sentiment.
    """

    if not comments:
        return []
    comments_text = "\n".join(f"- {c}" for c in comments)
    
    prompt = f"""
    Analyze these {sentiment} social media comments:
    {comments_text}

    Task:
    1. Extract 5-8 concise key takeaways.
    2. Provide 2-3 actionable improvements.

    Format the output EXACTLY as follows:
    KEY TAKEAWAYS
    * **Key Point**: Description
    * ...
    
    ACTIONABLE IMPROVEMENTS
    * **Improvement**: Description
    * ...

    Rules:
    - NO preamble or intro/outro.
    - Use '*' for bullet points.
    - Use '**' for bolding key terms.
    - Use neutral, professional language.
    """

    response = model.generate_content(prompt)

    return [
        line.strip()
        for line in response.text.splitlines()
        if line.strip()
    ]