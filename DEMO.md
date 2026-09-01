# Demo script

## Objective

Demonstrate document ingestion, semantic retrieval, grounded generation, and source inspection for an insurance claim. Estimated duration: 5–7 minutes.

## Before presenting

1. Start the application:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   python -m streamlit run app.py
   ```

2. Confirm the sidebar displays:

   ```text
   rag-segment-01
   namespace: rag-project
   embeddings: Qwen/Qwen3-Embedding-8B
   ```

3. Ensure no API keys are visible on screen.

## Presenter walkthrough

### 1. Introduce the use case — 30 seconds

Say:

> This assistant helps a claims reviewer search policy, incident, repair, receipt, correspondence, and claims-history documents. Retrieval-augmented generation gives the model relevant source passages before it answers.

Explain that Nebius provides embeddings and chat generation while Pinecone stores and searches vectors.

### 2. Index documents — 60–120 seconds

Click **Index / refresh documents**.

Say:

> The app extracts PDF and DOCX text, creates overlapping chunks, embeds them with Nebius, and uploads the vectors and source metadata to one Pinecone namespace. A refresh replaces only that namespace.

Expected result:

```text
Indexed <number> chunks.
```

The exact count depends on the documents and chunk configuration.

### 3. Ask for an overview — 60 seconds

Ask:

```text
Walk me through the insurance claim process described in these documents.
```

Expected observations:

- The answer uses retrieved claim and policy passages.
- Citation markers such as `[1]` appear.
- **Retrieved sources** lists filenames, pages/sections, and scores.

Expand **Retrieved sources** and connect one citation to its source.

### 4. Ask a focused evidence question — 60 seconds

Ask one of:

```text
What damage was reported, and which documents support it?
```

```text
Summarize the repair quote and identify the quoted amount.
```

```text
What policy terms appear relevant to this claim?
```

Say:

> The question becomes an embedding. Pinecone returns semantically similar chunks, and the chat model receives those chunks as evidence.

Verify important dates, amounts, and terms against retrieved sources.

### 5. Test insufficient context — 45 seconds

Ask:

```text
What was the weather in London yesterday?
```

Expected behavior: the assistant states that the supplied context is insufficient instead of inventing an answer.

### 6. Close — 30 seconds

Say:

> This prototype demonstrates the complete RAG loop: extraction, chunking, embeddings, vector storage, semantic retrieval, grounded generation, and source inspection. Production enhancements would include OCR, authentication, evaluation, monitoring, and stricter controls for sensitive claim information.

## Recovery notes

- **Model not found:** verify the exact Nebius model ID, restart Streamlit, and check the sidebar.
- **Index not found:** use a lowercase/hyphenated index name and index before querying.
- **Namespace not found:** run the current `rag.py`, which checks namespace existence before deletion.
- **Dimension mismatch:** use a new Pinecone index name after changing embedding models.
- **Slow first run:** narrate the architecture while the index is created and documents are embedded.

