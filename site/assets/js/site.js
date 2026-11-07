(() => {
  const root = document.documentElement;
  const live = document.getElementById("live");
  const announce = (message) => {
    live.textContent = "";
    requestAnimationFrame(() => { live.textContent = message; });
  };

  const copyText = async (text) => {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
      return;
    }
    const area = document.createElement("textarea");
    area.value = text;
    area.setAttribute("readonly", "");
    area.style.position = "fixed";
    area.style.opacity = "0";
    document.body.appendChild(area);
    area.select();
    const ok = document.execCommand("copy");
    area.remove();
    if (!ok) throw new Error("copy failed");
  };

  document.querySelectorAll(".code-block").forEach((block) => {
    const code = block.querySelector("pre code");
    if (!code) return;
    const label = block.querySelector(".code-label");
    const button = document.createElement("button");
    button.type = "button";
    button.className = "copy-btn";
    button.textContent = "Copy";
    button.setAttribute("aria-label", `Copy: ${label ? label.textContent : "code"}`);
    let timer;
    button.addEventListener("click", async () => {
      try {
        await copyText(code.textContent.replace(/\n+$/, ""));
        button.textContent = "Copied";
        button.dataset.state = "done";
        announce("Copied to clipboard");
      } catch {
        button.textContent = "Press ⌘C";
        const range = document.createRange();
        range.selectNodeContents(code);
        const selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
        announce("Copy is blocked. The text is selected; copy it with your keyboard.");
      }
      clearTimeout(timer);
      timer = setTimeout(() => {
        button.textContent = "Copy";
        delete button.dataset.state;
      }, 2000);
    });
    block.appendChild(button);
  });

  // The deck player listens for arrow keys on its own document, which this same-origin page can reach.
  const deck = document.getElementById("deck");
  const sendKey = (key) => {
    const doc = deck && deck.contentDocument;
    if (!doc) return false;
    const keyCode = key === "ArrowRight" ? 39 : 37;
    doc.dispatchEvent(new KeyboardEvent("keydown", { key, code: key, keyCode, which: keyCode, bubbles: true }));
    return true;
  };
  document.querySelectorAll("[data-deck]").forEach((button) => {
    button.addEventListener("click", () => {
      sendKey(button.dataset.deck === "next" ? "ArrowRight" : "ArrowLeft");
    });
  });

  // System, Light, or Dark. The choice is saved under the key the embedded deck reads too.
  const THEME_KEY = "ghsb-theme";
  const THEMES = ["system", "light", "dark"];
  const themeSwitch = document.querySelector(".theme-switch");
  const savedTheme = () => {
    try {
      const value = localStorage.getItem(THEME_KEY);
      return THEMES.includes(value) ? value : "system";
    } catch {
      return "system";
    }
  };
  // Light art and browser colors follow the system by default; an explicit choice overrides it.
  const applyTheme = (choice) => {
    if (choice === "system") root.removeAttribute("data-theme");
    else root.dataset.theme = choice;
    document.querySelectorAll("[data-theme-media]").forEach((element) => {
      const theme = element.dataset.themeMedia;
      element.media = choice === "system" ? `(prefers-color-scheme: ${theme})` : choice === theme ? "all" : "not all";
    });
    if (themeSwitch) {
      const radio = themeSwitch.querySelector(`input[value="${choice}"]`);
      if (radio) radio.checked = true;
    }
  };
  const tellDeck = () => {
    if (deck && deck.contentWindow) deck.contentWindow.postMessage({ type: "ghsb-theme" }, "/");
  };
  if (themeSwitch) {
    applyTheme(savedTheme());
    themeSwitch.hidden = false;
    themeSwitch.addEventListener("change", (event) => {
      const choice = event.target.value;
      try {
        if (choice === "system") localStorage.removeItem(THEME_KEY);
        else localStorage.setItem(THEME_KEY, choice);
      } catch {
        // Storage can be blocked; the choice still applies to this page view.
      }
      applyTheme(choice);
      tellDeck();
    });
    window.addEventListener("storage", (event) => {
      if (event.key === THEME_KEY || event.key === null) applyTheme(savedTheme());
    });
  }

  const links = [...document.querySelectorAll(".site-nav a")];
  const sections = links.map((a) => document.querySelector(a.getAttribute("href"))).filter(Boolean);
  if ("IntersectionObserver" in window && sections.length) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        links.forEach((a) => a.removeAttribute("aria-current"));
        const active = links.find((a) => a.getAttribute("href") === `#${entry.target.id}`);
        if (active) active.setAttribute("aria-current", "location");
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    sections.forEach((section) => observer.observe(section));
  }
})();
