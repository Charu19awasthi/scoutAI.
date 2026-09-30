# ScoutAI

https://scoutai-research-pla-w53j.bolt.host/


**Evidence-First AI Research & Data Intelligence Platform**

> "Ask a business question. Get a verified dataset."

## Problem

Turning a business question ("find me AI internships in India posted this
week") into a clean, trustworthy dataset today means manually searching,
copy-pasting into a spreadsheet, checking links by hand, and de-duplicating
rows — with no record of *why* any given row was included.

## Solution

ScoutAI takes a natural-language research requirement, uses an AI planner to
turn it into a structured, validated research plan, executes that plan
through deterministic backend code, and returns a searchable dataset where
**every single result carries its own evidence**: source, snippet, retrieval
time, requirement-match breakdown, and a verification status. Nothing is
marked "verified" because an LLM said so — only because backend validation
logic checked it.

## Features

- Natural-language requirement → structured AI research plan
- Deterministic, code-enforced plan validation (never blindly executes
  AI-generated instructions)
- Controlled, extensible data collection layer (ships with a safe bundled
  demo dataset; built to add permitted sources later)
- AI-assisted extraction with deterministic fallback
- Rule-based validation, confidence scoring, and status classification
  (`verified` / `review` / `invalid`)
- Conservative deduplication (won't merge unrelated companies with similar
  names)
- **Evidence-first**: every result has a "Why this result?" panel — source,
  snippet, timestamp, requirement match, verification status
- Live progress tracking while research runs
- Search / filter / sort / paginate results
- CSV and JSON export
- Full research history
- Works with **zero configuration** via Demo Mode — no Anthropic key
  required to see the full flow

## Architecture

See [`docs/architecture.md`](docs/architecture.md) for the full pipeline
diagram and design rationale. In short:

```
User prompt → AI Research Planner → Validated Plan → Controlled Collection
→ Extraction → Cleaning → Validation → Deduplication → Evidence → Database
→ Dashboard
```

The AI only ever produces a *plan* (structured JSON, validated by Pydantic
before use). All collection, validation, deduplication, evidence-attachment,
and persistence is deterministic application code.

## Technology stack

**Frontend:** React, Vite, Tailwind CSS, React Router, Lucide icons,
Recharts, Axios

**Backend:** Python, FastAPI, Pydantic, SQLAlchemy, SQLite (prototype;
Postgres-compatible), HTTPX, BeautifulSoup (for future permitted-source
collectors), Pandas

**AI:** Anthropic Claude, behind a provider-agnostic client
(`services/ai_client.py`) so another provider can be added later without
touching the rest of the app

## Folder structure

```
ScoutAI/
├── backend/
│   ├── app/
│   │   ├── main.py            FastAPI app, CORS, startup
│   │   ├── config.py          Settings (from .env)
│   │   ├── database.py        SQLAlchemy engine/session
│   │   ├── models/            ResearchTask, ResearchPlan, Result, Evidence
│   │   ├── schemas/           Pydantic request/response + AI-output schemas
│   │   ├── routes/            tasks, research, results, evidence, export
│   │   ├── services/          ai_client, ai_planner, ai_extractor,
│   │   │                      collector, validator, deduplicator,
│   │   │                      evidence_service, export_service,
│   │   │                      research_executor
│   │   └── utils/
│   ├── requirements.txt
│   ├── .env.example
│   └── .env                   (git-ignored; empty key = Demo Mode)
├── frontend/
│   └── src/
│       ├── pages/              Dashboard, NewResearch, Results, History,
│       │                       Datasets, EvidenceOverview, Settings
│       ├── components/         Sidebar, EvidencePanel, StatusBadge, Feedback
│       ├── layouts/            MainLayout
│       ├── services/api.js     The ONLY place the frontend talks to the backend
│       └── hooks/useTaskStatus.js
├── data/
│   ├── sample/internships.json   32 demo records (with intentional
│   │                              duplicates + incomplete records)
│   └── exports/
├── docs/
│   ├── architecture.md
│   └── api.md
└── README.md
```

## Setup

### Backend

```bash
cd backend

python -m venv venv
```

Activate the virtual environment:

- macOS/Linux: `source venv/bin/activate`
- Windows (PowerShell): `.\venv\Scripts\Activate.ps1`

Install dependencies:

```bash
pip install -r requirements.txt
```

Copy the environment template and (optionally) add your Anthropic key:

```bash
cp .env.example .env
```

Run the server:

```bash
uvicorn app.main:app --reload
```

The API is now live at `http://127.0.0.1:8000`, with interactive docs at
`http://127.0.0.1:8000/docs`. The SQLite database (`scoutai.db`) is created
automatically on first run.

### Frontend

```bash
cd frontend

npm install

npm run dev
```

Open `http://localhost:5173`.

### Claude setup (optional)

ScoutAI works out of the box in **Demo Mode** — no API key required. To
enable live Claude-powered planning, set in `backend/.env`:

```env
ANTHROPIC_API_KEY=your_real_key_here
ANTHROPIC_MODEL=claude-sonnet-4-5
```

Restart the backend. The Settings page and sidebar will show
"AI Engine: Connected" once a key is detected.

### Demo Mode

If `ANTHROPIC_API_KEY` is left blank, ScoutAI automatically uses a
deterministic demo planner and the bundled sample dataset
(`data/sample/internships.json`) — the full flow (prompt → plan → run →
results → evidence → export) works with zero network dependency, so a live
demo never fails because of an API or connectivity issue. The UI labels
this clearly as **Demo Mode**.

## Deploying

See [`DEPLOYMENT.md`](DEPLOYMENT.md) for step-by-step instructions to
deploy the backend to Render (free tier) and the frontend to Vercel or
Netlify (free static hosting), including a one-click `render.yaml`
blueprint.

## API documentation

See [`docs/api.md`](docs/api.md) for the full endpoint reference, or browse
`http://127.0.0.1:8000/docs` while the backend is running.

## Demo flow

1. Open ScoutAI → **New Research**
2. Enter: *"Find AI/ML internships in India posted within the last 7 days.
   Prefer startups and remote/hybrid roles. Extract company, role,
   location, skills, stipend, posting date and application link."*
3. Click **Generate Research Plan**
4. Review the structured plan → **Start Research**
5. Watch live pipeline progress (collection → extraction → validation →
   deduplication → evidence)
6. Browse results: search, filter by status/confidence, sort, paginate
7. Click a result → see **Why this result?** and its full evidence panel
8. Export the dataset as CSV or JSON

## Screenshots

_Add screenshots of the Dashboard, New Research flow, Results table, and
Evidence panel here once you've run the app locally._

## Future improvements

- Real permitted-source collectors (public APIs/feeds) behind the existing
  `BaseCollector` interface
- WebSocket-based live progress instead of polling
- PostgreSQL for multi-user production deployments
- Additional research intents beyond internship discovery (sales leads,
  sponsor discovery, competitor pricing, market research — the data model
  is already intent-agnostic: `ResearchTask` / `ResearchPlan` / `Result` /
  `Evidence`, not `InternshipTask`)
- Pluggable AI providers (OpenAI, Gemini) behind `services/ai_client.py`
- Authentication and per-user research history
