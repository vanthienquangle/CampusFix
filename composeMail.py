import google.generativeai as genai
from PIL import Image

genai.configure(api_key="AIzaSyDQa8b4K1Wcpc3OhpXBtGDgym5eXJgtPOY")

image = Image.open("image.jpg")

model = genai.GenerativeModel("gemini-1.5-flash")

response = model.generate_content([
    "Describe the problem identified in the provided image",
    image
])

print(response.text)