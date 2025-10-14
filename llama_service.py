# llama_service.py
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms.openai import OpenAI
import os

class LlamaService:
    def __init__(self, data_path="data"):
        print("🔄 Loading PDF documents and creating index...")

        # Load all files (PDFs, text, etc.)
        documents = SimpleDirectoryReader(data_path).load_data()

        # Create the vector index
        self.index = VectorStoreIndex.from_documents(documents)
        self.query_engine = self.index.as_query_engine()
        print("✅ Index ready!")

    def query(self, question: str) -> str:
        """Query your indexed documents"""
        response = self.query_engine.query(question)
        return str(response)
