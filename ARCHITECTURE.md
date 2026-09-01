# Architecture

## Component diagram

```mermaid
flowchart LR
    User[Claims user] --> UI[Streamlit UI<br/>app.py]

    subgraph App[Claims RAG application]
        UI --> Service[RAGService<br/>rag.py]
        Docs[(PDF and DOCX<br/>Documents folder)] --> Loader[Document extraction]
        Loader --> Chunker[Overlapping chunks]
        Chunker --> Service
        Service --> Prompt[Grounded prompt<br/>with numbered context]
    end

    Service -->|Document and query text| Embed[Nebius embedding model]
    Embed -->|Vectors| Service
    Service -->|Create, upsert, query| Pinecone[(Pinecone index<br/>and namespace)]
    Pinecone -->|Top-k chunks and metadata| Service
    Prompt -->|Context plus question| Chat[Nebius chat model]
    Chat -->|Answer with citations| UI
```

## Ingestion flow

```mermaid
sequenceDiagram
    actor User
    participant UI as Streamlit
    participant RAG as RAGService
    participant Files as PDF/DOCX files
    participant Nebius as Nebius embeddings
    participant PC as Pinecone

    User->>UI: Click Index / refresh documents
    UI->>RAG: ingest()
    RAG->>Files: Extract pages, paragraphs, tables
    RAG->>RAG: Normalize and chunk text
    RAG->>Nebius: Embed first batch
    Nebius-->>RAG: Vectors and dimension
    RAG->>PC: Create index if missing
    RAG->>PC: Check namespace existence
    opt Namespace exists
        RAG->>PC: Delete vectors in namespace
    end
    loop Batches
        RAG->>Nebius: Embed chunks
        RAG->>PC: Upsert vectors and metadata
    end
    RAG-->>UI: Indexed chunk count
```

## Question-answering flow

```mermaid
sequenceDiagram
    actor User
    participant UI as Streamlit
    participant RAG as RAGService
    participant Embed as Nebius embeddings
    participant PC as Pinecone
    participant Chat as Nebius chat

    User->>UI: Submit question
    UI->>RAG: ask(question)
    RAG->>PC: Verify index exists
    RAG->>Embed: Embed question
    Embed-->>RAG: Query vector
    RAG->>PC: Cosine top-k query in namespace
    PC-->>RAG: Text and source metadata
    RAG->>Chat: Numbered context plus question
    Chat-->>RAG: Answer with citations
    RAG-->>UI: Answer and retrieved sources
```

## Vector metadata

| Field | Description |
|---|---|
| `source` | Original filename |
| `page` | PDF page or DOCX section marker |
| `chunk` | Chunk number within the page/section |
| `text` | Source text supplied to the chat model |

Vector IDs are deterministic SHA-256-derived identifiers based on filename, page, chunk number, and text.

## Design decisions

- The OpenAI-compatible client supports both Nebius chat and embeddings.
- The first embedding response determines the Pinecone index dimension.
- Refresh deletes only the configured namespace, never the entire index.
- Missing namespaces are not deleted, preventing first-run 404 errors.
- Low-temperature generation reduces variability for claim answers.
- The system prompt requires context-only answers and inline citations.

## Current limitations

- No OCR for scanned PDFs
- Character-based rather than token-based chunks
- No authentication or per-user authorization
- No conversational history
- Generated citation markers should be checked against the retrieved-source panel
- Full chunk text is stored as Pinecone metadata; production use requires a privacy and retention review

