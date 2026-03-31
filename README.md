# 🔍 CodeReview Agent

> AI-powered code reviewer — submit code snippets, get structured feedback with bug detection, severity ratings, and refactored suggestions.

Built with [Google ADK](https://google.github.io/adk-docs/) + Gemini 2.5 Flash, deployed on Google Cloud Run.

---

## How it works

```
POST /review  →  ADK Runner  →  Gemini 2.5 Flash  →  Structured JSON review
```

1. You send a code snippet (any language)
2. The ADK agent prompts Gemini with a strict Pydantic output schema
3. You get back a structured code review with issues, severity, and fixes

---

## Output schema

| Field | Type | Description |
|---|---|---|
| `summary` | `string` | 2-3 sentence overall assessment |
| `language_detected` | `string` | Detected programming language |
| `issues` | `CodeIssue[]` | List of issues found (see below) |
| `score` | `A \| B \| C \| D \| F` | Overall code quality grade |
| `refactored_snippet` | `string` | Refactored version of the most critical section |

### CodeIssue schema

| Field | Type | Description |
|---|---|---|
| `line_reference` | `string` | The specific line or snippet with the issue |
| `severity` | `Critical \| Warning \| Info` | Issue severity level |
| `category` | `Bug \| Security \| Performance \| Readability \| Best Practice` | Issue category |
| `description` | `string` | Why this is a problem |
| `suggestion` | `string` | Specific fix with corrected code |

---

## Local setup

**Prerequisites:** Python 3.12+, a Gemini API key

```bash
git clone https://github.com/rajatguptaa/code-review.git
cd code-review

python3 -m venv venv            # Windows: python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

export GOOGLE_API_KEY="your_api_key_here"   # Windows: set GOOGLE_API_KEY=your_api_key_here
python server.py
```

Server and UI run at `http://localhost:8080`
Interactive API docs at `http://localhost:8080/docs`

---

## ADK Dev UI

You can also test the agent interactively using the built-in ADK Dev UI:

```bash
adk web
```

This launches a local web interface at `http://localhost:8000` where you can chat with the agent directly.

---

## Deploy to Cloud Run

### Option 1: Manual Deployment (gcloud CLI)

```bash
gcloud run deploy code-review-agent \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="GOOGLE_API_KEY=your_api_key_here"
```

### Option 2: CI/CD via GitHub Actions

This repository includes a reusable GitHub Actions workflow for building and deploying to Google Cloud Run automatically on pushes to `main`.

1. Review the configuration at `.github/workflows/deploy-cloud-run.yml`.
2. Update the environment variables (`PROJECT_ID`, `REGION`, `GAR_LOCATION`, `SERVICE`).
3. Create a GitHub Secret with your `GCP_CREDENTIALS` (Service Account JSON) or set up Workload Identity Federation as described in the workflow.

---

## Usage

**Linux / macOS**
```bash
curl -X POST "https://YOUR_SERVICE_URL/review" \
  -H "Content-Type: application/json" \
  -d '{"code": "def calc(x):\n  result = x / 0\n  passwords = [\"admin123\"]\n  return result"}'
```

**Windows CMD**
```cmd
curl -X POST "https://YOUR_SERVICE_URL/review" -H "Content-Type: application/json" -d "{\"code\": \"def calc(x):\\n  result = x / 0\\n  passwords = [\\\"admin123\\\"]\\n  return result\"}"
```

**Example response**
```json
{
  "summary": "The code contains a critical division by zero bug and a severe security vulnerability with hardcoded passwords. Immediate fixes required.",
  "language_detected": "Python",
  "issues": [
    {
      "line_reference": "result = x / 0",
      "severity": "Critical",
      "category": "Bug",
      "description": "Division by zero will cause a ZeroDivisionError at runtime.",
      "suggestion": "Add a guard: 'if divisor != 0: result = x / divisor' or use a try-except block."
    },
    {
      "line_reference": "passwords = [\"admin123\"]",
      "severity": "Critical",
      "category": "Security",
      "description": "Hardcoded passwords in source code is a severe security vulnerability.",
      "suggestion": "Use environment variables or a secrets manager: os.environ.get('PASSWORD')"
    }
  ],
  "score": "F",
  "refactored_snippet": "import os\n\ndef calc(x, divisor):\n    if divisor == 0:\n        raise ValueError('Divisor cannot be zero')\n    return x / divisor"
}
```

Interactive API docs available at `/docs`.

---

## Tech stack

| Component | Technology |
|-----------|-----------|
| Agent Framework | [Google ADK](https://google.github.io/adk-docs/) |
| LLM | Gemini 2.5 Flash |
| Web Server | FastAPI + Uvicorn |
| Deployment | Google Cloud Run |
| Container | Docker (Python 3.12-slim) |

---

## Project structure

```
code-review/
├── agent.py          # ADK Agent definition with Gemini model & prompt
├── schemas.py        # Pydantic output schemas (CodeReview, CodeIssue)
├── server.py         # FastAPI REST API with ADK Runner
├── requirements.txt  # Python dependencies
├── Dockerfile        # Cloud Run container config
└── README.md
```

---

## Inspired by

- [KiranAyyagari/story-weaver](https://github.com/KiranAyyagari/story-weaver) — AI-Powered Agile Ticket Refiner using the same ADK pattern
