from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from app.vector_store import get_vector_store
from app.config import LLM_MODEL


def build_qa_chain(project_name: str):
    vectordb = get_vector_store(project_name)

    retriever = vectordb.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    llm = ChatOpenAI(
        model=LLM_MODEL,
        temperature=0
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    return qa


def ask_question(project_name: str, question: str):
    vectordb = get_vector_store(project_name)

    # Get raw similarity results (for score)
    docs_with_scores = vectordb.similarity_search_with_score(
        question,
        k=4
    )

    qa_chain = build_qa_chain(project_name)
    result = qa_chain.invoke({"query": question})

    citations = []

    for doc, score in docs_with_scores:
        citations.append({
            "source": doc.metadata.get("source", "Unknown"),
            "preview": doc.page_content[:200],
            "score": round(float(score), 4)
        })

    return {
        "answer": result["result"],
        "citations": citations
    }