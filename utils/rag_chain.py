from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def get_langchain_rag_chain(retriever):
    llm = ChatOpenAI(model_name="gpt-3.5-turbo")
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

def is_query_related(query, model, chunks, threshold=0.6):
    query_emb = model.embed_query(query)
    chunk_embs = model.embed_documents(chunks)
    sims = cosine_similarity([query_emb], chunk_embs)
    return np.max(sims) > threshold
