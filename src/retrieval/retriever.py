from typing import List, Dict, Any
from src.embeddings.model_loader import EmbeddingModel
from src.vector_store.chroma_manager import ChromaManager

class Retriever:
    def __init__(self):
        """
        Initializes the Retriever with the embedding model and vector store.
        """
        self.embedding_model = EmbeddingModel()
        self.vector_db = ChromaManager()

    def retrieve(self, query: str, top_k: int = 5) -> Dict[str, List[Any]]:
        """
        Performs cross-modal retrieval.
        1. Embeds the text query.
        2. Searches the vector DB for the nearest neighbors (images OR text).
        3. Formats the results for the generator.
        """
        print(f"Retrieving for query: '{query}'")
        
        # 1. Convert text query to vector
        query_embedding = self.embedding_model.embed_text(query)

        # 2. Query the database
        # We query for slightly more than top_k to allow for filtering if needed
        raw_results = self.vector_db.query_similar(query_embedding, n_results=top_k * 2)

        # 3. Parse and Fuse Results
        # Chroma returns lists of lists (batch format), so we take the first index [0]
        ids = raw_results['ids'][0]
        documents = raw_results['documents'][0]
        metadatas = raw_results['metadatas'][0]
        distances = raw_results['distances'][0]

        retrieved_items = []
        
        for i in range(len(ids)):
            item = {
                "id": ids[i],
                "content": documents[i], # Text content or Image description
                "metadata": metadatas[i], # Contains 'image_path', 'page_number', etc.
                "score": 1 - distances[i] # Convert distance to similarity score (approx)
            }
            retrieved_items.append(item)

        # 4. Re-Ranking / Filtering (The "Fusion" Logic)
        # We sort by score descending to get the most relevant first
        retrieved_items.sort(key=lambda x: x['score'], reverse=True)
        
        # Return only the requested top_k
        final_results = retrieved_items[:top_k]
        
        return self._categorize_results(final_results)

    def _categorize_results(self, results: List[Dict]) -> Dict[str, List[Any]]:
        """
        Helper to separate images and text for the LLM.
        """
        categorized = {
            "text_chunks": [],
            "images": []
        }

        for item in results:
            # Check metadata to see if it's an image or text
            # (We set this 'type' during ingestion)
            if item['metadata'].get('type') == 'image':
                categorized['images'].append(item)
            else:
                categorized['text_chunks'].append(item)

        return categorized

if __name__ == "__main__":
    # Test
    retriever = Retriever()
    # results = retriever.retrieve("What does the performance graph show?")
    # print(f"Found {len(results['text_chunks'])} texts and {len(results['images'])} images.")