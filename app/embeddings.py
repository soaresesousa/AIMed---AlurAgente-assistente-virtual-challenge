from google import genai

client = genai.Client()

vetores = []

def embeddings_func(chunks):
    for chunk in chunks:
        resposta = client.models.embed_content(
            model="gemini-embedding-001",
            contents=chunk
        )
        vetores.append(resposta.embeddings[0].values)    
    
    return vetores