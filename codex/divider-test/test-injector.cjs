const assert = require('node:assert/strict');
const {applyStyle,connect} = require('./inject.cjs');
let style;
global.document = {
  getElementById: () => style,
  querySelector: () => ({}),
  querySelectorAll: selector => selector.startsWith('#') ? (style ? [style] : []) : [],
  createElement: () => ({remove(){ style=undefined; }}),
  head: {appendChild(value){style=value;}}
};
assert.equal(applyStyle('cyan').mainSurfaces,0);
assert.equal(applyStyle('orange').styleCount,1);
assert.equal(style.textContent,'orange');
assert.equal(applyStyle('',true).removed,true);
assert.equal(style,undefined);
(async()=>{
  await assert.rejects(connect('ws://example.com:9339/'),/Refusing/);
  await assert.rejects(connect('ws://127.0.0.1:9338/',9339),/Refusing/);
  console.log('Passed: shell without chat, idempotent CSS, removal, endpoint restrictions.');
})().catch(e=>{console.error(e);process.exitCode=1;});
