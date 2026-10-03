# Fable 5.1 · 100 HTML Files

A collection of **100 self-contained HTML visual studies** generated with **Fable 5.1** — generative art, physics simulations, typography experiments, interfaces and animated scenes. Every piece is a single HTML file with all CSS and JS inline (no external fonts, images or libraries), and ships with its original generation prompt and a rendered screenshot.

**Browse the gallery:** https://miaai-lab.github.io/Fable-5.1-100-HTML-Files/

## Structure

```
├── index.html            ← gallery index (screenshot + description + prompt per study)
├── thumbs/               ← rendered screenshots (001–100, web-optimized JPEG)
├── NNN-*.html            ← the 100 standalone studies
├── NNN-*.txt             ← original prompt, description, techniques and interaction notes
├── generate_index.py     ← regenerates index.html from the studies + thumbs
└── shot_playwright.js    ← regenerates thumbs/ (headless Chromium captures)
```

## Gallery features

- One card per study: screenshot, number, title, description
- **Open** — loads the piece in a new tab
- **Prompt** — expands to the full original generation prompt and its prompt file
- Search across numbers, titles, descriptions and prompt text, with a live result count

## The studies

The 100 studies cover, among others: aurora glassmorphism heroes, brutalist manifests, neumorphic
control surfaces, cyberpunk terminals, metaballs, particle constellations, editorial magazine
spreads, escape-room maps, neural-network visualizers, synths, planetariums, flow fields, reaction–
diffusion, string art, snow globes, tarot decks and a final organic wave lab.

## Rebuilding

```bash
# re-capture all screenshots (needs Playwright + a Chromium build)
node shot_playwright.js            # or: node shot_playwright.js 001-x.html,002-y.html

# regenerate the gallery page
python3 generate_index.py
```

Part of MiaAI Lab's LLM front-end capability evaluations: same prompt-style briefs, different model,
same 100-slot budget.
