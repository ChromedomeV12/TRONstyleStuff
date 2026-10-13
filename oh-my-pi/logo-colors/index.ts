import type { ExtensionAPI } from '@oh-my-pi/pi-coding-agent';

// Palette of the actual standalone Oh-My-Pi 18.10.3 welcome renderer.
const original = [[248,79,204],[147,98,244],[0,219,228]];
const tron = [[35,126,181],[111,195,223],[0,238,238]];
const indexed = new Map([[206,31],[170,38],[134,74],[99,45],[69,51],[74,87],[44,159]]);

// Recover the original gradient position and white shine from its RGB triangle.
// Repaint that position using blue/cyan stops, retaining the native shine.
export function recolorRGB(rgb: number[]): number[] {
  let best = { error: Infinity, segment: 0, fraction: 0, shine: 0 };
  for (let i = 0; i < original.length - 1; i++) {
    const a = original[i], b = original[i+1];
    const v = b.map((x,k) => x-a[k]), w = a.map(x => 255-x), p = rgb.map((x,k) => x-a[k]);
    const dot = (x: number[], y: number[]) => x.reduce((sum,n,k) => sum+n*y[k],0);
    const vv=dot(v,v), ww=dot(w,w), vw=dot(v,w), vp=dot(v,p), wp=dot(w,p);
    const det=vv*ww-vw*vw;
    let u=Math.max(0,(vp*ww-wp*vw)/det), s=Math.max(0,(wp*vv-vp*vw)/det);
    if (u+s>1) { const total=u+s; u/=total; s/=total; }
    const error=rgb.reduce((sum,x,k) => sum+(x-a[k]-u*v[k]-s*w[k])**2,0);
    if(error<best.error) best={error,segment:i,fraction:s>=.999?0:u/(1-s),shine:s};
  }
  const a=tron[best.segment], b=tron[best.segment+1];
  return a.map((x,k) => Math.round((x+(b[k]-x)*best.fraction)*(1-best.shine)+255*best.shine));
}

export function recolorLine(line: string): string {
  return line.replace(/\x1b\[38;2;(\d+);(\d+);(\d+)m(?=[▀█▒▄]\x1b\[0m)/g,
    (_all,r,g,b) => '\x1b[38;2;'+recolorRGB([+r,+g,+b]).join(';')+'m')
    .replace(/\x1b\[38;5;(\d+)m(?=[▀█▒▄]\x1b\[0m)/g,
      (all,n) => indexed.has(+n)?'\x1b[38;5;'+indexed.get(+n)+'m':all);
}

function findWelcome(node: any): any {
  if (typeof node?.playIntro==='function' && typeof node?.retargetIntro==='function'
    && typeof node?.setVersion==='function' && typeof node?.render==='function') return node;
  for(const child of node?.children ?? []) { const found=findWelcome(child); if(found) return found; }
}

export function installColors(tui: any): () => void {
  let welcome: any, native: any;
  const cache=new WeakMap<string[],string[]>();
  const attach=() => {
    if(welcome) return;
    const candidate=findWelcome(tui);
    if(!candidate) return;
    welcome=candidate; native=candidate.render;
    welcome.render=function(width: number) {
      const rows=native.call(this,width);
      const saved=cache.get(rows); if(saved) return saved;
      const start=rows.findIndex((line: string) => line.replace(/\x1b\[[0-9;]*m/g,'').trim()==='████████████');
      if(start<0) return rows;
      const painted=rows.map((line: string,index: number) => index>=start&&index<start+5?recolorLine(line):line);
      cache.set(rows,painted); return painted;
    };
    welcome.invalidate();
  };
  attach();
  // The zero-row widget calls this once if session_start precedes welcome mounting.
  return Object.assign(() => { if(welcome?.render && native) { welcome.render=native; welcome.invalidate(); } }, { attach });
}

export default function(pi: ExtensionAPI) {
  pi.on('session_start', async (_event,ctx) => {
    if(!ctx.hasUI) return;
    ctx.ui.setWidget('tron-original-logo-colors', tui => {
      const dispose=installColors(tui) as (()=>void)&{attach:()=>void};
      return {render(){dispose.attach();return [];},invalidate(){},dispose};
    });
  });
}
