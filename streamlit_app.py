import os, re
import streamlit as st

# -------- OpenAI client (new SDK) ----------
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except Exception:
    OPENAI_AVAILABLE = False

# -------- Config & state ----------
st.set_page_config(page_title="CodeScribe AI (Streamlit)", page_icon="🧠", layout="wide")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Priority: Streamlit Cloud secrets → env var → sidebar input
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", None) if hasattr(st, "secrets") else None
if not OPENAI_API_KEY:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# UI — header
st.title("CodeScribe AI")
st.caption("Explain • Tests • Docstrings • Audit • README — paste code and click")

# Sidebar: key + mode status
with st.sidebar:
    st.subheader("Settings")
    if not OPENAI_API_KEY:
        user_key = st.text_input("OpenAI API Key (optional)", type="password", help="Used only in your session")
        if user_key:
            OPENAI_API_KEY = user_key

    ai_mode = OPENAI_AVAILABLE and bool(OPENAI_API_KEY)
    st.write(f"**AI mode:** {'ON ✅' if ai_mode else 'OFF (demo) ⚠️'}")
    st.write(f"**Model:** {MODEL}")

# -------- LLM helpers ----------
def has_ai() -> bool:
    return ai_mode

def fallback_answer(prompt: str) -> str:
    head = "### (Demo Output)\n"
    return head + "Running in demo mode. Structured mock result based on your code & action.\n\n" + prompt[:1200]

def llm_answer(prompt: str, system="You are a senior software engineer. Be precise and actionable.") -> str:
    if has_ai():
        try:
            client = OpenAI(api_key=OPENAI_API_KEY)
            resp = client.chat.completions.create(
                model=MODEL,
                messages=[{"role":"system","content":system},
                          {"role":"user","content":prompt}],
                temperature=0.2,
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            return f"(LLM error: {e})\n\n" + fallback_answer(prompt)
    return fallback_answer(prompt)

# -------- Actions ----------
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
    prompt = (
        "Review this code for bugs, smells, risks, and security issues.\n"
        "- List each issue with severity (High/Med/Low) and a one-line fix.\n"
        "- End with 3 refactor suggestions.\n\n"
        f"```code\n{code}\n```"
    )
    return llm_answer(prompt, system="You are a careful code auditor. Be specific and practical.")

def gen_readme(code: str) -> str:
    prompt = f"Given this code, draft a concise README.md with features, setup, usage examples, and limitations.\n\n```code\n{code}\n```"
    return llm_answer(prompt)

# -------- UI layout ----------
left, right = st.columns([1,1])
with left:
    code = st.text_area("Paste your code here:", height=300, placeholder="// Paste code...")

    col1, col2, col3, col4, col5 = st.columns(5)
    do_explain = col1.button("Explain")
    do_tests   = col2.button("Tests")
    do_docs    = col3.button("Docstrings")
    do_audit   = col4.button("Audit")
    do_readme  = col5.button("README")

with right:
    st.markdown("### Output")
    output = st.empty()

# -------- Actions handling ----------
if do_explain:
    if not code.strip():
        st.error("Please paste some code first.")
    else:
        with st.spinner("Explaining..."):
            output.markdown(explain(code))

if do_tests:
    if not code.strip():
        st.error("Please paste some code first.")
    else:
        with st.spinner("Generating tests..."):
            output.code(gen_tests(code), language="python")

if do_docs:
    if not code.strip():
        st.error("Please paste some code first.")
    else:
        with st.spinner("Adding docstrings..."):
            output.code(gen_docs(code), language="python")

if do_audit:
    if not code.strip():
        st.error("Please paste some code first.")
    else:
        with st.spinner("Auditing..."):
            output.markdown(audit(code))

if do_readme:
    # README can work even without code (will produce a minimal scaffold)
    with st.spinner("Drafting README..."):
        output.code(gen_readme(code or "# Project\n\n(Describe your project here)"), language="markdown")

st.markdown("---")
st.caption("CodeScribe AI · Streamlit demo · Privacy: stateless, nothing stored server-side.")
