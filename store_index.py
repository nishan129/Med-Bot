from src.helper import load_pdf, text_split, download_hugging_face_embeddings
from pinecone import Pinecone
import pinecone
from dotenv import load_dotenv
import os


load_dotenv() 

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV')

extracted_data = load_pdf("data/")
text_chunks = text_split(extracted_data)
embeddings = download_hugging_face_embeddings()

# pinecone.init(api_key=PINECONE_API_KEY,
#               environment=PINECONE_API_ENV)

pc = Pinecone(api_key="7772d50d-7aa0-4423-8641-22f66fb55a37")
index_name = "med-bot"
index = pc.Index(index_name)
#docsearch = pc.from_texts([t.page_content for t in text_chunks], embeddings, index_name=index_name)
#print(len(text_chunks[0:6000]))
# Generate embeddings for each text chunk
vectors = []
for i, chunk in enumerate(text_chunks[1000:2000]):

    vector = embeddings.embed_query(chunk.page_content)  # Generate embedding for the text
    vectors.append({
        "id": f"vec{i+1}",  # Unique ID for each vector
        "values": vector,   # The embedding values
    })
    
index.upsert(vectors=vectors)
    
