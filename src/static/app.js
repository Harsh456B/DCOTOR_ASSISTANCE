const API_BASE = "";

function $(id) {
  return document.getElementById(id);
}

const imageInput = $("imageInput");
const dropZone = $("dropZone");
const imagePreviewWrapper = $("imagePreviewWrapper");
const imagePreview = $("imagePreview");
const clearImageBtn = $("clearImageBtn");
const languageSelect = $("languageSelect");
const analysisType = $("analysisType");
const voiceGender = $("voiceGender");
const contextInput = $("contextInput");
const analyzeBtn = $("analyzeBtn");
const btnSpinner = $("btnSpinner");
const reportOutput = $("reportOutput");
const copyReportBtn = $("copyReportBtn");
const audioPlayer = $("audioPlayer");
const audioHint = $("audioHint");

let selectedFile = null;

function openFileDialog() {
  imageInput.click();
}

dropZone.addEventListener("click", openFileDialog);

dropZone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropZone.classList.add("dragover");
});

dropZone.addEventListener("dragleave", () => {
  dropZone.classList.remove("dragover");
});

dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropZone.classList.remove("dragover");
  const file = e.dataTransfer.files?.[0];
  if (file && file.type.startsWith("image/")) {
    setSelectedFile(file);
  }
});

imageInput.addEventListener("change", (e) => {
  const file = e.target.files?.[0];
  if (file && file.type.startsWith("image/")) {
    setSelectedFile(file);
  }
});

clearImageBtn.addEventListener("click", () => {
  selectedFile = null;
  imageInput.value = "";
  imagePreviewWrapper.classList.add("hidden");
  imagePreview.src = "";
});

function setSelectedFile(file) {
  selectedFile = file;
  const reader = new FileReader();
  reader.onload = (ev) => {
    imagePreview.src = ev.target.result;
    imagePreviewWrapper.classList.remove("hidden");
  };
  reader.readAsDataURL(file);
}

// Tabs
document.querySelectorAll(".tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    const target = tab.getAttribute("data-tab");
    document.querySelectorAll(".tab").forEach((t) => t.classList.remove("active"));
    document.querySelectorAll(".tab-panel").forEach((panel) => panel.classList.remove("active"));
    tab.classList.add("active");
    $("tab-" + target).classList.add("active");
  });
});

function setLoading(isLoading) {
  if (isLoading) {
    analyzeBtn.disabled = true;
    btnSpinner.classList.remove("hidden");
  } else {
    analyzeBtn.disabled = false;
    btnSpinner.classList.add("hidden");
  }
}

async function analyzeImage() {
  if (!selectedFile) {
    alert("Please upload a medical image first.");
    return;
  }

  const formData = new FormData();
  formData.append("image", selectedFile);
  formData.append("analysis_type", analysisType.value);
  formData.append("language", languageSelect.value);
  formData.append("gender", voiceGender.value);
  formData.append("additional_context", contextInput.value || "");

  setLoading(true);
  reportOutput.textContent = "Analyzing image, please wait...";
  audioPlayer.classList.add("hidden");
  audioPlayer.src = "";
  audioHint.textContent = "Generating audio (if available)...";

  try {
    const res = await fetch(`${API_BASE}/api/analyze-image`, {
      method: "POST",
      body: formData,
    });

    if (!res.ok) {
      const errorText = await res.text();
      throw new Error(errorText || `Request failed with status ${res.status}`);
    }

    const data = await res.json();
    reportOutput.textContent = data.analysis || "No analysis text returned.";

    if (data.audio_path) {
      const audioUrl = `${API_BASE}/api/audio?path=${encodeURIComponent(
        data.audio_path,
      )}`;
      audioPlayer.src = audioUrl;
      audioPlayer.classList.remove("hidden");
      audioHint.textContent = "Audio generated. Press play to listen.";
    } else {
      audioPlayer.classList.add("hidden");
      audioPlayer.src = "";
      audioHint.textContent = "No audio was generated for this response.";
    }

    document
      .querySelector('.tab[data-tab="report"]')
      ?.classList.add("active");
    document.querySelector("#tab-report")?.classList.add("active");
    document
      .querySelector('.tab[data-tab="audio"]')
      ?.classList.remove("active");
    document.querySelector("#tab-audio")?.classList.remove("active");
  } catch (err) {
    console.error(err);
    reportOutput.textContent =
      "Something went wrong while analyzing the image.\n\n" +
      (err.message || String(err));
    audioPlayer.classList.add("hidden");
    audioPlayer.src = "";
    audioHint.textContent = "Unable to generate audio due to an error.";
  } finally {
    setLoading(false);
  }
}

analyzeBtn.addEventListener("click", analyzeImage);

copyReportBtn.addEventListener("click", async () => {
  const text = reportOutput.textContent || "";
  if (!text.trim()) return;
  try {
    await navigator.clipboard.writeText(text);
    copyReportBtn.textContent = "Copied";
    setTimeout(() => {
      copyReportBtn.textContent = "Copy report";
    }, 1500);
  } catch (e) {
    console.error(e);
  }
});

