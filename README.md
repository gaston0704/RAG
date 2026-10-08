# RAG PDF Chatbot

A lightweight Retrieval-Augmented Generation (RAG) application that lets you ask questions about a PDF document using a local vector database and Google's Gemini models.

This project loads a PDF, splits it into chunks, creates embeddings, stores them in Chroma, and answers user queries by retrieving the most relevant passages before generating a response.

## Features

- PDF ingestion with `PyPDFLoader`
- Text chunking with `RecursiveCharacterTextSplitter`
- Embeddings using Google Generative AI
- Vector storage with Chroma
- Retrieval-based question answering with LangChain
- Simple interactive CLI chat loop

## Tech Stack

- Python 3.10+
- LangChain
- LangChain Community
- Chroma
- Google Generative AI (Gemini)
- python-dotenv
- PyPDF

## Project Structure

```text
My-RAG-project/
├── .env                     # Local environment variables (API key)
├── rag_app.py               # Main RAG application
├── chroma_db/               # Persisted vector database (generated at runtime)
├── Curs.pdf  # Source PDF document
├── venv/                    # Virtual environment
├── .gitignore               # Git ignore rules
└── README.md                # Project documentation
```

## Prerequisites

Before running the app, make sure you have:

- Python installed
- A Google API key with access to Gemini models
- A PDF file to index

## Setup

1. Open a terminal in the project folder.

2. Create and activate a virtual environment:

```bash
python -m venv venv
```

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

3. Install the required packages:

```bash
pip install python-dotenv pypdf langchain langchain-community langchain-google-genai chromadb
```

4. Create a `.env` file in the project root and add your Google API key:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

5. Place your PDF in the project root and ensure the filename matches the loader in `rag_app.py`.

The app currently expects:

```python
loader = PyPDFLoader("TechCorp_Official_Employee_Handbook.pdf")
```

If your file has a different name, update that line in `rag_app.py`.

## Run the App

Start the chatbot:

```bash
python rag_app.py
```

You will see a prompt like:

```text
Your Question:
```

Type a question about the PDF and press Enter. To exit, type:

```text
exit
```

or

```text
quit
```

## How It Works

1. The PDF is loaded and converted into document pages.
2. The text is split into smaller chunks.
3. Each chunk is embedded using a Google embedding model.
4. The chunks are saved into Chroma for retrieval.
5. User questions are compared against the stored vectors.
6. The most relevant chunks are passed to Gemini as context.
7. Gemini generates a concise answer based on the retrieved content.

## Important Notes

- The Chroma database is stored in `./chroma_db` and will be created automatically on first run.
- The app uses the Google Gemini model configured in `rag_app.py`.
- If your PDF is large, adjust the chunk size and retrieval number in the code to improve quality and performance.

## Example

```text
Your Question: What is the company leave policy?
Answer: The employee handbook states that employees are entitled to ...
```

## Troubleshooting

- If the app cannot load the PDF, check that the filename is correct.
- If the API call fails, verify that `GOOGLE_API_KEY` is set correctly in `.env`.
- If dependencies are missing, run the installation command again inside the active virtual environment.
