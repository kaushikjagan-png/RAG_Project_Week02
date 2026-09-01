# Claims RAG application

This app reads PDF/DOCX files from `Documents`, creates embeddings with Nebius Token Factory, stores vectors in Pinecone, and answers grounded questions with a Nebius chat model.

## Run

1. Create and activate a Python 3.10+ virtual environment.
2. Run `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and add your Nebius and Pinecone API keys.
4. Review model IDs and the Pinecone region in `.env`.
5. Run `streamlit run app.py`.
6. Click **Index / refresh documents**, then ask questions.

Run `python ingest.py` for command-line ingestion.

The vector dimension is inferred from the embedding response. If the embedding model changes, use a new index name or recreate the index. Refreshing clears only the configured namespace. Image-only PDFs require OCR and are not supported in this basic version. `.env` is excluded from Git.
