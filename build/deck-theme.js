// System, Light, or Dark for the website deck. build-bento.py inlines this file right after
// #bento-doc, so it runs before Bento reads the slides. Light swaps in the light slides that
// build-bento.py stores in #ghsb-light; dark leaves the document alone. The website saves the
// same choice under the same key and also posts it here, so the page and its embedded deck agree.
(() => {
  const KEY = "ghsb-theme";
  const SLIDE_KEY = "ghsb-deck-slide";
  const HINT = "ghsb-theme:";
  const CHOICES = ["system", "light", "dark"];
  const root = document.documentElement;
  const prefersLight = window.matchMedia ? window.matchMedia("(prefers-color-scheme: light)") : null;

  const stored = () => {
    try {
      const value = localStorage.getItem(KEY);
      return CHOICES.includes(value) ? value : "system";
    } catch {
      return "system";
    }
  };
  // Switching themes reloads the deck. When storage is blocked, window.name carries the choice
  // across that reload, because it survives reloads in the same tab or frame.
  const hinted = () => {
    const name = String(window.name || "");
    const value = name.startsWith(HINT) ? name.slice(HINT.length) : "";
    return CHOICES.includes(value) ? value : null;
  };
  const hint = (value) => {
    if (value) window.name = HINT + value;
    else if (hinted()) window.name = "";
  };
  const resolve = (choice) => {
    if (choice !== "system") return choice;
    return prefersLight && prefersLight.matches ? "light" : "dark";
  };

  let choice = hinted() || stored();
  const wanted = resolve(choice);
  let applied = "dark";
  if (wanted === "light") {
    try {
      const block = document.getElementById("bento-doc");
      const doc = JSON.parse(block.textContent);
      const light = JSON.parse(document.getElementById("ghsb-light").textContent);
      const ids = (slides) => slides.map((s) => s.id).join("\n");
      if (ids(doc.slides) === ids(light.slides)) {
        doc.theme = light.theme;
        doc.slides = light.slides.map((s, i) => ({ ...s, notes: doc.slides[i].notes }));
        Object.assign(doc.assets, light.assets);
        block.textContent = JSON.stringify(doc).replace(/[<]/g, "\\u003c");
        applied = "light";
      } else {
        console.warn("gh-skills-builder: the light slides do not match this deck; showing dark");
      }
    } catch (error) {
      console.warn("gh-skills-builder: showing the dark slides", error);
    }
  }
  root.dataset.ghsbTheme = applied;

  // Bento always opens the player on the first slide, so a theme reload notes where you were.
  const slideIndex = () => {
    const sections = document.querySelectorAll(".reveal > .slides > section");
    for (let i = 0; i < sections.length; i += 1) {
      if (sections[i].classList.contains("present")) return i;
    }
    return -1;
  };
  const slideIds = (() => {
    try {
      return JSON.parse(document.getElementById("ghsb-light").textContent).slides.map((s) => s.id);
    } catch {
      return [];
    }
  })();
  const reload = () => {
    const index = slideIndex();
    try {
      if (index > 0 && slideIds[index]) sessionStorage.setItem(SLIDE_KEY, slideIds[index]);
    } catch {
      // Without session storage the deck restarts at the first slide.
    }
    location.reload();
  };

  let resume = null;
  try {
    resume = sessionStorage.getItem(SLIDE_KEY);
    sessionStorage.removeItem(SLIDE_KEY);
  } catch {
    resume = null;
  }
  if (resume) {
    // Bento jumps to a slide when an element linked to that slide's id is clicked.
    const started = Date.now();
    const jump = () => {
      const slides = document.querySelector(".reveal.ready > .slides");
      if (!slides) {
        if (Date.now() - started < 10000) setTimeout(jump, 50);
        return;
      }
      const link = document.createElement("span");
      link.dataset.link = resume;
      link.setAttribute("data-bento-transient", "");
      link.hidden = true;
      slides.appendChild(link);
      link.click();
      link.remove();
    };
    jump();
  }

  const listeners = [];
  const notify = () => listeners.forEach((listener) => listener());
  const follow = (value) => {
    choice = value;
    if (resolve(choice) !== wanted) reload();
    else notify();
  };
  // A choice that storage did not keep is hinted, so the reload still shows it.
  const choose = (value, saved) => {
    hint(saved ? null : value);
    follow(value);
  };
  window.addEventListener("storage", (event) => {
    if (event.key !== KEY && event.key !== null) return;
    hint(null);
    follow(stored());
  });
  if (prefersLight) prefersLight.addEventListener("change", () => follow(choice));
  window.addEventListener("message", (event) => {
    if (event.source !== window.parent || event.origin !== location.origin) return;
    if (!event.data || event.data.type !== "ghsb-theme") return;
    const value = CHOICES.includes(event.data.choice) ? event.data.choice : stored();
    choose(value, stored() === value);
  });

  // Inside the website the page header has the switch; the full-screen deck gets its own.
  if (window.self !== window.top) return;

  const build = () => {
    const style = document.createElement("style");
    style.setAttribute("data-bento-transient", "");
    style.textContent = `
.ghsb-theme{position:fixed;top:12px;right:12px;z-index:2147483647;display:flex;gap:2px;padding:3px;
  border-radius:999px;border:1.5px solid #2a6b3f;background:rgba(16,20,17,.92);color:#fff;
  font:600 13px/1 "Mona Sans",system-ui,-apple-system,"Segoe UI",sans-serif;opacity:0;pointer-events:none;
  transition:opacity .2s ease}
:root[data-ghsb-theme="light"] .ghsb-theme{border-color:#a6d9b5;background:rgba(255,255,255,.94);color:#20262c}
.ghsb-theme.is-shown,.ghsb-theme:focus-within{opacity:1;pointer-events:auto}
.ghsb-theme button{appearance:none;margin:0;border:0;background:transparent;color:inherit;font:inherit;
  cursor:pointer;padding:7px 11px;border-radius:999px}
.ghsb-theme button[aria-pressed="true"]{background:#0d6836;color:#fff}
.ghsb-theme button:focus-visible{outline:2px solid #5eec83;outline-offset:2px}
:root[data-ghsb-theme="light"] .ghsb-theme button:focus-visible{outline-color:#0d6836}
@media (prefers-reduced-motion:reduce){.ghsb-theme{transition:none}}`;
    document.head.appendChild(style);

    const group = document.createElement("div");
    group.className = "ghsb-theme";
    group.setAttribute("role", "group");
    group.setAttribute("aria-label", "Color theme");
    group.setAttribute("data-bento-transient", "");
    const buttons = CHOICES.map((value) => {
      const button = document.createElement("button");
      button.type = "button";
      button.textContent = value[0].toUpperCase() + value.slice(1);
      button.addEventListener("click", () => {
        let saved = false;
        try {
          localStorage.setItem(KEY, value);
          saved = localStorage.getItem(KEY) === value;
        } catch {
          // Private modes can block storage; the hint keeps the choice for this tab.
        }
        choose(value, saved);
      });
      group.appendChild(button);
      return button;
    });
    listeners.push(() => {
      buttons.forEach((button, i) => button.setAttribute("aria-pressed", String(CHOICES[i] === choice)));
    });
    notify();
    document.body.appendChild(group);

    // The presenter's Space key advances slides; on a focused button it should press the button.
    window.addEventListener("keydown", (event) => {
      if (group.contains(event.target) && (event.key === " " || event.key === "Enter")) event.stopPropagation();
    }, true);

    // Out of the way while presenting: shown briefly on load, then whenever the pointer moves.
    let timer = 0;
    const show = () => {
      group.classList.add("is-shown");
      clearTimeout(timer);
      timer = setTimeout(() => group.classList.remove("is-shown"), 2500);
    };
    document.addEventListener("pointermove", show, { passive: true });
    show();
  };
  if (document.body) build();
  else document.addEventListener("DOMContentLoaded", build);
})();
