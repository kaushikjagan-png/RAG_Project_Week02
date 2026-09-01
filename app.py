from pathlib import Path

from dotenv import load_dotenv
import streamlit as st
from rag import RAGService, Settings

# Streamlit reruns this module in a long-lived process. Override stale values that
# may have been loaded from an earlier version of .env, and resolve the file
# relative to this application rather than the terminal's working directory.
load_dotenv(dotenv_path=Path(__file__).with_name(".env"), override=True)
st.set_page_config(page_title="Claims RAG", page_icon="🔎")
st.title("Claims document assistant")
st.caption("Grounded answers from the supplied PDF and DOCX claim files.")

try:
    settings = Settings.from_env()
    service = RAGService(settings)
except Exception as exc:
    st.error(str(exc))
    st.info("Copy .env.example to .env, add your Nebius and Pinecone API keys, then restart.")
    st.stop()

with st.sidebar:
    st.subheader("Knowledge base")
    st.code(
        f"{settings.index_name}\n"
        f"namespace: {settings.namespace}\n"
        f"embeddings: {settings.embedding_model}",
        language=None,
    )
    if st.button("Index / refresh documents", type="primary", use_container_width=True):
        with st.spinner("Extracting, embedding, and indexing..."):
            try:
                st.success(f"Indexed {service.ingest()} chunks.")
            except Exception as exc:
                st.error(f"Indexing failed: {exc}")

question = st.chat_input("Ask about the claim, policy, reports, or correspondence")
if question:
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        with st.spinner("Searching the claim files..."):
            try:
                answer, sources = service.ask(question)
                st.markdown(answer)
                if sources:
                    with st.expander("Retrieved sources"):
                        for source in sources:
                            st.write(f"[{source['number']}] {source['source']} — page/section {source['page']} (score {source['score']:.3f})")
            except Exception as exc:
                st.error(f"Question answering failed: {exc}")
