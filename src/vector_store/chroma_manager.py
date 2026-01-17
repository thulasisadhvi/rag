import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any
import uuid

class ChromaManager:
    def __init__(self, persist_dir: str = "chroma_db"):
        """
        Initialize ChromaDB client.
        :param persist_dir: Where to save the database files on disk.
        """
        self.client = chromadb.PersistentClient(path=persist_dir)
        
        # Create or get the collection. 
        # We use cosine similarity which is standard for embeddings.
        self.collection = self.client.get_or_create_collection(
            name="multimodal_rag",
            metadata={"hnsw:space": "cosine"}
        )

    def add_data(self, 
                 embeddings: List[List[float]], 
                 documents: List[str], 
                 metadatas: List[Dict[str, Any]]):
        """
        Add data to the vector database.
        """
        if not embeddings:
            return

        # Generate unique IDs for each chunk
        ids = [str(uuid.uuid4()) for _ in range(len(embeddings))]

        self.collection.add(
            embeddings=embeddings,
            documents=documents, # The actual text content (or image description)
            metadatas=metadatas, # The rich metadata (page #, type, image_path)
            ids=ids
        )
        print(f"Added {len(ids)} items to ChromaDB.")

    def query_similar(self, query_embedding: List[float], n_results: int = 5):
        """
        Search the database for the most similar content.
        """
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        return results

if __name__ == "__main__":
    # Test
    db = ChromaManager()
    print("ChromaDB initialized.")