# JanVikas AI

An explainable Streamlit prototype for the Hack2Skill "AI for Digital Public Infrastructure & Governance" problem statement.

## Features
- Citizen request submission
- Multilingual-ready input
- Explainable AI priority scoring
- Demand hotspot map
- Analytics dashboard
- Policymaker dashboard
- SQLite database
- Demo data
- No external API key required

## Run

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

Linux/macOS:
```bash
source .venv/bin/activate
```

Install:
```bash
pip install -r requirements.txt
```

Start:
```bash
streamlit run app.py
```

## AI upgrade path

For the hackathon demo, the included AI engine is deterministic and explainable. In a production version, add:
1. Speech-to-text
2. Translation
3. LLM-based classification/summarization
4. RAG over government schemes and infrastructure policies
5. GIS hotspot clustering
6. Predictive demand forecasting
7. Human approval workflow
8. Authentication and audit logs

## Suggested project name

JanVikas AI — Citizen Voice to Government Action
