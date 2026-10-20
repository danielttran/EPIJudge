"""Original deterministic SVG diagrams tied directly to the first public example."""
import html,json,math
from oracle import tree
from generate import ROOT

COLORS=['#2563eb','#16a34a','#9333ea','#ea580c','#0891b2','#be123c']
class Drawing:
    def __init__(self,title,height=440):self.height=height;self.parts=[f'<title>{html.escape(title)}</title>', '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#64748b"/></marker></defs>', '<rect width="960" height="100%" fill="#f8fafc"/>'];self.text(28,32,title,20,'#0f172a')
    def text(self,x,y,text,size=16,color='#334155',anchor='start'):
        self.parts.append(f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" fill="{color}" text-anchor="{anchor}">{html.escape(str(text))}</text>')
    def line(self,x,y,u,v,color='#64748b',arrow=False):self.parts.append(f'<path d="M{x} {y}L{u} {v}" fill="none" stroke="{color}" stroke-width="2"'+(' marker-end="url(#arrow)"' if arrow else '')+'/>')
    def box(self,x,y,value,color='#2563eb',width=48,height=38):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="6" fill="white" stroke="{color}" stroke-width="2"/>');self.text(x+width/2,y+height/2+6,value,17,color,'middle')
    def finish(self):return '<svg xmlns="http://www.w3.org/2000/svg" role="img" viewBox="0 0 960 '+str(self.height)+'">'+''.join(self.parts)+'</svg>\n'

def draw_tree(d,values,x0,y0,width=420,highlight=None):
    root=tree(values)
    if not root:d.text(x0+width/2,y0+45,'empty tree',16,anchor='middle');return
    def depth(n):return 1+max(depth(n.left),depth(n.right)) if n else 0
    spacing=min(58,190/max(1,depth(root)-1))
    def visit(n,left,right,y):
        x=(left+right)/2
        for child,l,r,label in [(n.left,left,x,'L'),(n.right,x,right,'R')]:
            if child:
                cx=(l+r)/2;d.line(x,y+17,cx,y+spacing-17,arrow=True);d.text((x+cx)/2+4,y+spacing/2,label,11)
                visit(child,l,r,y+spacing)
        color='#be123c' if n.val==highlight else '#2563eb'
        d.parts.append(f'<circle cx="{x}" cy="{y}" r="19" fill="white" stroke="{color}" stroke-width="2"/>');d.text(x,y+6,n.val,16,color,'middle')
    visit(root,x0+10,x0+width-10,y0+35)

def draw_list(d,values,x0,y0,pos=-1,label='',colors=None):
    d.text(x0,y0,label,16);n=len(values)
    if not n:d.text(x0,y0+44,'empty list');return
    width=min(56,720/max(n,1));gap=20
    for i,v in enumerate(values):
        x=x0+i*(width+gap);d.box(x,y0+22,v,COLORS[(colors[i] if colors else i)%len(COLORS)],width);d.text(x+width/2,y0+77,f'index {i}',11,anchor='middle')
        if i+1<n:d.line(x+width+2,y0+41,x+width+gap-3,y0+41,arrow=True)
    end=x0+(n-1)*(width+gap)+width/2
    if pos>=0:
        dest=x0+pos*(width+gap)+width-5;d.parts.append(f'<path d="M{end} {y0+62}V{y0+110}H{dest}V{y0+62}" fill="none" stroke="#be123c" stroke-width="2" marker-end="url(#arrow)"/>');d.text((end+dest)/2,y0+129,f'tail links to index {pos}',13,'#be123c','middle')
    else:d.text(end+width/2+12,y0+47,'null',13)

def grid(d,rows,x0,y0,marked=(),islands=False):
    m,n=len(rows),len(rows[0]);size=min(58,340/max(m,n));marked=set(map(tuple,marked))
    for r in range(m):
        for c in range(n):
            color='#16a34a' if (r,c) in marked else '#2563eb';d.box(x0+c*size,y0+r*size,rows[r][c],color,size-4,size-4)
    d.text(x0,y0+m*size+19,'Rows and columns are zero-based.',12)

def graph(d,n,edges,x0,y0,width=420,directed=False):
    if n==0:d.text(x0+20,y0+50,'empty graph');return
    radius=min(135,width/2-40);points=[]
    for i in range(n):
        angle=-math.pi/2+2*math.pi*i/n;points.append((x0+width/2+radius*math.cos(angle),y0+145+radius*math.sin(angle)))
    for u,v in edges:
        x,y=points[u];xx,yy=points[v];dx,dy=xx-x,yy-y;dist=math.hypot(dx,dy)
        if dist:d.line(x+dx/dist*22,y+dy/dist*22,xx-dx/dist*24,yy-dy/dist*24,arrow=directed)
    for i,(x,y) in enumerate(points):d.parts.append(f'<circle cx="{x}" cy="{y}" r="20" fill="white" stroke="{COLORS[i%6]}" stroke-width="2"/>');d.text(x,y+6,i+1 if x0<0 else i,17,COLORS[i%6],'middle')

def make(s):
    case=json.loads((ROOT/'blind75/cases'/f'{s["id"]}.json').read_text())[0];a,e=case['arguments'],case['expected'];m=s['method'];mode=s['mode'];d=Drawing(s['title']);alt=''
    if m in ('Rotate','SpiralOrder','SetZeroes','PacificAtlantic','Exist','FindWords','NumIslands'):
        d.text(30,66,'Input');grid(d,a[0],35,88, e if m=='PacificAtlantic' else ())
        if m in ('Rotate','SetZeroes'):d.text(500,66,'After mutation');grid(d,e,505,88)
        else:
            out=json.dumps(e,ensure_ascii=True);d.text(470,118,'Result',18)
            for i in range(0,len(out),43):d.text(470,150+i//43*24,out[i:i+43],15)
            if m=='Exist':d.text(470,245,'Word: '+a[1]);d.text(470,274,'Use adjacent cells; never reuse a cell.',14)
            if m=='PacificAtlantic':d.text(470,270,'Green cells can reach both oceans.',14);d.text(35,355,'Pacific: top and left. Atlantic: bottom and right.',14)
            if m=='FindWords':d.text(470,260,'Dictionary: '+', '.join(a[1]),14)
            if m=='NumIslands':d.text(470,240,'Only horizontal and vertical neighbors connect.',14)
        alt=f'Example 1: grid {json.dumps(a[0])}; result {json.dumps(e)}.'
    elif mode.startswith('list_'):
        d.height=470
        if m=='MergeKLists':
            offset=0;entries=[]
            for i,row in enumerate(a[0]):
                ids=list(range(offset,offset+len(row)));draw_list(d,row,35,65+i*100,label=f'Input list {i}',colors=ids);entries.extend(zip(row,ids));offset+=len(row)
            draw_list(d,e,500,190,label='Merged list',colors=[i for _,i in sorted(entries)])
        elif m=='MergeTwoLists':
            draw_list(d,a[0],35,65,label='list1');draw_list(d,a[1],35,210,label='list2',colors=list(range(len(a[0]),len(a[0])+len(a[1]))));entries=list(zip(a[0]+a[1],range(len(a[0])+len(a[1]))));draw_list(d,e,430,135,label='Merged list',colors=[i for _,i in sorted(entries)])
        elif mode=='list_cycle':draw_list(d,a[0],40,80,pos=a[1],label='Input nodes');d.text(40,300,'Has cycle: '+str(e).lower(),19)
        else:
            ids=list(range(len(a[0])))
            if m=='ReverseList':ids.reverse()
            elif m=='RemoveNthFromEnd':ids.pop(len(ids)-a[1])
            elif m=='ReorderList':ids=[v for i in range((len(ids)+1)//2) for v in ([i,len(ids)-1-i] if i!=len(ids)-1-i else [i])]
            draw_list(d,a[0],35,70,label='Before');draw_list(d,e,35,260,label='After (colors follow original nodes)',colors=ids)
        alt=f'Example 1: list input {json.dumps(a)}; result {json.dumps(e)}. Boxes are distinct nodes even when values repeat.'
    elif any(p['type']=='tree' for p in s['params']) or m=='BuildTree':
        d.height=450
        if m=='BuildTree':d.text(30,70,'Preorder: '+json.dumps(a[0]));d.text(30,103,'Inorder: '+json.dumps(a[1]));draw_tree(d,e,450,100);d.text(500,83,'Reconstructed tree')
        else:
            d.text(30,67,'Input tree');draw_tree(d,a[0],15,78,highlight=e if mode=='tree_node' else None)
            if mode in ('tree_inplace','tree_codec'):d.text(515,67,'After' if mode=='tree_inplace' else 'Restored copy');draw_tree(d,e,495,78)
            elif m in ('IsSameTree','IsSubtree'):d.text(515,67,'Second tree');draw_tree(d,a[1],495,78);d.text(35,380,'Result: '+str(e).lower(),19)
            else:d.text(505,145,'Result: '+json.dumps(e),19)
            if mode=='tree_node':d.text(505,190,f'p = {a[1]}, q = {a[2]}; return the red original node.',14)
        alt=f'Example 1: breadth-first tree input {json.dumps(a)}; result {json.dumps(e)}. L and R mark child direction.'
    elif mode=='graph_clone':
        n=len(a[0]);edges=[(i,v-1) for i,row in enumerate(a[0]) for v in row if i<v-1]
        # graph() uses zero-based labels; override labels below by explicitly drawing shifted captions.
        d.text(30,70,'Original labels 1..n');d.text(510,70,'New nodes, same labels and edges')
        for x0 in (0,480):
            radius=100;points=[(x0+220+radius*math.cos(-math.pi/2+2*math.pi*i/n),220+radius*math.sin(-math.pi/2+2*math.pi*i/n)) for i in range(n)]
            for i,j in edges:d.line(*points[i],*points[j])
            for i,(x,y) in enumerate(points):d.parts.append(f'<circle cx="{x}" cy="{y}" r="22" fill="white" stroke="{COLORS[i%6]}" stroke-width="2"/>');d.text(x,y+6,i+1,18,anchor='middle')
        alt=f'Example 1: original and separate copy both have adjacency {json.dumps(e)}; neither shares node objects.'
    elif m in ('CanFinish','CountComponents','ValidTree'):
        edges=[(b,a1) for a1,b in a[1]] if m=='CanFinish' else [tuple(row) for row in a[1]]
        graph(d,a[0],edges,5,75,directed=m=='CanFinish');d.text(510,150,'Result: '+json.dumps(e),21)
        if m=='CanFinish':d.text(500,210,'Arrow: prerequisite → dependent course.',15)
        alt=f'Example 1: {a[0]} vertices with '+('prerequisite pairs ' if m=='CanFinish' else 'undirected edges ')+json.dumps(a[1])+f'; result {json.dumps(e)}.'
    elif m in ('Insert','Merge','EraseOverlapIntervals','CanAttendMeetings','MinMeetingRooms'):
        rows=a[0]+([a[1]] if m=='Insert' else []);scale=65
        for i,(start,end) in enumerate(rows):
            y=100+i*55;d.line(40+start*scale,y,40+end*scale,y,COLORS[i%6]);d.box(40+start*scale-15,y-16,start,COLORS[i%6],30,32);d.box(40+end*scale-15,y-16,end,COLORS[i%6],30,32)
        d.text(35,330,'Result: '+json.dumps(e),20);d.text(35,365,'Closed intervals merge at shared endpoints.' if m in ('Insert','Merge') else 'A meeting may start when another ends.',15)
        alt=f'Example 1: intervals {json.dumps(a)}; result {json.dumps(e)}. Endpoint semantics follow the problem statement.'
    elif m=='MaxArea':
        h=a[0];scale=45;base=300
        for i,v in enumerate(h):d.line(75+i*95,base,75+i*95,base-v*scale,'#2563eb');d.text(75+i*95,base+27,i,14,anchor='middle');d.text(75+i*95,base-v*scale-12,v,16,anchor='middle')
        d.line(45,base,420,base);d.text(500,160,'Best area: '+str(e),23);d.text(500,205,'Width 3 × shorter height 2 = 6.',17)
        alt='Example 1: heights [3,1,4,2]. The first and last segments enclose area 3 times 2, which is 6.'
    elif m=='ReverseBits':
        before=f'{a[0]:032b}';after=f'{e:032b}';d.text(40,110,'Input, all 32 bits');d.text(40,155,before,24);d.text(40,230,'Reversed, all 32 bits');d.text(40,275,after,24);d.text(40,340,f'{a[0]} becomes {e}',20);alt=f'Example 1: all 32 bits of {a[0]} reverse to {e}, including leading zeros.'
    else:return None
    d.text(28,d.height-18,'Original local illustration • Example 1 • No external assets',11,'#64748b')
    return d.finish(),alt

if __name__=='__main__':
    catalog=json.loads((ROOT/'blind75/catalog.json').read_text());out=ROOT/'EpiJudge.Web/wwwroot/blind75';out.mkdir(parents=True,exist_ok=True);manifest=[]
    for s in catalog:
        result=make(s)
        if result:
            svg,alt=result;path=out/(s['id']+'.svg');path.write_text(svg);manifest.append(dict(id=s['id'],path='/blind75/'+path.name,alt=alt))
    (ROOT/'blind75/diagrams.json').write_text(json.dumps(manifest,indent=2)+'\n');print('Generated',len(manifest),'original diagrams')
