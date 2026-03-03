from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from app.config import VECTOR_DB_PATH, EMBEDDING_MODEL
import os


def get_vector_store(project_name: str):
    project_path = os.path.join(VECTOR_DB_PATH, project_name)

    os.makedirs(project_path, exist_ok=True)

    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    vectordb = Chroma(
        persist_directory=project_path,
        embedding_function=embeddings
    )

    return vectordb


def add_chunks(project_name: str, chunks, source_name):
    vectordb = get_vector_store(project_name)

    metadatas = [{"source": source_name} for _ in chunks]

    vectordb.add_texts(
        texts=chunks,
        metadatas=metadatas
    )

    vectordb.persist()