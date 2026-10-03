#!/usr/bin/env python3
"""Generate index.html — gallery of every numbered study: screenshot, description,
collapsible original prompt. Layout mirrors the public Qwen3.8-Max collection."""
import html, os, re

DIR = os.path.dirname(os.path.abspath(__file__))
THUMB_EXT = "jpg"
KEYS = ("TITLE", "PROMPT", "DESCRIPTION")
# A prompt body contains its own all-caps sub-labels (e.g. "HUD:"), so only these stop it.
STOP = r"(?=\n(?:TITLE|PROMPT|DESCRIPTION|TECHNIQUES|INTERACTION):)"


def read_txt(path):
    """Return {TITLE, PROMPT, DESCRIPTION}; PROMPT keeps every paragraph up to DESCRIPTION."""
    raw = open(path, encoding="utf-8").read()
    out = {}
    for key in KEYS:
        stop = STOP if key != "TITLE" else r"$"
        m = re.search(r"^%s:\s*(.+?)\s*%s" % (key, stop), raw, re.M | re.S)
        if m:
            out[key] = re.sub(r"\n{2,}", "\n", m.group(1).strip())
    return out


def esc(s, quote=True):
    return html.escape(s or "", quote=quote)


entries = []
for fn in sorted(os.listdir(DIR)):
    m = re.match(r"^(\d{3})-.+\.html$", fn)
    if not m:
        continue
    txt = fn[:-5] + ".txt"
    d = read_txt(os.path.join(DIR, txt)) if os.path.exists(os.path.join(DIR, txt)) else {}
    slug = fn[:-5].split("-", 1)[1]
    entries.append({
        "num": fn[:3], "file": fn, "txt": txt,
        "title": d.get("TITLE") or slug.replace("-", " ").title(),
        "prompt": d.get("PROMPT", ""),
        "desc": d.get("DESCRIPTION", "").replace("\n", " "),
    })
entries.sort(key=lambda e: e["num"])
print("parsed:", len(entries))


def card(e):
    t, desc, prompt = esc(e["title"]), esc(e["desc"]), esc(e["prompt"])
    search = esc(" ".join([e["num"], e["title"], e["desc"], e["prompt"][:400]])).replace('"', "&quot;")
    thumb = "thumbs/%s.%s" % (e["file"][:-5], THUMB_EXT)
    return f"""<article class="card" data-title="{search}">
  <a class="thumb" href="{e["file"]}" target="_blank" rel="noopener" aria-hidden="true" tabindex="-1"><img src="{thumb}" alt="{t} screenshot" loading="lazy" decoding="async"></a>
  <div class="card-top">
    <div class="num">{e["num"]}</div>
    <div class="main">
      <div class="title"><a href="{e["file"]}" target="_blank" rel="noopener">{t}</a></div>
      <div class="desc">{desc}</div>
    </div>
    <div class="actions">
      <a class="btn btn-open" href="{e["file"]}" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17L17 7"/><path d="M9 7h8v8"/></svg>
        Open
      </a>
      <button class="btn btn-prompt" type="button" aria-expanded="false"><svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6h16M4 12h10M4 18h7"/></svg>
        Prompt
      </button>
    </div>
  </div>
  <div class="prompt-panel">
    <div class="prompt-label">Original prompt</div>
    <div class="prompt-text">{prompt}</div>
    <div class="file-name">{e["txt"]}</div>
  </div>
</article>"""


page = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Fable 5.1 · 100 HTML Files</title>
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<style>
  :root {
    --bg:#f7f6f2; --card:#ffffff; --line:#e6e1d6; --line-strong:#cfc6b4;
    --tx:#211d17; --muted:#665e50; --dim:#9a917f;
    --acc:#6d28d9; --acc2:#4338ca; --acc3:#0e7a5f;
    --shadow:0 1px 2px rgba(30,20,50,.05), 0 8px 24px -12px rgba(30,20,50,.12);
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  html { scroll-behavior: smooth; }
  body { font-family: "Segoe UI", system-ui, -apple-system, sans-serif; background: var(--bg);
         color: var(--tx); min-height: 100vh; line-height: 1.5; }
  body::before { content: ""; position: fixed; inset: 0; pointer-events: none; z-index: 0;
    background:
      radial-gradient(ellipse 80% 50% at 10% -10%, rgba(109,40,217,.10), transparent 50%),
      radial-gradient(ellipse 60% 40% at 90% 0%, rgba(67,56,202,.08), transparent 45%),
      radial-gradient(ellipse 50% 30% at 50% 100%, rgba(14,122,95,.08), transparent 40%); }
  .wrap { position: relative; z-index: 1; max-width: 960px; margin: 0 auto; padding: 48px 20px 80px; }
  header { margin-bottom: 36px; }
  .eyebrow { font-size: 11px; letter-spacing: .28em; text-transform: uppercase; color: var(--acc);
             margin-bottom: 12px; font-weight: 600; }
  h1 { font-size: clamp(28px, 5vw, 42px); font-weight: 800; letter-spacing: -.03em;
       line-height: 1.12; margin-bottom: 12px; }
  h1 span { background: linear-gradient(120deg, #7c3aed, #4f46e5, #0d9488);
            -webkit-background-clip: text; background-clip: text; color: transparent; }
  .lede { color: var(--muted); font-size: 16px; max-width: 58ch; }
  .toolbar { display: flex; flex-wrap: wrap; gap: 12px; align-items: center; margin: 28px 0 8px;
             position: sticky; top: 0; z-index: 10; padding: 14px 0;
             background: linear-gradient(180deg, rgba(247,246,242,.96) 65%, rgba(247,246,242,0));
             backdrop-filter: blur(8px); }
  .search { flex: 1; min-width: 220px; position: relative; }
  .search input { width: 100%; background: var(--card); border: 1px solid var(--line-strong);
    color: var(--tx); border-radius: 10px; padding: 12px 14px 12px 40px; font-size: 14px;
    outline: none; transition: border-color .2s, box-shadow .2s; }
  .search input::placeholder { color: var(--dim); }
  .search input:focus { border-color: rgba(109,40,217,.5); box-shadow: 0 0 0 3px rgba(109,40,217,.12); }
  .search svg { position: absolute; left: 13px; top: 50%; transform: translateY(-50%);
                width: 16px; height: 16px; color: var(--dim); pointer-events: none; }
  .count { font-size: 12px; letter-spacing: .08em; text-transform: uppercase; color: var(--dim);
           white-space: nowrap; font-variant-numeric: tabular-nums; }
  .count b { color: var(--acc); font-weight: 600; }
  .list { display: flex; flex-direction: column; gap: 12px; margin-top: 8px; }
  .card { background: var(--card); border: 1px solid var(--line); border-radius: 14px;
          overflow: hidden; box-shadow: var(--shadow);
          transition: border-color .2s, box-shadow .2s, transform .15s, background .2s; }
  .card:hover { border-color: #c9c0ae; transform: translateY(-1px);
    box-shadow: 0 2px 6px rgba(30,20,50,.06), 0 16px 34px -16px rgba(30,20,50,.20); }
  .thumb { display: block; }
  .thumb img { display: block; width: 100%; height: auto; border-radius: 14px 14px 0 0;
               transition: transform .25s ease; background: #111; }
  .card:hover .thumb img { transform: scale(1.015); }
  .card-top { display: grid; grid-template-columns: auto 1fr auto; gap: 16px;
              align-items: start; padding: 18px 18px 14px; }
  .num { font-family: ui-monospace, "SF Mono", Menlo, monospace; font-size: 12px;
         letter-spacing: .06em; color: #5b21b6; background: rgba(109,40,217,.10);
         border: 1px solid rgba(109,40,217,.22); border-radius: 8px; padding: 6px 9px;
         min-width: 48px; text-align: center; font-variant-numeric: tabular-nums; }
  .main { min-width: 0; }
  .title { font-size: 17px; font-weight: 650; letter-spacing: -.02em; margin-bottom: 4px; }
  .title a { color: inherit; text-decoration: none; }
  .title a:hover { color: var(--acc); }
  .desc { font-size: 13.5px; color: var(--muted); display: -webkit-box;
          -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
  .actions { display: flex; flex-direction: column; gap: 8px; align-items: stretch; }
  .btn { display: inline-flex; align-items: center; justify-content: center; gap: 6px;
    padding: 9px 14px; border-radius: 9px; font-size: 12px; font-weight: 600;
    letter-spacing: .04em; text-transform: uppercase; text-decoration: none;
    border: 1px solid transparent; cursor: pointer; white-space: nowrap; font-family: inherit;
    transition: background .15s, border-color .15s, color .15s, transform .1s, box-shadow .15s; }
  .btn:active { transform: scale(.97); }
  .btn-open { background: linear-gradient(135deg, rgba(124,58,237,.14), rgba(79,70,229,.12));
              color: #5b21b6; border-color: rgba(124,58,237,.35); }
  .btn-open:hover { background: linear-gradient(135deg, #7c3aed, #4f46e5); color: #fff;
                    box-shadow: 0 6px 16px -6px rgba(124,58,237,.5); }
  .btn-prompt { background: transparent; color: var(--muted); border-color: var(--line-strong); }
  .btn-prompt:hover { color: var(--tx); border-color: #a89f8b; background: #fbfaf7; }
  .btn-prompt[aria-expanded="true"] { color: var(--acc3); border-color: rgba(14,122,95,.4);
                                      background: rgba(14,122,95,.08); }
  .prompt-panel { display: none; border-top: 1px solid var(--line); padding: 16px 18px 18px;
                  background: #f4f1ea; }
  .card.open .prompt-panel { display: block; }
  .prompt-label { font-size: 10px; letter-spacing: .22em; text-transform: uppercase;
                  color: var(--acc3); margin-bottom: 10px; font-weight: 600; }
  .prompt-text { font-size: 13.5px; color: #47402f; line-height: 1.65; white-space: pre-wrap; }
  .file-name { margin-top: 12px; font-family: ui-monospace, Menlo, monospace; font-size: 11px;
               color: var(--dim); }
  .empty { text-align: center; padding: 60px 20px; color: var(--muted);
           border: 1px dashed var(--line-strong); border-radius: 14px;
           background: rgba(255,255,255,.6); display: none; }
  footer { margin-top: 48px; padding-top: 20px; border-top: 1px solid var(--line-strong);
           font-size: 12px; color: var(--dim); display: flex; justify-content: space-between;
           flex-wrap: wrap; gap: 8px; }
  @media (max-width: 640px) {
    .card-top { grid-template-columns: auto 1fr; }
    .actions { grid-column: 1 / -1; flex-direction: row; }
    .btn { flex: 1; }
  }
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="eyebrow">Collection · 100 studies</div>
    <h1>Fable 5.1 <span>100 HTML</span> Files</h1>
    <p class="lede">One hundred self-contained visual studies — generative art, physics, typography,
      interfaces and scenes — generated with Fable 5.1. Open any piece in a new tab, or expand a card
      to read the original generation prompt.</p>
  </header>

  <div class="toolbar">
    <div class="search">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>
      <input type="search" id="q" placeholder="Search by name, number, or prompt…" autocomplete="off" spellcheck="false">
    </div>
    <div class="count" id="count"><b>%N%</b> studies</div>
  </div>

  <div class="list" id="list">
%CARDS%
  </div>

  <div class="empty" id="empty">No studies match your search.</div>

  <footer>
    <span>Fable 5.1 · generated collection</span>
    <span>Nº 001–100</span>
  </footer>
</div>
<script>
(function () {
  var q = document.getElementById("q");
  var list = document.getElementById("list");
  var empty = document.getElementById("empty");
  var count = document.getElementById("count").querySelector("b");
  var cards = Array.prototype.slice.call(list.querySelectorAll(".card"));

  list.addEventListener("click", function (ev) {
    var btn = ev.target.closest(".btn-prompt");
    if (!btn) return;
    var open = btn.closest(".card").classList.toggle("open");
    btn.setAttribute("aria-expanded", open ? "true" : "false");
  });

  function apply() {
    var term = q.value.trim().toLowerCase(), shown = 0;
    cards.forEach(function (card) {
      var hit = !term || card.getAttribute("data-title").toLowerCase().indexOf(term) !== -1;
      card.style.display = hit ? "" : "none";
      if (hit) shown++;
    });
    count.textContent = shown;
    empty.style.display = shown ? "none" : "block";
  }
  q.addEventListener("input", apply);
  apply();
})();
</script>
</body>
</html>
""".replace("%N%", str(len(entries))).replace("%CARDS%", "\n".join(card(e) for e in entries))

out = os.path.join(DIR, "index.html")
open(out, "w", encoding="utf-8").write(page)
print("wrote", out, len(page), "bytes")
