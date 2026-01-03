import os
import google.generativeai as genai

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
    You're analysing {sentiment} social  media comments.

    Below are {sentiment} comments from the user on the post:
    {comments_text}

    Task:
    - Extract 5 to 10 consice key takeaways.
    - Use simple, neutral language.
    - Avoid repetition
    - 
    - You can also suggest further imporvement to be applied to be better.
    - Do not mention individual users.
    """

    response = model.generate_content(prompt)

    return [
        line.strip("-. ").strip()
        for line in response.text.splitlines()
        if line.strip()
    ]