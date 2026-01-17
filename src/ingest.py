import os
from src.ingestion.document_parser import DocumentParser
from src.ingestion.image_processor import ImageProcessor
from src.embeddings.model_loader import EmbeddingModel
from src.vector_store.chroma_manager import ChromaManager

def main():
    # 1. Setup
    DATA_DIR = "sample_documents"
    db = ChromaManager()
    embedder = EmbeddingModel()
    pdf_parser = DocumentParser()
    img_processor = ImageProcessor()

    print(f"🚀 Starting ingestion from {DATA_DIR}...")

    # 2. Iterate through files
    for filename in os.listdir(DATA_DIR):
        filepath = os.path.join(DATA_DIR, filename)
        
        extracted_chunks = []

        # A. Handle PDFs
        if filename.endswith(".pdf"):
            print(f"Processing PDF: {filename}")
            extracted_chunks = pdf_parser.parse_pdf(filepath)

        # B. Handle Images
        elif filename.endswith((".png", ".jpg", ".jpeg")):
            print(f"Processing Image: {filename}")
            result = img_processor.process_image(filepath)
            if result:
                extracted_chunks = [result]

        # 3. Embed and Store
        if extracted_chunks:
            # Prepare lists for batch insertion
            texts_to_embed = [] # This will be text OR image descriptions
            metadatas = []
            ids = []

            for chunk in extracted_chunks:
                # For images, we embed the 'content' (which might be OCR text or a placeholder)
                # In a real VLM app, you might use a specific Image Embedding model here.
                # For this assignment using CLIP, we can embed the images directly if supported,
                # OR embed the text description. 
                
                # IMPORTANT: If chunk is image, use embed_image, else embed_text
                if chunk['type'] == 'image':
                    # Embed the actual image pixels using CLIP
                    vector = embedder.embed_image(chunk['metadata'].get('image_path') or chunk['image_path'])
                    # For the document text stored in DB, we use "Image: [filename]" as a placeholder
                    doc_text = f"Image content from {filename}" 
                else:
                    # Embed the text
                    vector = embedder.embed_text(chunk['content'])
                    doc_text = chunk['content']

                if vector:
                    db.add_data(
                        embeddings=[vector],
                        documents=[doc_text],
                        metadatas=[chunk['metadata']]
                    )
            
            print(f"Saved {len(extracted_chunks)} chunks from {filename}")

    print("✅ Ingestion Complete!")

if __name__ == "__main__":
    main()