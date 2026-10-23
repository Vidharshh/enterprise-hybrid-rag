# Enterprise Hybrid RAG Platform

An enterprise-oriented hybrid retrieval-augmented generation (RAG) research agent. It combines PostgreSQL for structured data, Qdrant for vector retrieval, Neo4j for knowledge-graph exploration, and Redis for caching and routing. The Python agent runs locally; Groq hosts the LLM inference workload.

This design avoids running large Llama models on the MacBook, where local inference caused the machine to freeze. Local embedding generation can be added independently, subject to available hardware.

> **Project status:** This README describes the intended stack and initial setup. Confirm repository files, service names, model availability, and test scripts against the implementation as it is built.

## Architecture

```text
                    ┌──────────────────────────┐
                    │ Local Python research    │
                    │ agent and orchestrator   │
                    └────────────┬─────────────┘
                                 │
              ┌──────────────────┼────────────────────┐
              │                  │                    │
       ┌──────▼──────┐    ┌──────▼──────┐      ┌──────▼──────┐
       │ PostgreSQL  │    │   Qdrant    │      │   Neo4j     │
       │ structured  │    │ semantic    │      │ entities &  │
       │ records     │    │ retrieval   │      │ relations   │
       └─────────────┘    └─────────────┘      └─────────────┘
              │                  │                    │
              └──────────────────┴────────────────────┘
                                 │
                           ┌─────▼─────┐
                           │  Redis    │
                           │ cache /   │
                           │ routing   │
                           └───────────┘

              Python agent ───── HTTPS ─────► Groq API
                                             LLM inference
```

The agent coordinates retrieval across the local data services and sends relevant context to Groq for generation. The databases and orchestration remain under local development control. Requests sent to Groq leave the machine, so only send data that is appropriate for the configured provider and account.

### Service responsibilities

| Component | Responsibility | Local endpoint (default) |
| --- | --- | --- |
| Python agent | Query routing, retrieval orchestration, evidence handling, answer generation | Local process |
| PostgreSQL | Structured records and SQL retrieval | `localhost:5432` |
| Qdrant | Dense vector search over embedded chunks | `localhost:6333` (dashboard: `http://localhost:6333/dashboard`) |
| Neo4j | Entity and relationship queries | Bolt: `localhost:7687`; Browser: `http://localhost:7474` |
| Redis | Query, result, or embedding cache, as implemented | `localhost:6379` |
| Groq API | Hosted LLM inference | `https://api.groq.com` |

## Prerequisites

