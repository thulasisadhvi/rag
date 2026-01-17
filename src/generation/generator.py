import os
import ollama
from typing import Dict, Any, List

class Generator:
    def __init__(self):
        """
        Initialize the local LLaVA model via Ollama.
        No API keys required!
        """
        self.model = "llava" 
        print(f"Generator ready using local model: {self.model}")

    def generate_answer(self, query: str, context: Dict[str, List[Any]]) -> str:
        """
        Generates a visually grounded answer using local LLaVA.
        """
        print("Generating answer with local LLaVA...")

        # 1. Collect Image Paths
        # LLaVA via Ollama is simple: you pass the text query and a list of image paths.
        image_paths = []
        for item in context.get('images', []):
            image_paths.append(item['metadata']['image_path'])

        # 2. Build the Text Prompt
        # We verify if we found any context
        if not context['text_chunks'] and not image_paths:
            return "I couldn't find any relevant information in the documents."

        context_text = ""
        for item in context.get('text_chunks', []):
            context_text += f"\n- {item['content']}\n"

        prompt = (
            f"You are a helpful assistant. Use the following context and images to answer the question.\n"
            f"Question: {query}\n\n"
            f"Context from documents:\n{context_text}\n\n"
            f"Instruction: Answer the question based on the text and the provided images."
        )

        # 3. Call the Local Model
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{
                    'role': 'user',
                    'content': prompt,
                    'images': image_paths # Ollama handles the file reading/encoding automatically!
                }]
            )
            return response['message']['content']
        except Exception as e:
            return f"Error generating answer: {e}"

if __name__ == "__main__":
    # Test
    gen = Generator()
    print("Generator initialized.")