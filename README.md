# Virtual Human Assistant - Free AI Desktop App

This repository now includes an MVP Python desktop application based on the **Virtual Human Assistant** concept.

## What it does

- Understands whether input is a question, task, or goal.
- Builds a simple **Understand → Think → Plan → Act → Verify → Learn** plan.
- Uses only **free/open-source models**:
  - Local Ollama model first (free, local).
  - Hugging Face Inference API fallback (free tier).
- Stores short-term memory in `memory.json`.
- Desktop UI with Plan / Response / Memory tabs.

## Security first

Do **not** hardcode API keys in code.
Use environment variables only.
If keys were shared publicly, rotate/revoke them immediately.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# export variables from .env manually or via your shell workflow
python app.py
```

## Optional: local free model with Ollama

1. Install Ollama
2. Pull a free model:
   ```bash
   ollama pull llama3.1:8b
   ```
3. Run app; it will use `http://localhost:11434` automatically.

## Notes

- This MVP is intentionally safe/simple and avoids dangerous auto-control actions.
- You can later add controlled mouse/keyboard automation modules with explicit user confirmation.
