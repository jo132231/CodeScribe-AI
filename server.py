from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os, re

# Optional OpenAI support
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except Exception:
    OPENAI_AVAILABLE = False

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def has_ai():
    return OPENAI_AVAILABLE and OPENAI_API_KEY and OPENAI_API_KEY.strip()

def llm_answer(prompt, system="You are a senior software engineer. Be precise and actionable."):
    if has_ai():
        try:
            client = OpenAI(api_key=OPENAI_API_KEY)
            resp = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "system", "content": system},
                          {"role": "user", "content": prompt}],
                temperature=0.2,
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            return f"(LLM error: {e})\n\n" + fallback_answer(prompt)
    else:
        return fallback_answer(prompt)

def fallback_answer(prompt: str) -> str:
    head = "### (Demo Output)\n"
    return head + "No OPENAI_API_KEY detected. Showing a structured mock result based on your code and action.\n\n" + prompt[:1200]

def explain(code: str) -> str:
    prompt = f"Explain this code to a mid-level dev. Include purpose, key logic, edge cases, and complexity.\n\n```code\n{code}\n```"
    return llm_answer(prompt)

def gen_tests(code: str) -> str:
    lang = "python" if re.search(r"def\s+\w+\(", code) else "javascript"
    framework = "pytest" if lang == "python" else "Jest"
    prompt = f"Write {framework} unit tests with good coverage for this {lang} code. Keep deterministic.\n\n```{lang}\n{code}\n```"
    return llm_answer(prompt, system="You write minimal, excellent unit tests. Output only the test file content.")

def gen_docs(code: str) -> str:
    prompt = f"Add clear docstrings/comments (PEP257 for Python or JSDoc for JS/TS). Do not change behavior. Return the revised code only.\n\n```code\n{code}\n```"
    return llm_answer(prompt, system="Return ONLY the revised code.")

def audit(code: str) -> str:
    prompt = f"""Review this code for bugs, smells, risks, and security issues. 
- List each issue with severity (High/Med/Low) and a one-line fix.
- End with 3 refactor suggestions.

```code
{code}
```"""
    return llm_answer(prompt, system="You are a careful code auditor. Be specific and practical.")

def gen_readme(code: str) -> str:
    prompt = f"Given this code, draft a concise README.md with features, setup, usage examples, and limitations.\n\n```code\n{code}\n```"
    return llm_answer(prompt)

@app.route("/")
def home():
    return render_template("index.html", model=MODEL, ai_enabled=bool(has_ai()))

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(force=True)
    action = data.get("action", "").lower()
    code = data.get("code", "") or ""
    if not code.strip() and action != "readme":
        return jsonify({"ok": False, "error": "No code received."}), 400

    if action == "explain":
        out = explain(code)
    elif action == "tests":
        out = gen_tests(code)
    elif action == "docs":
        out = gen_docs(code)
    elif action == "audit":
        out = audit(code)
    elif action == "readme":
        out = gen_readme(code)
    else:
        return jsonify({"ok": False, "error": "Unknown action."}), 400

    return jsonify({"ok": True, "result": out})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
