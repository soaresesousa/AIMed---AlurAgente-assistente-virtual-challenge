from pathlib import Path
from langchain_core.documents import Document
from pypdf import PdfReader


def ler_pdfs(caminho_pasta: str) -> list[Document]:
    documentos = []

    for caminho_pdf in Path(caminho_pasta).glob("*.pdf"):
        leitor = PdfReader(caminho_pdf)

        for numero_pagina, pagina in enumerate(leitor.pages, start=1):
            texto = pagina.extract_text() or ""

            if texto.strip():
                documentos.append(
                    Document(
                        page_content=texto,
                        metadata={"source": caminho_pdf.name, "page": numero_pagina},
                    )
                )

    return documentos