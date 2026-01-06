import os
import google.generativeai as genai
from dotenv import load_dotenv
import re

load_dotenv()

def get_gemini_model(api_key: str = None):
    """Initialize Gemini model with provided API key or environment variable."""
    key = api_key or os.getenv("GEMINI_API_KEY")
    if not key:
        raise ValueError("Gemini API key is required")
    genai.configure(api_key=key)
    return genai.GenerativeModel("gemini-2.5-flash-lite")



def extract_combined_takeaways(positive_comments: list[str], negative_comments: list[str], api_key: str = None) -> dict:
    """
    Generate takeaways for both positive and negative comments in a single call.
    """
    if not positive_comments and not negative_comments:
        return {"positive": [], "negative": []}

    # Get the Gemini model with the provided API key
    model = get_gemini_model(api_key)

    # Limit comment count to maintain focus and speed
    pos_text = "\n".join(f"- {c}" for c in positive_comments[:40])
    neg_text = "\n".join(f"- {c}" for c in negative_comments[:40])

    prompt = f"""
    Analyze these social media comments and provide insights.

    POSITIVE COMMENTS:
    {pos_text if pos_text else "None"}

    NEGATIVE COMMENTS:
    {neg_text if neg_text else "None"}

    Task:
    1. For POSITIVE comments, extract 5-8 key takeaways and 2-3 actionable improvements.
    2. For NEGATIVE comments, extract 5-8 key takeaways and 2-3 actionable improvements.

    Format the output EXACTLY as follows:
    [POSITIVE_START]
    KEY TAKEAWAYS
    * **Key Point**: Description
    ...
    ACTIONABLE IMPROVEMENTS
    * **Improvement**: Description
    ...
    [POSITIVE_END]

    [NEGATIVE_START]
    KEY TAKEAWAYS
    * **Key Point**: Description
    ...
    ACTIONABLE IMPROVEMENTS
    * **Improvement**: Description
    ...
    [NEGATIVE_END]

    Rules:
    - NO preamble or intro/outro.
    - Use neutral, professional language.
    """

    response = model.generate_content(prompt)
    text = response.text

    def extract_section(start_tag, end_tag):
        pattern = f"{re.escape(start_tag)}(.*?){re.escape(end_tag)}"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            content = match.group(1).strip()
            return [line.strip() for line in content.splitlines() if line.strip()]
        return []

    return {
        "positive": extract_section("[POSITIVE_START]", "[POSITIVE_END]"),
        "negative": extract_section("[NEGATIVE_START]", "[NEGATIVE_END]")
    }

