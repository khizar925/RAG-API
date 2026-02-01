from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import chromadb
import ollama
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://rag-chat-ai-webapp.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)

chroma = chromadb.PersistentClient(path="./db")
collection = chroma.get_or_create_collection("docs")


def generate_stream(q: str, chat_id: str, user_id: str):
    context = ""

    try:
        results = collection.query(
            query_texts=[q],
            n_results=1,
            where={
                "$and": [
                    {"chat_id": chat_id},
                    {"user_id": user_id}
                ]
            }
        )
        if results["documents"] and results["documents"][0]:
            context = results["documents"][0][0]
    except Exception:
        context = ""

    if context:
        prompt = f"Context:\n{context}\n\nQuestion: {q}\n\nAnswer clearly and concisely based on the context above:"
    else:
        prompt = f"Question: {q}\n\nAnswer clearly and concisely:"

    for chunk in ollama.generate(
        model="qwen2.5-coder:1.5b",
        prompt=prompt,
        stream=True,
        options={"num_predict": 150}
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
        import uuid
        doc_id = str(uuid.uuid4())

        collection.add(
            documents=[text],
            ids=[doc_id],
            metadatas=[{"chat_id": chat_id, "user_id": user_id}]
        )

        return {
            "status": "success",
            "message": "Content added to knowledge base",
            "id": doc_id
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }