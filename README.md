# RAG PDF Chatbot

A small Retrieval-Augmented Generation (RAG) app that answers questions about a PDF, using a local
Chroma vector database and Google's Gemini models. Answers are generated only from the passages
retrieved from the document; if the document doesn't contain the answer, the model is instructed to say so.

## How it works

1. The PDF is loaded page by page (`PyPDFLoader`).
2. The text is split into chunks of 500 characters with 50 characters of overlap (`RecursiveCharacterTextSplitter`).
3. Each chunk is embedded with `gemini-embedding-001` and stored in a local Chroma database.
4. For each question, the 2 most similar chunks are retrieved.
5. The chunks and the question are sent to Gemini (temperature 0) with a prompt that restricts the answer to the
   retrieved context (max. three sentences).

The vector database is stored in `chroma_db/<pdf name>/`, so each PDF is indexed once and reused on later runs.

## Quick start

```bash
python -m venv venv
venv\Scripts\activate          # Windows (on macOS/Linux: source venv/bin/activate)
pip install -r requirements.txt
```

Create a `.env` file in the project folder with your Google API key (it is git-ignored and must never be committed):

```
GOOGLE_API_KEY=your_google_api_key_here
```

Run it on the included fictional sample document:

```bash
python rag_app.py
```

Or on your own PDF:

```bash
python rag_app.py path/to/your_document.pdf
```

Type a question at the `Your Question:` prompt; type `exit` or `quit` to stop.

## Test questions

`sample_employee_handbook.pdf` is a fictional one-page handbook written for testing. These questions have known answers
in it, plus one question that is deliberately not covered, to check that the app says it doesn't know instead of inventing an answer.

| Question | Expected answer |
|---|---|
| How many days of annual leave do employees get? | 21 working days per year |
| How many unused leave days can be carried over, and until when? | Up to 5 days, until 31 March |
| When is a medical certificate required? | After 3 consecutive sick days |
| How many days per week can I work remotely? | Up to 2, with manager approval |
| Who must approve expenses above 200 EUR? | The department head |
| Can I store customer data on my personal laptop? | No |
| What is the name of the CEO? | Not in the document: should answer that it doesn't know |

## Project structure

```
.
├── rag_app.py                       # Main application
├── sample_employee_handbook.pdf     # Fictional sample document for testing
├── requirements.txt
├── .gitignore                       # Excludes .env, chroma_db/, venv/ and other PDFs
└── README.md
```

## Limitations and next steps

- Retrieval returns only the top 2 chunks of 500 characters, so questions that need information from several parts of a long document may be answered incompletely. Chunk size and `k` are set in `rag_app.py`.
- Answers don't show their source page yet; adding page-number citations would make them easier to verify.
- The test questions above are checked by hand; automating them (question, expected fact, pass/fail) is the next step.
- Only Gemini is used at the moment. Switching the chat model to another provider (for example Claude) means replacing the `ChatGoogleGenerativeAI` line; the embeddings are a separate choice.