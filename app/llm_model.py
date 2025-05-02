import requests

token = "Bearer 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"

def get_pneumonia_suggestions(patient_age, severity_level):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        # Optional headers for OpenRouter rankings:
        "HTTP-Referer": "https://yourwebsite.com",  
        "X-Title": "PneumoniaCareBot",
    }

    prompt_text = (
        f"A {patient_age}-year-old patient has been diagnosed with a severity level of "
        f"{severity_level} pneumonia. What are some common recommendations for managing "
        f"suggest some exercise and remedies to overcome this issue and give me a short suggestion in 3 to 4 lines above 50 only is dangesrous below 50 means not dangerous"
    )

    data = {
        "model": "meta-llama/llama-4-maverick:free",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt_text
                    }
                ]
            }
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    result = False
    if response.status_code == 200:
        result = True
        
        print(response.json())
        response = response.json()['choices'][0]['message']['content']
    else:
        response = response.text

    return result, response