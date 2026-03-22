import os


def generate_memo(summary_text: str) -> str:
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        return "⚠️ Missing OpenRouter API key"

try:
    from openai import OpenAI

    client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
        )

        response = client.chat.completions.create(
            model="openrouter/free",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a senior equity research analyst. "
                        "Write a professional memo with these sections: "
                        "Executive Summary, Growth, Profitability, Risk, "
                        "Valuation View, Recommendation."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Analyze this company data:\n\n{summary_text}",
                },
            ],
            temperature=0.3,
        )

        return response.choices[0].message.content or "⚠️ Empty AI response"

    except Exception as e:
        return f"⚠️ OpenRouter AI Error: {e}"