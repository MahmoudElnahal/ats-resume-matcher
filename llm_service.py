import openai
from config import OPENAI_API_KEY

# إنشاء عميل OpenAI الجديد
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def call_gpt(prompt: str, model: str = "gpt-4o") -> str:
    """
    استدعاء GPT-4 باستخدام النسخة الحديثة من مكتبة openai
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful resume analysis assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ GPT Error: {e}")
        return ""
