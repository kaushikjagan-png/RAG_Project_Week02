# Claims Document RAG Assistant

A retrieval-augmented generation application for insurance claim files. It extracts PDF/DOCX text, generates embeddings with Nebius Token Factory, stores vectors in Pinecone, retrieves relevant passages, and produces grounded answers with citations.

## Features

- PDF and DOCX ingestion, including DOCX tables
- Boundary-aware overlapping chunks
- Nebius chat and embedding models through an OpenAI-compatible API
- Automatic Pinecone serverless index creation
- Safe namespace refresh for new and existing namespaces
- Retrieved filenames, page/section numbers, and similarity scores
- Grounded answers with inline citation markers
- Streamlit UI and command-line ingestion

See [ARCHITECTURE.md](ARCHITECTURE.md) for component and sequence diagrams. Use [DEMO.md](DEMO.md) for a presenter-ready walkthrough.

## Prerequisites

- Python 3.10+
- Nebius Token Factory API key
- Pinecone API key and an available serverless region

## Install

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and add API keys. Never commit `.env`.

## Configuration

| Variable | Purpose | Example |
|---|---|---|
| `NEBIUS_API_KEY` | Nebius authentication | Secret value |
| `NEBIUS_BASE_URL` | Nebius API endpoint | `https://api.tokenfactory.nebius.com/v1/` |
| `NEBIUS_CHAT_MODEL` | Answer model | `Qwen/Qwen3-235B-A22B-Instruct-2507` |
| `NEBIUS_EMBEDDING_MODEL` | Document/query embedding model | `Qwen/Qwen3-Embedding-8B` |
| `PINECONE_API_KEY` | Pinecone authentication | Secret value |
| `PINECONE_INDEX_NAME` | Vector index | `rag-segment-01` |
| `PINECONE_NAMESPACE` | Dataset partition | `rag-project` |
| `PINECONE_CLOUD` | Serverless cloud | `aws` |
| `PINECONE_REGION` | Serverless region | `us-east-1` |
| `DOCUMENTS_DIR` | Source folder | `Documents` |
| `CHUNK_SIZE` | Approximate characters per chunk | `1200` |
| `CHUNK_OVERLAP` | Repeated characters between chunks | `200` |
| `TOP_K` | Retrieved chunks per question | `5` |

Model availability can vary by Nebius account. Pinecone index names must use lowercase letters, numbers, and hyphens.

## Run

```powershell
python -m streamlit run app.py
```

1. Confirm the intended index, namespace, and embedding model in the sidebar.
2. Click **Index / refresh documents** and wait for success.
3. Ask a question.
4. Expand **Retrieved sources** to inspect evidence and similarity scores.

Command-line ingestion:

```powershell
python ingest.py
```

## Troubleshooting

### `pip` is not recognized

Install Python, reopen PowerShell, and use `python -m pip install -r requirements.txt`.

### Nebius says the model does not exist

Use an exact model ID available to your Nebius account. Restart Streamlit after editing `.env` and confirm the effective model in the sidebar.

### Pinecone index not found

Use a lowercase/hyphenated index name and click **Index / refresh documents** before asking questions.

### Pinecone namespace not found

The current application checks namespace existence before deletion. Restart Streamlit after updating `rag.py`, then index again.

### Vector dimension mismatch

Use a new `PINECONE_INDEX_NAME` after changing the embedding model, or recreate the old index.

### No text extracted

This version supports text-based PDF and DOCX files. Scanned PDFs require OCR.

## Security

- `.env` is excluded by `.gitignore`.
- Never paste or upload screenshots containing API keys.
- Immediately revoke and rotate exposed credentials.
- Review privacy, retention, and encryption requirements before using real claim data.

## Project layout

```text
.
├── app.py
├── rag.py
├── ingest.py
├── Documents/
├── .env.example
├── ARCHITECTURE.md
├── DEMO.md
└── requirements.txt
```
