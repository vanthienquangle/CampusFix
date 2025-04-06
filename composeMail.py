# Testing generative purpose
import google.generativeai as genai
import json
from PIL import Image

genai.configure(api_key="")

image = Image.open("faucet.jpg")

model = genai.GenerativeModel("gemini-1.5-flash")

response = model.generate_content([
    "Describe the problem identified in the provided image",
    image
])

# Load contact responsibilities
with open('contacts.json') as f:
    CONTACTS = json.load(f)

def find_contact_by_issue(issue_text):
    issue_lower = issue_text.lower()
    for role, info in CONTACTS.items():
        for keyword in info["keywords"]:
            if keyword in issue_lower:
                return info  # {name, email, keywords}
    return None

print(response.text)
print(find_contact_by_issue(response.text)["name"])
