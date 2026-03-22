# Institutional Financial Dashboard V2A

A repository-ready, Streamlit-first financial intelligence app for **listed companies**.

## What this pack includes
- Live adapters for **Financial Modeling Prep**, **FRED**, and **Anthropic**
- Safe **sample-mode fallback** so the app still runs without API keys
- KPI, valuation, risk, scoring, and memo generation layers
- Streamlit premium dashboard UI
- Repo hygiene: `.gitignore`, `.env.example`, Streamlit secrets template
- Tests for core engines and service orchestration

## Architecture
```text
frontend/app.py                    # Streamlit entrypoint
backend/adapters/                  # External API clients
backend/services/                  # Business orchestration
backend/engine/                    # KPI, valuation, risk, scoring logic
backend/ai/                        # AI memo generation
backend/utils/                     # config, caching, formatting, helpers
backend/data/                      # sample data fallback
tests/                             # unit tests
```

## Local setup
```bash
python -m venv .venv
# Windows
.venv\Scriptsctivate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
streamlit run frontend/app.py
```

## Environment variables
See `.env.example`.

## Streamlit deployment
- Main file path: `frontend/app.py`
- Add your secrets in Streamlit Cloud settings
- Do **not** commit real keys to GitHub

## Notes
- `USE_SAMPLE_DATA=true` lets you demo the app instantly.
- Set `USE_SAMPLE_DATA=false` once your keys are configured and you want fully live mode.
- Alpha Vantage is included as an optional backup adapter skeleton and can be wired into the orchestration layer later.
