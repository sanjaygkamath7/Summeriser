import streamlit as st
from PyPDF2 import PdfReader
from docx import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from streamlit_extras.add_vertical_space import add_vertical_space
from langchain.llms.cohere import Cohere
from langchain.chains.question_answering import load_qa_chain
from langchain import PromptTemplate, LLMChain
from langchain.callbacks import get_openai_callback
import pickle
from langchain.embeddings.huggingface_hub import HuggingFaceHubEmbeddings
import os
import pymongo



COHERE_API_KEY = os.getenv('COHERE_API_KEY') or 'ceBXM6Q8ggpUzZGzcNLZfbE7tEq9mF4qxC58UUrz'
HUGGING_FACE_API = os.getenv("HUGGING_FACE") or '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'

if not COHERE_API_KEY:
    raise ValueError("COHERE_API_KEY is not set")
if not HUGGING_FACE_API:
    raise ValueError("HUGGING_FACE_API is not set")

embedding_model = "sentence-transformers/all-mpnet-base-v2"
llm_model = "google/flan-t5-xl"
llm = Cohere(cohere_api_key=COHERE_API_KEY)

# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://sanjaykamath6969:wBgUzSlKebdHlsXJ@cluster0.wlatvo2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["Login"]
collection = db["Signup"]

# Function to insert data into MongoDB
def insert_data(data):
    collection.insert_one(data)
    st.success("Data inserted successfully!")

# Function to retrieve data from MongoDB
def get_data():
    data = list(collection.find())
    return data

# Streamlit app
def main():
    st.title("Streamlit MongoDB Integration")
    
    # Input form to insert data
    st.subheader("Insert Data")
    name = st.text_input("Name")
    age = st.number_input("Age")
    submit_button = st.button("Submit")
    if submit_button:
        data = {"name": name, "age": age}
        insert_data(data)
    
    # Display retrieved data
    st.subheader("Data from MongoDB")
    data = get_data()
    for item in data:
        st.write(f"Name: {item['name']}, Age: {item['age']}")
        
def extract_text_from_docx(docx_file):
    doc = Document(docx_file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def summarize_text(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function=len)
    template = '''Hi, I want you to act as an AI Assistant for high school students who want to understand the book. 
    The text of the book is {text}. Please keep your language in layman's terms. Can you please summarize this book in 
    20 words? '''
    prompt = PromptTemplate(input_variables=["text"], template=template)
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    
    if len(text) > 4000:
        contract_text = text[:4000]
        summary = llm_chain.run(contract_text)
    else:
        summary = llm_chain.run(text)
    
    return summary, text_splitter.split_text(text)

def summerise():
    user_input_file = st.file_uploader("Upload your PDF or DOCX file:", type=['pdf', 'docx'])
    if user_input_file is not None:
        if user_input_file.type == 'application/pdf':
            pdf_file = PdfReader(user_input_file)
            text = ""
            for page in pdf_file.pages:
                text += page.extract_text()
        elif user_input_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            text = extract_text_from_docx(user_input_file)
        else:
            st.error("Unsupported file format. Please upload a PDF or DOCX file.")
            return
        
        st.session_state["summary"], chunks = summarize_text(text)
        
        root_embedding_path = 'src/embeddings'
        store_name = user_input_file.name[:-4]
        embedding_root_path = os.path.join(root_embedding_path, store_name)
        
        if os.path.exists(f'{embedding_root_path}.pkl'):
            with open(f"{embedding_root_path}.pkl", "rb") as f:
                st.session_state["VectorStore"] = pickle.load(f)
        else:
            embeddings = HuggingFaceHubEmbeddings(repo_id=embedding_model, huggingfacehub_api_token=HUGGING_FACE_API)
            st.session_state["VectorStore"] = FAISS.from_texts(chunks, embedding=embeddings)
            with open(f"{embedding_root_path}.pkl", "wb") as f:
                pickle.dump(st.session_state["VectorStore"], f)
        
        st.markdown("Summary of the document:")
        st.write(st.session_state["summary"])
        add_vertical_space(2)
        
        query = st.text_input("Ask questions about your document:")
        if query and "VectorStore" in st.session_state:
            docs = st.session_state["VectorStore"].similarity_search(query=query, k=3)
            chain = load_qa_chain(llm=llm, chain_type="stuff")
            with get_openai_callback() as cb:
                response = chain.run(input_documents=docs, question=query)
                print(cb)
            st.write(response)

if __name__ == "__main__":
    summerise()
