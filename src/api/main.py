from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os

# Import our custom modules
from src.retrieval.retriever import Retriever
from src.generation.generator import Generator

app = FastAPI(title="Multimodal RAG API")

# Initialize modules (Load models once on startup to save time)
print("Initializing RAG pipeline...")
retriever = Retriever()
generator = Generator()
print("Pipeline ready.")

# --- Pydantic Models for Input/Output Validation ---

class QueryRequest(BaseModel):
    query: str

class Source(BaseModel):
    document_id: str
    page_number: int
    content_type: str
    snippet: str # Text snippet or Image path

class QueryResponse(BaseModel):
    answer: str
    sources: List[Source]

# --- API Endpoints ---

@app.post("/query", response_model=QueryResponse)
async def query_rag_system(request: QueryRequest):
    """
    Main endpoint:
    1. Receives text query.
    2. Retrieves relevant images and text.
    3. Generates an answer using VLM.
    4. Returns answer + sources.
    """
    try:
        # Step 1: Retrieve Context
        # We ask for top 3 chunks to keep context concise for the VLM
        context = retriever.retrieve(request.query, top_k=5)
        
        # Step 2: Generate Answer
        answer = generator.generate_answer(request.query, context)
        
        # Step 3: Format Sources for Response
        # We need to combine text and images back into a single list of sources
        response_sources = []
        
        # Add text sources
        for item in context.get('text_chunks', []):
            response_sources.append(Source(
                document_id=item['metadata']['filename'],
                page_number=item['metadata']['page_number'],
                content_type="text",
                snippet=item['content'][:200] + "..." # Truncate for display
            ))
            
        # Add image sources
        for item in context.get('images', []):
            response_sources.append(Source(
                document_id=item['metadata']['filename'],
                page_number=item['metadata']['page_number'],
                content_type="image",
                snippet=item['metadata']['image_path'] # Return path to the image
            ))

        return QueryResponse(answer=answer, sources=response_sources)

    except Exception as e:
        print(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "active"}

if __name__ == "__main__":
    # Run the server
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)