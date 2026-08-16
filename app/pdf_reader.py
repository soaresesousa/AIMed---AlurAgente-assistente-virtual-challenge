import os
from pypdf import PdfReader

def ler_pdfs(caminho_pasta):
    texto_completo = ""

    for arquivo in os.listdir(caminho_pasta):
        if arquivo.endswith('.pdf'):
            caminho_arquivo = os.path.join(caminho_pasta, arquivo)
            leitor = PdfReader(caminho_arquivo)
            for pagina in leitor.pages:
                texto = pagina.extract_text()
                texto_completo += texto + "\n"
    return texto_completo