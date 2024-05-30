from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings, load_pdf,text_split, vector_store
from pinecone import Pinecone
#from langchain.vectorstores import Pinecone
from langchain.vectorstores import FAISS
import pinecone
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from src.prompt import *
import os

app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')

extracted_data = load_pdf("data/")
text_chunks = text_split(extracted_data)
embeddings = download_hugging_face_embeddings()

vector_stor = vector_store(text_chunks,embeddings)

PROMPT = PromptTemplate(template=prompt_template, input_variables=['context','question'])
chain_type_kwargs = {"prompt":PROMPT}

llm = CTransformers(model="model/llama-2-7b-chat.ggmlv3.q4_0.bin",
                    model_type='llama',
                    config={
                        "max_new_tokens":512,
                        "temperature":0.8
                    })

qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever = vector_stor.as_retriever(search_kwargs={"k":2}),
    return_source_documents = True,
    chain_type_kwargs=chain_type_kwargs    
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get",methods=['GET','POST'])
def chat():
    msg = request.form['msg']
    input = msg
    print(input)
    result = qa({'query':input})
    print(result)
    return str(result['result'])




if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080,debug=True)