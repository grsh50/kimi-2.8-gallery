#!/usr/bin/env node
/* Capture thumbs/*.jpg for every numbered study with headless Chromium.
   Long wall-clock waits + a scroll pass so rAF canvases and scroll reveals render. */
const path = require("path");
const fs = require("fs");
const { chromium } = require("/home/zurih/.npm/_npx/e41f203b7505f1fb/node_modules/playwright");

const DIR = __dirname;
const CHROME = path.join(process.env.HOME, ".cache/ms-playwright/chromium-1228/chrome-linux/chrome");
const THUMBS = path.join(DIR, "thumbs");
fs.mkdirSync(THUMBS, { recursive: true });

const files = fs.readdirSync(DIR).filter(f => /^\d{3}-.+\.html$/.test(f)).sort();
const WAIT = 2800;                  // let idle animation / boot sequences settle
const VIEWPORT = { width: 1280, height: 800 };

(async () => {
  const only = process.argv[2] ? process.argv[2].split(",") : null;
  const browser = await chromium.launch({
    executablePath: CHROME,
    headless: true,
    args: ["--hide-scrollbars", "--no-sandbox", "--force-device-scale-factor=1"]
  });
  const page = await (await browser.newContext({ viewport: VIEWPORT, deviceScaleFactor: 1 })).newPage();
  const list = only ? files.filter(f => only.includes(f)) : files;
  for (const [i, f] of list.entries()) {
    const out = path.join(THUMBS, f.replace(/\.html$/, ".jpg"));
    try {
      await page.goto("file://" + encodeURI(path.join(DIR, f)), { waitUntil: "load", timeout: 20000 });
      await page.waitForTimeout(WAIT);
      await page.evaluate(async () => {          // trigger scroll reveals, then return
        for (let y = 0; y < document.documentElement.scrollHeight; y += 600) {
          window.scrollTo(0, y); await new Promise(r => setTimeout(r, 25));
        }
        window.scrollTo(0, 0);
      });
      await page.waitForTimeout(700);
      await page.screenshot({ path: out, type: "jpeg", quality: 82 });
      console.log(`[${i + 1}/${list.length}] ${f} -> ${fs.statSync(out).size} bytes`);
    } catch (e) {
      console.log(`FAIL ${f}: ${e.message}`);
    }
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
