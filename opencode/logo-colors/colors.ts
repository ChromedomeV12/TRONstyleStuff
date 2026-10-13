// Recognition patterns only: the plugin never creates or replaces any artwork.
const left=['                   ','█▀▀█ █▀▀█ █▀▀█ █▀▀▄','█__█ █__█ █^^^ █__█','▀▀▀▀ █▀▀▀ ▀▀▀▀ ▀~~▀'];
const right=['             ▄     ','█▀▀▀ █▀▀█ █▀▀█ █▀▀█','█___ █__█ █__█ █^^^','▀▀▀▀ ▀▀▀▀ ▀▀▀▀ ▀▀▀▀'];
type Cell={char:string;fg:string;bg?:string};
const group=(rows:string[],fg:string,shadow:string):Cell[] => rows.flatMap(row=>[...row].map(char=>({
  char:char==='_'?' ':char==='^'||char==='~'?'▀':char===','?'▄':char,
  fg:char==='~'||char===','?shadow:fg,
  ...(char==='_'||char==='^'?{bg:shadow}:{}),
})));
const blue='#6FC3DF', cyan='#00EEEE', blueShadow='#203B47', cyanShadow='#04464B';
const variants=[
  left.flatMap((row,i)=>[...group([row],blue,blueShadow),...group([right[i]],cyan,cyanShadow)]),
  [...group(left.slice(1),blue,blueShadow),...group(right,cyan,cyanShadow)],
  group(['█▀▀█','█__█','▀▀▀▀'],cyan,cyanShadow),
];
function leaves(node:any):any[] {
  if(typeof node.plainText==='string') return [node];
  return (node.getChildren?.()??[]).flatMap(leaves);
}
function find(node:any):{nodes:any[];cells:Cell[]}|undefined {
  for(const child of node.getChildren?.()??[]) {const found=find(child);if(found)return found;}
  if(typeof node.plainText==='string'||!node.getChildren?.().length)return;
  const nodes=leaves(node), text=nodes.map(n=>n.plainText).join('');
  const cells=variants.find(cells=>cells.map(c=>c.char).join('')===text);
  if(cells)return {nodes,cells};
}
export function installColors(context:any) {
  const renderer=context.renderer;
  const painted=new Map<any,{fg:any;bg:any}>();
  let previous:any[]=[];
  let width=-1,height=-1;
  const restore=()=>{
    for(const [node,color] of painted)if(!node.isDestroyed){node.fg=color.fg;node.bg=color.bg;}
    painted.clear();previous=[];
  };
  const update=()=>{
    if(context.ui.router.current().type!=='home'){if(painted.size)restore();return;}
    if(painted.size&&width===renderer.width&&height===renderer.height&&previous.every(node=>!node.isDestroyed))return;
    const found=find(renderer.root);
    if(!found)return;
    if(found.nodes.length===previous.length&&found.nodes.every((node,i)=>node===previous[i]))return;
    // Grouped text leaves must have one uniform color; otherwise fail closed.
    let offset=0;
    const changes=found.nodes.map(node=>{
      const cells=found.cells.slice(offset,offset+node.plainText.length);offset+=node.plainText.length;
      return {node,color:cells[0],uniform:cells.every(c=>c.fg===cells[0]?.fg&&c.bg===cells[0]?.bg)};
    });
    if(changes.some(change=>!change.uniform||!change.color))return;
    restore();
    for(const {node,color} of changes){
      painted.set(node,{fg:node.fg,bg:node.bg});node.fg=color.fg;
      if(color.bg)node.bg=color.bg;
    }
    previous=found.nodes;width=renderer.width;height=renderer.height;renderer.requestRender();
  };
  renderer.on('frame',update);
  return ()=>{renderer.off('frame',update);restore();renderer.requestRender();};
}
