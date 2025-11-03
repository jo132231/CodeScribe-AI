async function analyze(action, code) {
  const res = await fetch("/analyze", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ action, code })
  });
  const data = await res.json();
  if (!data.ok) throw new Error(data.error || "Unknown error");
  return data.result;
}

function setLoading(btn, loading) {
  if (loading) {
    btn.dataset._label = btn.textContent;
    btn.textContent = "…";
    btn.disabled = true;
  } else {
    btn.textContent = btn.dataset._label || btn.textContent;
    btn.disabled = false;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const codeEl = document.getElementById("codeInput");
  const outputCard = document.getElementById("outputCard");
  const output = document.getElementById("output");
  const title = document.getElementById("outputTitle");
  const clearBtn = document.getElementById("clearBtn");

  document.querySelectorAll(".action-btn").forEach(btn => {
    btn.addEventListener("click", async () => {
      const action = btn.getAttribute("data-action");
      const code = codeEl.value || "";
      setLoading(btn, true);
      try {
        const result = await analyze(action, code);
        title.textContent = action.toUpperCase();
        output.textContent = result;
        outputCard.classList.remove("hidden");
        outputCard.scrollIntoView({ behavior: "smooth", block: "nearest" });
      } catch (err) {
        title.textContent = "Error";
        output.textContent = (err && err.message) || String(err);
        outputCard.classList.remove("hidden");
      } finally {
        setLoading(btn, false);
      }
    });
  });

  clearBtn.addEventListener("click", () => {
    outputCard.classList.add("hidden");
    output.textContent = "";
    codeEl.focus();
  });
});
