from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model = 'gemini-2.5-pro')

response = model.invoke("Write a poem about the sea.")

print(response.content)
