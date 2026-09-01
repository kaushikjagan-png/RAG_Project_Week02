from dotenv import load_dotenv
from rag import RAGService, Settings

if __name__ == "__main__":
    load_dotenv()
    count = RAGService(Settings.from_env()).ingest()
    print(f"Indexed {count} chunks successfully.")
