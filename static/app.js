const promptEl = document.getElementById("prompt");
const generateBtn = document.getElementById("generateBtn");
const copyBtn = document.getElementById("copyBtn");
const loadingEl = document.getElementById("loading");
const errorEl = document.getElementById("error");
const outputEl = document.getElementById("output");

let lastOutput = "";

function setLoading(isLoading) {
  loadingEl.classList.toggle("hidden", !isLoading);
  generateBtn.disabled = isLoading;
  copyBtn.disabled = isLoading || !lastOutput;
}

function showError(message) {
  errorEl.textContent = message;
  errorEl.classList.remove("hidden");
}

function clearError() {
  errorEl.textContent = "";
  errorEl.classList.add("hidden");
}

function showOutput(data) {
  lastOutput = JSON.stringify(data, null, 2);
  outputEl.textContent = lastOutput;
  outputEl.classList.remove("hidden");
  copyBtn.disabled = false;
}

generateBtn.addEventListener("click", async () => {
  clearError();
  outputEl.classList.add("hidden");
  setLoading(true);

  try {
    const response = await fetch("/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ prompt: promptEl.value })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Generation failed");
    }

    showOutput(data);
  } catch (error) {
    showError(error.message);
  } finally {
    setLoading(false);
  }
});

copyBtn.addEventListener("click", async () => {
  if (!lastOutput) return;
  await navigator.clipboard.writeText(lastOutput);
});
