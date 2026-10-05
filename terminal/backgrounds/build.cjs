// Render the existing boardroom's code-native ENCOM mark with Chromium.
// Requires Playwright and Microsoft Edge; run: node build.cjs
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('playwright');

async function main() {
  const fontPath = path.resolve(__dirname, '../../encom-boardroom/css/terminator.woff');
  const font = fs.readFileSync(fontPath).toString('base64');
  const palette = JSON.parse(fs.readFileSync(path.resolve(__dirname, '../TRON-Legacy.json'), 'utf8'));
  const browser = await chromium.launch({ channel: 'msedge', headless: true });
  try {
    const page = await browser.newPage({ viewport: { width: 320, height: 128 }, deviceScaleFactor: 1 });
    await page.setContent(`<!doctype html><meta charset="utf-8"><style>
      @font-face { font-family: Terminator; src: url(data:font/woff;base64,${font}); }
      html, body { margin: 0; width: 100%; height: 100%; background: transparent; overflow: hidden; }
      /* Adapted from encom-boardroom/css/light-table-styles.css #lt-encom-logo. */
      .mark { position: absolute; right: 28px; bottom: 28px; padding: 11px 0 11px 12px;
        font: 28px/1 Terminator; color: ${palette.blue};
        border: 2px solid ${palette.brightCyan}; border-right: 0; border-radius: 8px 0 0 8px; }
    </style><div class="mark">ENCOM</div>`);
    await page.evaluate(() => document.fonts.ready);
    const bounds = await page.locator('.mark').boundingBox();
    if (!bounds || bounds.x < 12 || bounds.y < 12) throw new Error('Logo does not fit the sticker');
    await page.screenshot({ path: path.join(__dirname, 'encom-corner.png'), omitBackground: true });
    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.evaluate(background => { document.body.style.background = background; }, palette.background);
    await page.screenshot({ path: path.join(__dirname, 'encom-background-1920x1080.png') });
    await page.setViewportSize({ width: 960, height: 540 });
    await page.screenshot({ path: path.join(__dirname, 'preview.png') });
    console.log(JSON.stringify({ background: palette.background, sticker: [320, 128], logoBounds: bounds }));
  } finally { await browser.close(); }
}
main().catch(error => { console.error(error); process.exitCode = 1; });
