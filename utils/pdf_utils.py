<<<<<<< HEAD
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
import tempfile
from dotenv import load_dotenv
import os
=======
import tempfile
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings  # updated for new import
>>>>>>> 961e378 (Initail COmmit)

load_dotenv()

def clean_text(text):
    # Remove unwanted special tokens (can also be customized)
    return text.replace("<|endoftext|>", "")

def load_and_embed_pdf(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    loader = PyPDFLoader(tmp_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
<<<<<<< HEAD
    texts = [c.page_content for c in chunks]

    embed_model = OpenAIEmbeddings(disallowed_special=())
    vectorstore = FAISS.from_texts(texts, embed_model)

=======

    texts = [clean_text(c.page_content) for c in chunks]

    # Pass disallowed_special=() to allow all special tokens
    embed_model = OpenAIEmbeddings(
        disallowed_special=()  # ✅ allows special tokens like <|endoftext|>
    )

    vectorstore = FAISS.from_texts(texts, embed_model)

>>>>>>> 961e378 (Initail COmmit)
    return texts, vectorstore.as_retriever(), embed_model
