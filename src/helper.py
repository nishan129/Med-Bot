from langchain.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

def load_pdf(data):
    loader = DirectoryLoader(data,
                             glob = "*.pdf",
                             loader_cls = PyPDFLoader)
    
    documents = loader.load()
    
    return documents

def text_split(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size= 500, chunk_overlap = 20)
    text_chunks = text_splitter.split_documents(extracted_data)
    
    return text_chunks


def download_hugging_face_embeddings():
    embeddings = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2",model_kwargs= {"device":"cpu"})
    return embeddings

def vector_store(text_chunks,embeddings):
    return FAISS.from_documents(text_chunks, embeddings)