from google import genai
from google.genai import types

def motivate():

    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Give me a random motivational quote",
        config = types.GenerateContentConfig(
            thinking_config = types.ThinkingConfig(thinking_budget = 0) # disabling thinking
        )
    )

    print(response.text)

motivate()