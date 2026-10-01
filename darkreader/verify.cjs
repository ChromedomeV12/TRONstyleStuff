// npm install --no-save playwright darkreader@4.9.133 in a separate test directory.
// NODE_PATH may point there; DARKREADER_JS may specify the downloaded API bundle.
const {chromium} = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const assert = require('node:assert/strict');
const theme = JSON.parse(fs.readFileSync(path.join(__dirname, 'TRON.theme.json')));
const css = fs.readFileSync(path.join(__dirname, 'TRON.css'), 'utf8');
(async () => {
    const browser = await chromium.launch({channel: 'msedge', headless: true});
    try {
        const page = await browser.newPage({viewport: {width: 1200, height: 1120}});
        const errors = [];
        page.on('pageerror', e => errors.push(e.message));
        await page.goto(pathToFileURL(path.join(__dirname, 'preview.html')).href);
        await page.addScriptTag({path: process.env.DARKREADER_JS || require.resolve('darkreader')});
        const read = () => page.evaluate(() => {
            const nodes = ['h1', 'h2', '#link', '#inline', '#mark', '#token', '#media', 'aside', 'hr', '#button'];
            return Object.fromEntries(nodes.map(s => {
                const e = document.querySelector(s), c = getComputedStyle(e), r = e.getBoundingClientRect();
                return [s, {color: c.color, background: c.backgroundColor, border: c.borderRightColor,
                    filter: c.filter, rect: [r.x, r.y, r.width, r.height]}];
            }));
        });
        await page.evaluate(theme => DarkReader.enable(theme), theme);
        await page.waitForFunction(() => document.documentElement.dataset.darkreaderScheme === 'dark');
        await page.waitForTimeout(400);
        const base = await read();
        await page.evaluate(({theme, css}) => DarkReader.enable(theme, {css}), {theme, css});
        await page.waitForFunction(() => getComputedStyle(document.querySelector('h2')).color === 'rgb(0, 238, 238)');
        const tron = await read();
        assert.equal(tron.h1.color, 'rgb(216, 225, 221)');
        assert.equal(tron['#link'].color, 'rgb(111, 195, 223)');
        assert.equal(tron['#inline'].color, 'rgb(255, 140, 26)');
        assert.equal(tron['#mark'].color, 'rgb(255, 209, 102)');
        assert.equal(tron.aside.border, 'rgb(33, 117, 131)');
        for (const key of Object.keys(base)) assert.deepEqual(tron[key].rect, base[key].rect, `${key} layout`);
        assert.deepEqual(tron['#token'], base['#token'], 'code token preserved');
        assert.deepEqual(tron['#media'], base['#media'], 'media treatment preserved');
        await page.locator('#link').hover();
        assert.equal((await read())['#link'].color, 'rgb(255, 140, 26)');
        await page.mouse.move(0, 0);
        await page.locator('#field').focus();
        await page.keyboard.press('Tab');
        assert.equal(await page.locator('#button').evaluate(e => getComputedStyle(e).outlineColor), 'rgb(0, 238, 238)');
        await page.locator('#button').evaluate(e => e.blur());
        await page.screenshot({path: path.join(__dirname, 'preview.png'), fullPage: true});
        await page.evaluate(({theme, css}) => DarkReader.enable({...theme, mode: 0}, {css}), {theme, css});
        await page.waitForFunction(() => document.documentElement.dataset.darkreaderScheme === 'dimmed');
        assert.notEqual((await read()).h2.color, 'rgb(0, 238, 238)', 'overlay inactive in light mode');
        await page.evaluate(() => DarkReader.disable());
        assert.equal(await page.evaluate(() => document.documentElement.hasAttribute('data-darkreader-scheme')), false);
        assert.deepEqual(errors, []);
        console.log('PASS: Dark Reader 4.9.133 colors, hover, focus, unchanged layout/code/media, light mode and disable.');
    } finally {
        await browser.close();
    }
})().catch(e => {console.error(e); process.exitCode = 1;});
