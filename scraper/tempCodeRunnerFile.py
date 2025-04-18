

import openai
import os

# Set your OpenAI API key here (or use os.environ["OPENAI_API_KEY"])
openai.api_key = "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"  # Replace with your key

def generate_qa():
    prompt = f"""
Create a Context Regarding World War 2. Then frame a question and its answer to make a QA Dataset


Respond in the following format:
Context: <context>
Question: <question>
Answer: <answer>
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that creates QA datasets for machine learning."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=300
    )

    output = response["choices"][0]["message"]["content"]
    return output.strip()


qa = generate_qa()
print(qa)
