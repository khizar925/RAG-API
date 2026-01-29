<img src="https://cdn.prod.website-files.com/677c400686e724409a5a7409/6790ad949cf622dc8dcd9fe4_nextwork-logo-leather.svg" alt="NextWork" width="300" />

# Build a RAG API with FastAPI

**Project Link:** [View Project](http://learn.nextwork.org/projects/ai-devops-api)

**Author:** Khizar Qamar  
**Email:** khizarqamar06@gmail.com

---

![Image](http://learn.nextwork.org/glowing_magenta_quiet_crab/uploads/ai-devops-api_g3h4i5j6)

---

## Introducing Today's Project!

In this project, I demonstrate how to build a Retrieval-Augmented Generation (RAG) API from scratch using FastAPI. I chose this project to learn how RAG works, how to use ChromaDB for vector search, integrate a local LLM with Ollama, and run the entire system locally for free.

### Key services and concepts

Services I used were Ollama, FastAPI, and ChromaDB to manage the AI model, web interface, and vector storage. Key concepts I learnt include RAG (Retrieval-Augmented Generation), generating text embeddings for semantic search, and building RESTful APIs to connect private data with local LLMs.

### Challenges and wins

This project took me approximately two hours. The most challenging part was understanding how text embeddings are mathematically mapped to enable accurate semantic search. It was most rewarding to see the API successfully retrieve specific facts from my documents and generate precise, context-aware answers.

### Why I did this project

I did this project because I wanted to gain hands-on experience in bridging the gap between AI development and backend engineering by building a functional RAG system

---

## Setting Up Python and Ollama

In this step, I'm setting up Python and Ollama. Python is the main programming language used to build the backend API and handle logic such as request processing, embeddings, and interaction with the vector database that I am using to build the RAG API. Ollama is used to run large language models locally, allowing me to perform inference without relying on paid cloud APIs. I need these tools because Python provides a rich ecosystem of libraries (such as FastAPI and vector database clients) to implement the RAG pipeline, while Ollama enables cost-free, local model execution for retrieval-augmented generation.

### Python and Ollama setup

![Image](http://learn.nextwork.org/glowing_magenta_quiet_crab/uploads/ai-devops-api_i9j0k1l2)

### Verifying Python is working

### Ollama and tinyllama ready

Ollama is an open-source tool for running large language models locally on your machine, and I downloaded the tinyllama model because its compact 1.1 billion parameter size allows it to run quickly and efficiently on standard hardware without high resource costs. This model will help my RAG API by acting as the primary engine that synthesizes retrieved context and user queries into coherent, natural language responses.

---

## Setting Up a Python Workspace

In this step, I'm setting up my local development environment by creating a project folder, initializing a Python virtual environment, and installing necessary dependencies. I need it because it ensures a clean, isolated workspace where my project’s specific libraries can run consistently and reliably without interfering with other system configurations.

### Python workspace setup

### Virtual environment

A virtual environment is an isolated workspace that keeps a project's Python libraries separate from the rest of the system. I created one for this project to prevent version conflicts and ensure that the specific dependencies needed for the RAG API remain organized. Once I activate it, the terminal will prioritize the local libraries within that environment, and to create one, I used the "python -m venv venv command to build the necessary local directory.

### Dependencies

The packages I installed include FastAPI, ChromaDB, Uvicorn, and Ollama. FastAPI is used for creating the web API and managing the endpoints that receive user queries. Chroma is used for storing and searching through document embeddings as a vector database, ensuring the AI has the right context. Uvicorn is used for acting as the lightning-fast web server that actually runs the FastAPI application. Ollama is used for handling the communication with your local LLM to generate the final natural language response.

![Image](http://learn.nextwork.org/glowing_magenta_quiet_crab/uploads/ai-devops-api_u1v2w3x4)

---

## Setting Up a Knowledge Base

In this step, I’m creating a knowledge base by writing my own content and turning it into embeddings so the AI can search through it.
A knowledge base is a collection of information that the AI uses to find accurate answers instead of guessing.
I need it because it allows my RAG system to respond based on real data that I provide, making the answers more reliable and relevant.

### Knowledge base setup

![Image](http://learn.nextwork.org/glowing_magenta_quiet_crab/uploads/ai-devops-api_t1u2v3w4)

### Embeddings created

Embeddings are numerical representations of text that capture its meaning as a list of numbers. I created them by using a processing script to convert my documents into a format that a computer can mathematically compare. The db/ folder contains the persistent vector database where these numerical representations are stored for quick access. This is important for RAG because it allows the system to instantly find the most relevant pieces of information from my documents to provide as context for the AI's answers.

---

## Building the RAG API

In this step, I'm building a RAG API by writing the core application code and launching the local server. An API is a bridge that allows different software programs to talk to each other, while FastAPI is a high-performance framework that makes it easy to build these bridges using Python. I'm creating this because it provides a functional interface where I can send questions and receive AI-generated answers based on my specific knowledge base.

### FastAPI setup

### How the RAG API works

My RAG API works by sending a question to the API at the endpoint "/query". Next Chroma DB searches the Knowledge Base to match with the questions meaning. Chroma returns the most relevant information from the documents. The question and the matching text are sent together to tinyllama, which creates an answer. Then the answer is returned at th endpoint.

![Image](http://learn.nextwork.org/glowing_magenta_quiet_crab/uploads/ai-devops-api_f3g4h5i6)

---

## Testing the RAG API

In this step, I'm testing my RAG API. I'll test it using Swagger UI. Swagger UI is an automatically generated, interactive documentation page for the FastAPI Server. I'll use it to visually explore the API Endpoints to see which parameter is accepted.

### Testing the API

### API query breakdown

I queried my API by running the Linux command curl -X POST "http://127.0.0.1:8000/query" -G --data-urlencode "q=What is Kubernetes?". The command uses the POST method, which means I am sending data—in this case, my question—to the server to be processed rather than just requesting a static page. The API responded with the results of the query that it gets from running the tinyllama AI Model.

![Image](http://learn.nextwork.org/glowing_magenta_quiet_crab/uploads/ai-devops-api_g3h4i5j6)

### Swagger UI exploration

Swagger UI is an interactive, web-based interface that automatically documents and visualizes API endpoints. I used it to test the /query endpoint by providing the parameter "q" containing my question and clicking the "Execute" button. The best part about using Swagger UI was that it allowed me to interact with my API instantly in the browser without writing any extra frontend code or complex command-line arguments.

---

## Adding Dynamic Content

In this project extension, I'm am creating an API Endpoint called /add that lets  me dynamically addd content to the Knowledge base, that means i dont make to manually edit k8s.txt and rerun the embed.py and rather I will create a endpoint where users will add information through the web interface without manual interventions. 

### Adding the /add endpoint

![Image](http://learn.nextwork.org/glowing_magenta_quiet_crab/uploads/ai-devops-api_w9x0y1z2)

### Dynamic content endpoint working

The /add endpoint allows me to dynamically insert new text or documents into the ChromaDB vector store. This is useful because it makes the knowledge base dynamic, allowing the system to learn and retrieve fresh information in real-time without the need to manually re-run the initial setup scripts or restart the entire API.

---

---
