# CodeScribe Lite (Flask + Tailwind)

A minimal, working version of the CodeScribe AI UI with a real Flask backend.
- Works **without** an API key (deterministic demo output)
- Uses OpenAI if `OPENAI_API_KEY` is set

## Quickstart
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

pip install -r requirements.txt

# Optional for live AI:
# macOS/Linux:
export OPENAI_API_KEY=your_key_here
# Windows (cmd):
# set OPENAI_API_KEY=your_key_here

python server.py
# Open http://127.0.0.1:5000
```
