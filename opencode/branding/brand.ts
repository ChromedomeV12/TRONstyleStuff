import { banner } from './art';

// Exact signatures from OpenCode 2.0.27. Fail closed if upstream changes the logo.
const left = ['                   ', '█▀▀█ █▀▀█ █▀▀█ █▀▀▄', '█__█ █__█ █^^^ █__█', '▀▀▀▀ █▀▀▀ ▀▀▀▀ ▀~~▀'];
const right = ['             ▄     ', '█▀▀▀ █▀▀█ █▀▀█ █▀▀█', '█___ █__█ █__█ █^^^', '▀▀▀▀ ▀▀▀▀ ▀▀▀▀ ▀▀▀▀'];
const normalize = (text: string) => text.replace(/_/g, ' ').replace(/[\^~]/g, '▀').replace(/,/g, '▄').replace(/\s/g, '');
const signatures = new Set([
  normalize(left.map((line, i) => line + right[i]).join('')),
  normalize([...left.slice(1), ...right].join('')),
  normalize(['█▀▀█', '█__█', '▀▀▀▀'].join('')),
]);
function textOf(node: any): string {
  if (typeof node.plainText === 'string') return node.plainText;
  return (node.getChildren?.() ?? []).map(textOf).join('');
}
function findLogo(node: any): any {
  for (const child of node.getChildren?.() ?? []) {
    const match = findLogo(child);
    if (match) return match;
  }
  // Match a container, never a leaf text node or arbitrary application text.
  if (typeof node.plainText === 'string' || !node.getChildren?.().length) return;
  if (signatures.has(normalize(textOf(node)))) return node;
}
function firstText(node: any): any {
  if (typeof node.plainText === 'string') return node;
  for (const child of node.getChildren?.() ?? []) {
    const found = firstText(child);
    if (found) return found;
  }
}

export function installLogo(context: any) {
  const renderer = context.renderer;
  let original: any;
  let replacement: any;
  let lastWidth = -1;
  let lastHeight = -1;
  let disposed = false;
  const clear = () => {
    if (original && !original.isDestroyed) original.visible = true;
    replacement?.destroyRecursively();
    original = undefined; replacement = undefined;
  };
  const update = () => {
    if (disposed) return;
    if (context.ui.router.current().type !== 'home') { if (replacement) clear(); return; }
    if (original?.isDestroyed || replacement?.isDestroyed) clear();
    const width = renderer.width;
    const height = renderer.height;
    if (replacement && lastWidth === width && lastHeight === height) return;
    if (replacement) clear();
    const candidate = findLogo(renderer.root);
    if (!candidate?.parent) return;
    // Reuse the host's exact native classes. Discovered plugins do not receive
    // an @opentui/core module alias, and a second renderer copy is unnecessary.
    const Box = candidate.constructor;
    const Text = firstText(candidate)?.constructor;
    if (typeof Box !== 'function' || typeof Text !== 'function') return;
    const parent = candidate.parent;
    const index = parent.getChildren().indexOf(candidate);
    const art = banner(Math.max(1, width - 4), height);
    const contentWidth = Math.max(...art.map(line => line.content.length));
    const box = new Box(renderer, { id: 'tron-encomcode-logo', flexDirection: 'column', width: contentWidth, flexShrink: 0 });
    for (const [row, line] of art.entries()) {
      box.add(new Text(renderer, { id: 'tron-encomcode-line-' + row, content: line.content, fg: line.color, selectable: false }));
    }
    candidate.visible = false;
    parent.add(box, index + 1);
    original = candidate; replacement = box;
    lastWidth = width; lastHeight = height;
    renderer.requestRender();
  };
  // Work on existing frames; no timer, polling loop, service, or binary patch.
  renderer.on('frame', update);
  return () => {
    disposed = true;
    renderer.off('frame', update);
    clear();
    renderer.requestRender();
  };
}
