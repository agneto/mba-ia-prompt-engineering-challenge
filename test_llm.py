import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

try:
    print(f"Testando modelo: {os.getenv('LLM_MODEL')}")
    llm = ChatGoogleGenerativeAI(model=os.getenv('LLM_MODEL'), temperature=0)
    response = llm.invoke("Olá, isso é um teste.")
    print(f"Resposta: {response.content}")
except Exception as e:
    print(f"Erro no teste: {e}")
