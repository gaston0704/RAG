import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

# Load environment variables from the .env file (GOOGLE_API_KEY)
load_dotenv()
if not os.getenv("GOOGLE_API_KEY"):
    sys.exit("GOOGLE_API_KEY is missing. Create a .env file with GOOGLE_API_KEY=your_key")

# PDF to index: pass a path as argument, e.g. `python rag_app.py my_document.pdf`
pdf_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("sample_employee_handbook.pdf")
if not pdf_path.is_file():
    sys.exit(f"PDF not found: {pdf_path}")

# One vector database per PDF: documents don't mix and the index is reused between runs
db_dir = Path("chroma_db") / pdf_path.stem

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

if db_dir.is_dir() and any(db_dir.iterdir()):
    print(f"Loading existing vector database for {pdf_path.name}...")
    vector_db = Chroma(persist_directory=str(db_dir), embedding_function=embeddings)
else:
    # Load the PDF document
    print(f"Loading {pdf_path.name}...")
    document = PyPDFLoader(str(pdf_path)).load()

    # Chunking the text
    print("Chunking text...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = text_splitter.split_documents(document)

    # Create embeddings and store them in the vector DB
    print(f"Creating vector database ({len(chunks)} chunks)...")
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(db_dir)
    )

# Configure the database to act as a document retriever
retriever = vector_db.as_retriever(search_kwargs={"k": 2})

# Define the prompt structure for the LLM
template = """
Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, just say that you don't know. 
Use three sentences maximum and keep the answer concise.

Context: {context}

Question: {question}

Answer:
"""
prompt = PromptTemplate.from_template(template)

# Initialize the free Gemini model tier
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=0)

# Helper function to stitch retrieved chunks into a single text block
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Connect everything together using LangChain Expression Language (LCEL)
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
)

# Chat with your PDF in a continuous loop
print("\n--- PDF Chatbot Initialized ---")
print("Type 'exit' or 'quit' to stop.")

while True:
    # 1. Wait for the user to type a question
    user_question = input("\nYour Question: ")

    # 2. Allow the user to break the loop and close the program
    if user_question.lower() in ['exit', 'quit']:
        print("Shutting down chatbot. Goodbye!")
        break

    # 3. Send the question through our RAG chain
    response = rag_chain.invoke(user_question)

    # 4. Clean up the output format
    if isinstance(response.content, list):
        clean_answer = response.content[0]['text']
    else:
        clean_answer = response.content

    # 5. Print the final answer to the console
    print(f"Answer: {clean_answer}")