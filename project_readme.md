# Enterprise Hybrid RAG Platform

An enterprise-grade Hybrid Retrieval-Augmented Generation (RAG) platform combining structured SQL query execution (PostgreSQL), dense vector search (Qdrant), knowledge graphs (Neo4j), and multi-turn cache routing (Redis), powered by Groq cloud LLM inference.

## 🛠️ Prerequisites & System Requirements

Before starting, ensure you have the following software installed on your machine:

1. **Operating System**: macOS, Linux (Ubuntu/Debian/Fedora), or Windows 10/11 (with WSL2 or PowerShell).
2. **Docker Desktop / Docker Engine**: Required to run containerized databases (PostgreSQL, Qdrant, Neo4j, Redis).
   * Download: [Docker Desktop](https://www.docker.com/products/docker-desktop/)
3. **Python**: Python 3.9+ installed locally.
4. **Groq API Key**: Active API key from [Groq Console](https://console.groq.com/).

---

## 🚀 Quickstart & Setup Guide

### Step 1: Clone the Repository & Set Up Virtual Environment

#### macOS / Linux
```bash
# 1. Open terminal and navigate to your workspace
cd enterprise-hybrid-rag

# 2. Create Python virtual environment
python3 -m venv venv

# 3. Activate the virtual environment
source venv/bin/activate
```

#### Windows (PowerShell)
```powershell
# 1. Open PowerShell and navigate to your workspace
cd enterprise-hybrid-rag

# 2. Create Python virtual environment
python -m venv venv

# 3. Activate the virtual environment
# (If execution is blocked, run: Set-ExecutionPolicy Unrestricted -Scope Process)
.\venv\Scripts\Activate.ps1
```

#### Windows (Command Prompt)
```cmd
cd enterprise-hybrid-rag
python -m venv venv
.\venv\Scripts\activate.bat
```

---

### Step 2: Install Dependencies

With your virtual environment activated, install all required dependencies (using an increased timeout to handle larger packages like PyTorch):

```bash
pip install --upgrade pip
pip install --default-timeout=1000 -r requirements.txt
```

---

### Step 3: Configure Environment Variables (`.env`)

Create a `.env` file in the project root folder:

* **macOS / Linux**: `cp .env.example .env`
* **Windows (PowerShell)**: `Copy-Item .env.example .env`

Ensure your `.env` contains the following configuration:

```env
# ==========================================
# Groq Cloud API
# ==========================================
GROQ_API_KEY=your_actual_groq_api_key_here
LLM_MODEL=openai/gpt-oss-120b

# ==========================================
# Local Infrastructure Containers
# ==========================================
POSTGRES_DB=olist
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

QDRANT_HOST=localhost
QDRANT_PORT=6333

NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password

REDIS_HOST=localhost
REDIS_PORT=6379
```

---

### Step 4: Spin Up Infrastructure Containers

Ensure Docker Desktop / Engine is running, then start the container stack:

```bash
docker compose up -d
```

Verify that all containers are healthy:

```bash
docker compose ps
```

| Container | Service | Local Port / Interface |
| :--- | :--- | :--- |
| `postgres` | Relational Store (Olist Dataset) | `localhost:5432` |
| `qdrant` | Vector Database | `localhost:6333` (UI: `http://localhost:6333/dashboard`) |
| `neo4j` | Knowledge Graph | `localhost:7687` (Browser: `http://localhost:7474`) |
| `redis` | Query & Embedding Cache | `localhost:6379` |

---

### Step 5: Verify LLM Connection

Run the Groq cloud verification test script to confirm API key access and inference readiness:

```bash
python test_groq.py
```

Expected output:
```text
Testing primary LLM model: 'openai/gpt-oss-120b'...

✅ Primary LLM Test Successful!
Active Model: openai/gpt-oss-120b
Response: Yes—I’m connected and ready to serve as the primary language model...
```

---

## 🏗️ Phase 2 Roadmap: Vector Embeddings & Hybrid Search

Now that Phase 1 infrastructure and cloud connections are verified, you are ready to begin **Phase 2**:

1. **Document Chunking & Vector Ingestion**:
   * Utilize `sentence-transformers` to generate embeddings locally.
   * Create and configure Qdrant collections for product catalog search.
2. **Knowledge Graph Modeling (Neo4j)**:
   * Build graph relationships between customer orders, product categories, and sellers.
3. **Hybrid Query Orchestration**:
   * Implement query routing between PostgreSQL (SQL), Qdrant (Dense Vector), and Neo4j (Graph).

---

### 💡 VS Code Configuration Tip

If you encounter `reportMissingImports` warnings in VS Code:
1. Press `Cmd + Shift + P` (macOS) or `Ctrl + Shift + P` (Windows/Linux) $\rightarrow$ **Python: Select Interpreter**.
2. Select `./venv/bin/python` (macOS/Linux) or `.\venv\Scripts\python.exe` (Windows).
3. Open Command Palette $\rightarrow$ **Developer: Reload Window**.