- macOS, Linux, or Windows with WSL2/PowerShell
- Git
- Docker Desktop or Docker Engine with Compose
- Python 3.9 or later (use the version required by the project's dependencies if it is higher)
- A Groq account and API key from the [Groq Console](https://console.groq.com/)

## Setup

### 1. Get the project and create a virtual environment

Clone the repository if it is hosted remotely, then enter its directory:

```bash
git clone https://github.com/Vidharshh/enterprise-hybrid-rag.git enterprise-hybrid-rag
cd enterprise-hybrid-rag
```

For a repository already on your machine, enter its root directory instead. Create and activate a virtual environment:

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

```powershell
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

```cmd
:: Windows Command Prompt
python -m venv .venv
.venv\Scripts\activate.bat
```

### 2. Install Python dependencies

If the repository includes `requirements.txt`:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Install the Groq Python SDK if it is not already listed by the project:

```bash
python -m pip install groq
```

### 3. Configure environment variables

Copy the sample file if the repository provides one:

```bash
# macOS / Linux
cp .env.example .env
```

```powershell
# Windows PowerShell
Copy-Item .env.example .env
```

Set the key and service settings in `.env`. Adjust database names, passwords, ports, and model to match the actual compose and application configuration.

```dotenv
# Groq Cloud API
GROQ_API_KEY=gsk_replace_with_your_groq_api_key
LLM_MODEL=openai/gpt-oss-120b

# PostgreSQL
POSTGRES_DB=olist
POSTGRES_USER=postgres
POSTGRES_PASSWORD=replace_with_a_local_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Qdrant
QDRANT_HOST=localhost
QDRANT_PORT=6333

# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=replace_with_a_local_password

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
```

The model name above is an example from the referenced setup. Check [Groq's supported models](https://console.groq.com/docs/models) for currently available IDs and use a model compatible with the API features your agent needs.

### 4. Start the local data services

From the directory containing `compose.yaml` or `docker-compose.yml`:

```bash
docker compose up -d
docker compose ps
```

Wait for the services to become healthy before starting the agent. The local ports shown above are defaults; the Compose file is authoritative.

### 5. Check Groq connectivity

If the project supplies a connection-check script, run it from the repository root with the virtual environment active. The pasted project draft refers to:

```bash
python test_groq.py
```

That script should make a small request using `GROQ_API_KEY` and report the selected model. If the script does not exist yet, use the [Groq quickstart](https://console.groq.com/docs/quickstart) to make a minimal chat completion, or add a project-specific smoke check.

### 6. Run the research agent

Run the project's documented entry point after configuring the data stores and loading the required data. The exact command depends on the implementation; for example, a project may provide a CLI, notebook, or application module. Check the repository's source and project scripts for the supported command.

## Git and secret handling

Before the first commit, verify that `.env`, virtual environments, caches, and local data are ignored. A starter `.gitignore` should include at least:

```gitignore
.env
.venv/
venv/
__pycache__/
*.py[cod]
.pytest_cache/
```

Keep a `.env.example` with placeholder values, never real credentials. Do not paste API keys into source code, notebooks, logs, commits, screenshots, or issue reports. If a key is exposed, revoke it in the Groq Console and create a replacement. For shared or deployed environments, use the hosting platform's secret manager rather than committing a `.env` file.

To create a GitHub remote, create an empty repository and then run:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<your-username>/enterprise-hybrid-rag.git
git push -u origin main
```

Replace the remote URL with your own. Inspect staged files before committing (`git status` and `git diff --cached`) to make sure secrets and private data are excluded.

## Research quality: verification and evidence grounding

The primary evaluation goal is a well-supported answer, not merely a fluent one. For each response, the agent should:

- Retrieve evidence from the relevant stores and retain source identifiers, document locations, or record keys.
- Separate retrieved facts from model-generated interpretation.
- Tie material claims to specific evidence so a reader can check them.
- Say when evidence is missing, conflicting, stale, or insufficient; avoid filling gaps with unsupported claims.
- Verify structured values against PostgreSQL results and graph relationships against Neo4j results rather than trusting a generated summary.
- Measure retrieval quality and answer quality separately. Useful checks include retrieval recall/precision on labeled questions, claim-level support rate, citation correctness, contradiction handling, and abstention when evidence is inadequate.
- Maintain a small regression set of research questions with expected source records and supported claims; rerun it when prompts, chunking, indexes, routing, or models change.

Treat LLM output as a hypothesis that needs evidence. A successful API response or a plausible answer is not proof that the answer is correct.

## Provider-agnostic design

Keep provider-specific code behind a small inference interface, such as `generate(messages, model, options)`. The application should own prompt construction, retrieval, evidence checks, and evaluation; a provider adapter should own authentication, request formatting, and provider errors.

Read the provider and model from configuration, and normalize responses and errors into application-level types. This keeps the retrieval pipeline independent of Groq and makes it possible to evaluate another hosted or local provider later without rewriting orchestration. Do not assume every provider supports identical tool calling, structured output, context sizes, or rate limits.

## Rate limits and free-tier notes

Groq offers a free plan, but availability and limits depend on the model, account, and current plan. Limits can cover requests and tokens across minute/day windows, and the first limit reached can throttle the workload. Do not rely on fixed request-per-day numbers from older guides. Check the [official rate limits page](https://console.groq.com/docs/rate-limits) and the limits shown for your own organization before estimating capacity.

When handling throttling:

- Detect HTTP `429` responses and respect `Retry-After` when present.
- Add bounded exponential backoff with jitter; avoid unbounded retries.
- Limit concurrency and batch or cache repeated work where appropriate.
- Record request IDs and usage metadata without logging secrets or sensitive prompt contents.
- Make evaluation scripts resumable so a limit does not waste completed work.

See Groq's [API error guide](https://console.groq.com/docs/errors) for current error behavior. A free tier should be treated as suitable for development and experimentation, not as a guaranteed production capacity or service-level commitment.

## Troubleshooting

| Symptom | Things to check |
| --- | --- |
| `GROQ_API_KEY` missing or authentication fails | Confirm `.env` is at the expected path, the application loads it, the key is active, and the environment variable name is exactly `GROQ_API_KEY`. Never print the key while debugging. |
| Groq returns `429` | Check account/model limits, reduce request rate or concurrency, and use bounded backoff honoring `Retry-After`. |
| Model not found or unsupported | Check the current [supported models](https://console.groq.com/docs/models) list, model ID spelling, and endpoint compatibility. |
| Docker services are unavailable | Confirm Docker is running, inspect `docker compose ps` and service logs, and check for local port conflicts or mismatched credentials. |
| Python cannot connect to a service | Verify host, port, credentials, and whether the application runs on the host or inside Docker. A container may need the Compose service name rather than `localhost`. |
| VS Code reports missing Python imports | Select the project's `.venv` interpreter, then reload the editor window. |
| Agent answers without evidence | Inspect retrieval results, source metadata, prompt constraints, and claim verification. Do not treat a successful model call as evidence. |

## Roadmap

1. **Document ingestion and embeddings:** chunk source material, preserve source metadata, generate embeddings, and index the chunks in Qdrant. The referenced plan uses local `sentence-transformers` embeddings; this workload can be configured separately from cloud LLM inference.
2. **Knowledge graph modeling:** define entities and relationships and load them into Neo4j with traceable source references.
3. **Hybrid query orchestration:** route appropriate questions to PostgreSQL, Qdrant, and Neo4j, then combine results with explicit provenance.
4. **Evaluation and iteration:** build labeled research questions and measure retrieval, claim support, citation accuracy, conflict handling, and abstention.

## References

- [Groq Quickstart](https://console.groq.com/docs/quickstart)
- [Groq Supported Models](https://console.groq.com/docs/models)
- [Groq Rate Limits](https://console.groq.com/docs/rate-limits)
- [Groq API Errors](https://console.groq.com/docs/errors)
- [Groq API Reference](https://console.groq.com/docs/api-reference)
