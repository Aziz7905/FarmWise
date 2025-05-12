from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from .llm import GroqLlamaLLM
from .retrievers import load_ensemble_retriever

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are a crop rotation assistant.

ONLY use the CONTEXT below to answer the QUESTION.
Respond in 1–3 sentences. Avoid words like 'context' or 'document'.

CONTEXT:
{context}

QUESTION:
{question}

FINAL ANSWER:"""
)

retriever = load_ensemble_retriever()
llm = GroqLlamaLLM()

qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=False,
    chain_type_kwargs={"prompt": prompt}
)

def answer_question(query: str) -> str:
    return qa.run(query)
