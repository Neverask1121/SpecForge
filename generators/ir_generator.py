import json
from groq import Groq

from models.ir_schema import IR
from prompts.ir_prompt import IR_PROMPT

client = Groq()


def generate_ir(requirement: str):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": IR_PROMPT
            },
            {
                "role": "user",
                "content": requirement
            }
        ]
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError("LLM returned empty response")

    content = content.strip()

    if content.startswith("```json"):
        content = content.replace("```json", "", 1)

    if content.startswith("```"):
        content = content.replace("```", "", 1)

    if content.endswith("```"):
        content = content[:-3]

    content = content.strip()

    data = json.loads(content)

    return IR(**data)