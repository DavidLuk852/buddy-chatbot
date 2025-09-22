import requests
from bs4 import BeautifulSoup
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

def fetch_web_content(urls):
    documents = []
    cache_file = 'data.txt'
    if Path(cache_file).exists():
        with open(cache_file, 'r', encoding='utf-8') as f:
            return [f.read()]
    session = requests.Session()
    session.mount("https://", requests.adapters.HTTPAdapter(max_retries=3))
    for url in urls:
        try:
            response = session.get(url, timeout=10, verify=True)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text(separator='\n').strip()
            documents.append(text)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            documents.append(f"Error fetching content from {url}")
    with open(cache_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(documents))
    return documents

urls = [
    "https://library.hkbu.edu.hk/using-the-library/opening-hours/regular-service-hours/",
    "https://library.hkbu.edu.hk/using-the-library/opening-hours/public-holiday-arrangements/",
    "https://library.hkbu.edu.hk/using-the-library/opening-hours/typhoon-and-rainstorm-arrangements/",
    "https://ar.hkbu.edu.hk/student-services/course-registration/course-add-drop",
    "https://ar.hkbu.edu.hk/student-services/new-student-orientation/study/course-add-drop-for-new-students",
    "https://ar.hkbu.edu.hk/student-services/academic-results/academic-honours",
    "https://ar.hkbu.edu.hk/student-services/academic-results/academic-problems",
    "https://ar.hkbu.edu.hk/student-services/academic-results/appeal-procedures",
    "https://ar.hkbu.edu.hk/student-services/academic-results/assessment-grading-system",
    "https://ar.hkbu.edu.hk/student-services/academic-results/dismissal",
    "https://ar.hkbu.edu.hk/student-services/graduation/honours-classification",
    "https://ar.hkbu.edu.hk/student-services/graduation/scholastic-awards",
    "https://ar.hkbu.edu.hk/student-services/graduation/schedules-for-approval-of-graduation",
    "https://ar.hkbu.edu.hk/student-services/graduation/important-notes-for-graduating-students",
    "https://sa.hkbu.edu.hk/en/cdc/ussen/what-is-sen/disabilities-and-sen.html?tabs1=others-tab",
    "https://sa.hkbu.edu.hk/en/cdc/ussen/about-the-unit/about-us.html",
    "https://sa.hkbu.edu.hk/en/cdc/ussen/support-for-students-with-sen/learning-support.html",
    "https://ar.hkbu.edu.hk/student-services/special-educational-needs/registration",
    "https://ar.hkbu.edu.hk/student-services/tuition-fees/payment-schedule",
    "https://ar.hkbu.edu.hk/student-services/tuition-fees/tuition-fee-payment-arrangement",
    "https://ar.hkbu.edu.hk/student-services/tuition-fees/deferral-delay-of-tuition-fee-payment",
    "https://ar.hkbu.edu.hk/student-services/course-registration/bad-weather-arrangement",
    "https://ar.hkbu.edu.hk/student-services/course-registration/class-timetable",
    "https://ar.hkbu.edu.hk/student-services/course-registration/pre-registration",
    "https://ar.hkbu.edu.hk/student-services/course-registration/course-withdrawal",
    "https://ar.hkbu.edu.hk/student-services/course-registration/study-load",
    "https://ar.hkbu.edu.hk/student-services/incoming-exchange-and-extended-study-programme/pre-registration",
    "https://ar.hkbu.edu.hk/student-services/incoming-exchange-and-extended-study-programme/course-add-drop",
    "https://ar.hkbu.edu.hk/student-services/incoming-exchange-and-extended-study-programme/course-list/for-2025-26-fall-semester-physical-exchange",
    "https://ar.hkbu.edu.hk/student-services/incoming-exchange-and-extended-study-programme/course-list/for-2025-26-spring-semester-physical-exchange",
    "https://ar.hkbu.edu.hk/student-services/incoming-exchange-and-extended-study-programme/important-notes-for-incoming-exchange-and-extended-study-programme-students",
    "https://ar.hkbu.edu.hk/student-services/student-record/amendment-of-personal-data",
    "https://ar.hkbu.edu.hk/student-services/student-record/hkbu-digital-credential-system",
    "https://ar.hkbu.edu.hk/student-services/student-record/replacement-of-student-card",
    "https://ar.hkbu.edu.hk/student-services/student-record/testimonial",
    "https://ar.hkbu.edu.hk/student-services/student-record/transcript",
    "https://ar.hkbu.edu.hk/student-services/useful-information/mtr-student-travel-scheme",
    "https://ar.hkbu.edu.hk/student-services/useful-information/non-local-student-visa",
    "https://ar.hkbu.edu.hk/student-services/useful-information/student-e-card",
    "https://ar.hkbu.edu.hk/student-services/examinations/make-up-exam",
    "https://ar.hkbu.edu.hk/student-services/examinations/supplementary-exam",
    "https://ar.hkbu.edu.hk/student-services/learning-and-teaching/undergraduate-curriculum-structure",
    "https://ar.hkbu.edu.hk/student-services/learning-and-teaching/learning-pathways",
    "https://ar.hkbu.edu.hk/student-services/learning-and-teaching/academic-advising",
    "https://ar.hkbu.edu.hk/student-services/exemption-unit-transfer/year-1-students",
    "https://ar.hkbu.edu.hk/student-services/exemption-unit-transfer/fulfilling-minor-requirements",
    "https://ar.hkbu.edu.hk/student-services/exemption-unit-transfer/overseas-exchange",
    "https://ar.hkbu.edu.hk/student-services/exemption-unit-transfer/extended-study-programme",
    "https://ar.hkbu.edu.hk/student-services/exemption-unit-transfer/local-collaboration-scheme",
    "https://ar.hkbu.edu.hk/student-services/exemption-unit-transfer/exemption-from-uclc1005",
    "https://ar.hkbu.edu.hk/student-services/major-concentration-minor/major-transdisciplinary-second-major-second-major",
    "https://ar.hkbu.edu.hk/student-services/major-concentration-minor/change-of-study-programme",
    "https://ar.hkbu.edu.hk/student-services/major-concentration-minor/concentrations",
    "https://ar.hkbu.edu.hk/student-services/major-concentration-minor/double-major-programmes-fass",
    "https://ar.hkbu.edu.hk/student-services/suspension-withdrawal-of-studies/leave-of-absence",
    "https://ar.hkbu.edu.hk/student-services/suspension-withdrawal-of-studies/suspension-of-studies",
    "https://ar.hkbu.edu.hk/student-services/suspension-withdrawal-of-studies/withdrawal-of-studies"
]
web_content = fetch_web_content(urls)

loader = TextLoader("data.txt", encoding='utf-8')
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=250, chunk_overlap=0)
doc_splits = text_splitter.split_documents(docs)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = SKLearnVectorStore.from_documents(
    documents=doc_splits,
    embedding=embeddings,
)
retriever = vectorstore.as_retriever(k=4)

model = ChatOllama(model="llama3.1")
prompt = PromptTemplate(
    template="""You are an assistant for question-answering tasks.
    Use the following documents to answer the question, do not mention document IDs, and consider the context of previous questions if relevant.
    If you don't know the answer, just say that you don't know.
    Use three sentences maximum and keep the answer concise:
    Question: {question} 
    Documents: {documents} 
    Answer: 
    """,
    input_variables=["question", "documents"],
)
parser = StrOutputParser()

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