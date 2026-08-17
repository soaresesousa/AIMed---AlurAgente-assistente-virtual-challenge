import os
from langchain_google_genai import ChatGoogleGenerativeAI

def main():
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        google_api_key=os.environ["GEMINI_API_KEY"]        
    )

    resp = llm.invoke("Responda com uma frase: O que é rag?")
    print(resp.content)

if __name__ == "__main__":
    main()