import os
import json

import google.generativeai as genai

from dotenv import load_dotenv

from langchain_community.document_loaders import (
    PyPDFLoader
)

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

loader = PyPDFLoader(
    "employee.pdf"
)

documents = loader.load()

text = "\n".join(
    doc.page_content
    for doc in documents
)

prompt = f"""
You are an Employee Information Extraction Agent.

Extract ONLY the employee details present in the document.

Return ONLY valid JSON.

If a field is missing, return null.

JSON format:

{{
    "employee_name": "",
    "employee_id": "",
    "designation": "",
    "department": "",
    "email": "",
    "phone": "",
    "joining_date": "",
    "salary": "",
    "manager": "",
    "location": ""
}}

Document:

{text}
"""

response = model.generate_content(
    prompt
)

json_text = response.text.strip()

if json_text.startswith("```json"):
    json_text = json_text.replace("```json", "")
    json_text = json_text.replace("```", "").strip()

employee = json.loads(json_text)

print(
    json.dumps(
        employee,
        indent=4
    )
)