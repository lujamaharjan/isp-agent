# ISP Chatbot & RAG System

A Retrieval-Augmented Generation (RAG) chatbot built for ISP-related queries, powered by a local LLM via **Ollama** and served through a **Chainlit** chat UI mounted inside **FastAPI**.

## About the Project

This project implements an ISP (Internet Service Provider) support chatbot using a RAG pipeline. It combines document retrieval with a locally-running LLM to answer user queries with context-aware, grounded responses — no external API calls, no data leaving your machine.

The chat interface is built with Chainlit and mounted as a sub-application inside FastAPI, allowing the same server to expose both the conversational UI and any additional REST endpoints.

## Features

- 🔍 Retrieval-augmented answers grounded in your own documents
- 💬 Chat UI via Chainlit, mounted inside a FastAPI app
- 🧠 Local LLM inference using Ollama (no cloud dependency)
- 🗂️ Vector search powered by ChromaDB
- 🔗 Orchestration with LangChain / LangGraph
- 🗃️ Lightweight persistence with SQLite

## Tech Stack

| Component      | Purpose                                  |
|----------------|-------------------------------------------|
| FastAPI        | Web server / API framework                |
| Chainlit       | Chat UI, mounted inside FastAPI           |
| SQLite         | Lightweight local data storage            |
| LangChain      | RAG pipeline components                   |
| LangGraph      | Agent / workflow orchestration            |
| Ollama         | Local LLM inference runtime               |
| ChromaDB       | Vector database for document retrieval    |

## Project Structure

```
.
├── app/                # FastAPI app + Chainlit mount
├── data/                # Source documents for the knowledge base
├── chroma_db/           # Persisted vector store (generated)
├── requirements.txt
└── README.md
```

> Update this section to match your actual folder layout.

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) installed locally
- Git

## Setup & Installation

### 1. Install Ollama

Download and install Ollama from [ollama.com](https://ollama.com), then pull the model used by this project:

```bash
ollama pull tinyllama
```

### 2. Clone the repository

```bash
git clone <your-repo-url>
cd <your-repo-name>
```

### 3. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the App

Make sure the Ollama service is running in the background, then start the FastAPI server (which mounts the Chainlit UI):

```bash
uvicorn app.main:app --reload
```

> Replace `app.main:app` with the actual module path to your FastAPI app instance.

Once running, open your browser at:

```
http://localhost:8000
```

## Usage

1. Start the app as described above.
2. Open the chat interface in your browser.
3. Ask questions related to ISP services — the system will retrieve relevant context from the knowledge base and generate an answer using the local LLM.

## Configuration

You may want to document any environment variables or config files here, for example:

```env
OLLAMA_MODEL=tinyllama
CHROMA_DB_PATH=./chroma_db
```

## Roadmap / Ideas

- [ ] Add support for additional Ollama models
- [ ] Improve document ingestion pipeline
- [ ] Add authentication
- [ ] Deploy with Docker

## License

Specify your license here (e.g. MIT).