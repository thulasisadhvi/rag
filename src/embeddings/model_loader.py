from sentence_transformers import SentenceTransformer
from PIL import Image
from typing import List, Union
import numpy as np

class EmbeddingModel:
    def __init__(self, model_name: str = "clip-ViT-B-32"):
        """
        Initializes the CLIP model. 
        'clip-ViT-B-32' is a standard, efficient model for multimodal tasks.
        """
        print(f"Loading embedding model: {model_name}...")
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text: Union[str, List[str]]) -> List[List[float]]:
        """
        Converts text into a vector embedding.
        """
        # CLIP has a short context window (77 tokens). 
        # Ideally, we truncate or summarize text before embedding for CLIP.
        embeddings = self.model.encode(text)
        
        # Convert to list if it's a single numpy array
        if isinstance(embeddings, np.ndarray):
            return embeddings.tolist()
        return embeddings

    def embed_image(self, image_path: str) -> List[float]:
        """
        Converts an image file into a vector embedding.
        """
        try:
            img = Image.open(image_path)
            embedding = self.model.encode(img)
            return embedding.tolist()
        except Exception as e:
            print(f"Error embedding image {image_path}: {e}")
            return []

if __name__ == "__main__":
    # Test
    model = EmbeddingModel()
    vec = model.embed_text("Hello world")
    print(f"Vector length: {len(vec)}") # Should be 512 for ViT-B-32