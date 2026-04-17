const API = {
  referenceData: () => fetch("/api/reference-data").then(r => r.json()),
  personaCard: (id) => fetch(`/api/persona-card/${id}`).then(r => { if (!r.ok) throw new Error("Persona not found"); return r.json(); }),
  refine: (body) => fetch("/api/refine", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) }).then(async r => { const data = await r.json(); if (!r.ok) throw new Error(data.detail || "Refinement failed"); return data; }),
};

// ─── State ───────────────────────────────────────────────────────────────────
let currentPersonaCard = null;

// ─── DOM refs ─────────────────────────────────────────────────────────────────
const $ = id => document.getElementById(id);
const form = $("persona-form");
const companyInput = $("company-name");
const industrySelect = $("industry");
const marketSelect = $("market");
const personaSelect = $("persona");
const originalSection = $("original-card-section");
const refinedSection = $("refined-card-section");
const refineBtn = $("refine-btn");
const loadingOverlay = $("loading-overlay");
const toast = $("toast");

// ─── Bootstrap: load reference data ──────────────────────────────────────────
async function bootstrap() {
  try {
    const data = await API.referenceData();
    populateSelect(industrySelect, data.industries, "Select industry");
    populateSelect(marketSelect, data.markets, "Select market");
    data.personas.forEach(p => {
      const opt = new Option(p.label, p.id);
      personaSelect.appendChild(opt);
    });
  } catch {
    showToast("error", "Failed to load", "Could not fetch reference data. Please refresh.");
  }
}

function populateSelect(el, items, placeholder) {
  el.innerHTML = `<option value="" disabled selected>${placeholder}</option>`;
  items.forEach(item => el.appendChild(new Option(item, item)));
}

// ─── Persona card display ─────────────────────────────────────────────────────
personaSelect.addEventListener("change", async () => {
  const id = personaSelect.value;
  if (!id) return;
  clearFieldError(personaSelect);
  try {
    const card = await API.personaCard(id);
    currentPersonaCard = card;
    renderPersonaCard("original-card", card, personaSelect.options[personaSelect.selectedIndex].text);
    originalSection.classList.remove("section-hidden");
    refinedSection.classList.add("section-hidden");
    originalSection.scrollIntoView({ behavior: "smooth", block: "nearest" });
  } catch (err) {
    showToast("error", "Error", err.message);
  }
});

function renderPersonaCard(containerId, card, personaLabel, isRefined = false) {
  const container = $(containerId);
  const subtitle = container.closest(".card").querySelector(".card__subtitle");
  if (subtitle) subtitle.textContent = personaLabel;

  const sections = [
    { key: "core_responsibilities", label: "Core Responsibilities" },
    { key: "external_signals", label: "External Signals" },
    { key: "objections_concerns_risks", label: "Objections, Concerns & Risks" },
    { key: "value_gaps", label: "Value Gaps" },
  ];

  let html = "";

  if (isRefined && card.refinement_summary) {
    html += `
      <div class="refinement-summary">
        <div class="refinement-summary__label">Refinement Summary</div>
        ${escapeHtml(card.refinement_summary)}
      </div>`;
  }

  sections.forEach(({ key, label }) => {
    const items = card[key] || [];
    html += `
      <div class="persona-section">
        <div class="persona-section__title">${label}</div>
        <ul class="persona-section__list">
          ${items.map(item => `<li>${escapeHtml(item)}</li>`).join("")}
        </ul>
      </div>`;
  });

  container.innerHTML = html;
}

// ─── Form validation ──────────────────────────────────────────────────────────
function validateForm() {
  let valid = true;

  if (!companyInput.value.trim()) {
    showFieldError(companyInput, "Company name is required.");
    valid = false;
  } else if (!/^[a-zA-Z0-9\s&.,'\-()]+$/.test(companyInput.value.trim())) {
    showFieldError(companyInput, "Use letters, numbers, and common punctuation only.");
    valid = false;
  } else {
    clearFieldError(companyInput);
  }

  [industrySelect, marketSelect, personaSelect].forEach(sel => {
    if (!sel.value) {
      showFieldError(sel, `Please select a ${sel.id.replace("-", " ")}.`);
      valid = false;
    } else {
      clearFieldError(sel);
    }
  });

  if (!currentPersonaCard) {
    showToast("error", "Persona card not loaded", "Please select a persona to load its card before refining.");
    valid = false;
  }

  return valid;
}

function showFieldError(el, msg) {
  el.classList.add("error");
  const errEl = el.parentElement.querySelector(".field-error");
  if (errEl) { errEl.textContent = msg; errEl.classList.add("visible"); }
}

function clearFieldError(el) {
  el.classList.remove("error");
  const errEl = el.parentElement?.querySelector(".field-error");
  if (errEl) errEl.classList.remove("visible");
}

// ─── Form submit / refine ─────────────────────────────────────────────────────
form.addEventListener("submit", async e => {
  e.preventDefault();
  if (!validateForm()) return;

  setLoading(true);

  const payload = {
    company_name: companyInput.value.trim(),
    industry: industrySelect.value,
    market: marketSelect.value,
    persona: personaSelect.value,
    persona_card: currentPersonaCard,
  };

  try {
    const refined = await API.refine(payload);
    const personaLabel = personaSelect.options[personaSelect.selectedIndex].text;
    renderPersonaCard("refined-card", refined, personaLabel, true);
    refinedSection.classList.remove("section-hidden");
    refinedSection.scrollIntoView({ behavior: "smooth", block: "start" });
    showToast("success", "Refinement complete", `Persona card for ${payload.company_name} has been contextualized.`);
  } catch (err) {
    showToast("error", "Refinement failed", err.message);
  } finally {
    setLoading(false);
  }
});

// ─── Reset ────────────────────────────────────────────────────────────────────
$("reset-btn").addEventListener("click", () => {
  form.reset();
  currentPersonaCard = null;
  originalSection.classList.add("section-hidden");
  refinedSection.classList.add("section-hidden");
  [companyInput, industrySelect, marketSelect, personaSelect].forEach(clearFieldError);
});

// ─── Helpers ──────────────────────────────────────────────────────────────────
function setLoading(on) {
  loadingOverlay.classList.toggle("visible", on);
  refineBtn.disabled = on;
}

let toastTimer;
function showToast(type, title, message) {
  toast.className = `toast toast--${type}`;
  const iconPath = type === "success"
    ? "M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
    : "M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z";
  toast.innerHTML = `
    <svg class="toast__icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
      <path stroke-linecap="round" stroke-linejoin="round" d="${iconPath}"/>
    </svg>
    <div class="toast__body">
      <div class="toast__title">${escapeHtml(title)}</div>
      <div class="toast__message">${escapeHtml(message)}</div>
    </div>`;
  toast.classList.add("visible");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove("visible"), 5000);
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

// ─── Init ─────────────────────────────────────────────────────────────────────
bootstrap();
