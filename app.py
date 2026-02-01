from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import chromadb
import ollama
import uuid
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://rag-chat-ai-webapp.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)

chroma = chromadb.PersistentClient(path="./db")
collection = chroma.get_or_create_collection("docs")


def chunk_text(text, chunk_size=1000, overlap=100):
    """Split text into overlapping chunks."""
    if not text:
        return []
        
    chunks = []
    start = 0
    text_len = len(text)
    
    while start < text_len:
        end = start + chunk_size
        chunks.append(text[start:end])
        # Move start forward, but minus overlap to keep context
        start += chunk_size - overlap
    
    return chunks


def generate_stream(q: str, chat_id: str, user_id: str):
    context = ""

    try:
        # Retrieve top 3 relevant chunks instead of 1
        results = collection.query(
            query_texts=[q],
            n_results=3,
            where={
                "$and": [
                    {"chat_id": chat_id},
                    {"user_id": user_id}
                ]
            }
        )
        
        if results["documents"] and results["documents"][0]:
            # Join multiple chunks to form context
            context = "\n---\n".join(results["documents"][0])
    except Exception as e:
        print(f"Error querying database: {e}")
        context = ""

    if context:
        prompt = f"Context:\n{context}\n\nQuestion: {q}\n\nAnswer clearly and concisely based on the context above:"
    else:
        prompt = f"Question: {q}\n\nAnswer clearly and concisely:"

    for chunk in ollama.generate(
        model="qwen2.5-coder:1.5b",
        prompt=prompt,
        stream=True,
        options={"num_predict": 300}
    ):
        yield chunk["response"]


@app.post("/query")
def query(q: str, chat_id: str, user_id: str):
    return StreamingResponse(
        generate_stream(q, chat_id, user_id),
        media_type="text/plain"
    )


@app.post("/add")
def add_knowledge(text: str, chat_id: str, user_id: str):
    """Add new content to the knowledge base dynamically."""
    try:
        chunks = chunk_text(text)
        
        if not chunks:
             return {
                "status": "error",
                "message": "Text is empty or could not be chunked"
            }

        ids = [str(uuid.uuid4()) for _ in chunks]
        metadatas = [{"chat_id": chat_id, "user_id": user_id} for _ in chunks]

        collection.add(
            documents=chunks,
            ids=ids,
            metadatas=metadatas
        )

        return {
            "status": "success",
            "message": f"Content added to knowledge base ({len(chunks)} chunks)",
            "ids": ids
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )
