from langchain_community.document_loaders.mongodb import MongodbLoader
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import SKLearnVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import os
from pathlib import Path

# Load existing data from data.txt
#cache_file = 'data.txt'
#if not Path(cache_file).exists():
#    raise FileNotFoundError(f"{cache_file} not found. Please create it with the required data.")

#loader = TextLoader(cache_file, encoding='utf-8')
#docs = loader.load()

# Load from MongoDB (replace with your connection details)
loader = MongodbLoader(
    connection_string="mongodb://localhost:27017/",  # or your MongoDB URI
    db_name="testing",  # e.g., "hkbu_data"
    collection_name="testing",  # e.g., "campus_info"
    filter_criteria={},  # Optional: filter dict, e.g., {"category": "library"}
    field_names=["content"]  # Optional: fields to extract, e.g., your data field
)
docs = loader.load()


# Split the documents into chunks
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=250, chunk_overlap=0)
doc_splits = text_splitter.split_documents(docs)

# Initialize embeddings and vector store
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = SKLearnVectorStore.from_documents(
    documents=doc_splits,
    embedding=embeddings,
)
retriever = vectorstore.as_retriever(k=4)

# Initialize the model and prompt
model = ChatOllama(
    model="llama3.1",
    temperature=0.0,
)
prompt = PromptTemplate(
    template="""You are an assistant for question-answering tasks.
    Use the following documents to answer the question concisely.
    If you don't know the answer, just say that you don't know.
    Do not mention Document IDs in the response.
    Question: {question} 
    Documents: {documents} 
    Answer: 
    """,
    input_variables=["question", "documents"],
)
parser = StrOutputParser()

# Set up the RAG chain
rag_chain = (
    {"documents": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | parser
)

if __name__ == "__main__":
    query = "What are the regular library hours at HKBU?"
    response = rag_chain.invoke(query)
    print(f"Question: {query}")
    print(f"Response: {response}")