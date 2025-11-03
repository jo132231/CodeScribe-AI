# CodeScribe AI

CodeScribe AI is a lightweight developer tool that explains code, generates unit tests, adds documentation, performs risk audits, and creates README files using AI.

## Features
✅ Code explanation  
✅ Auto unit test generation (pytest / Jest)  
✅ Docstring / JSDoc insertion  
✅ Code audit with severity & fixes  
✅ One-click README generation  
✅ Works even without API key (demo mode)

## Tech Stack
- Backend: Python + Flask
- Frontend: HTML + Tailwind + Vanilla JS
- AI: OpenAI API (`gpt-4o-mini`)
- Fallback: Local mock output if no API key

## Run Locally
```sh
git clone https://github.com/YOUR_USERNAME/codescribe-ai.git
cd codescribe-ai
py -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
set OPENAI_API_KEY=your_key_here   # Windows
python server.py
# CodeScribe-AI
Developer tool to explain, test, document &amp; audit code using AI
