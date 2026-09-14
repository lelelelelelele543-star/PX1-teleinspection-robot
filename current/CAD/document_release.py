"""Build both current PDFs from the master mesh and authoritative tables."""
from pathlib import Path
import csv,json,gzip,hashlib,re,html,os,xml.etree.ElementTree as ET
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Image,KeepTogether
from reportlab.graphics.shapes import Drawing,Rect,String,Path as GraphicsPath
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4,landscape,A3
import fitz
R=Path(__file__).resolve().parents[1];I=R/'images';I.mkdir(exist_ok=True)
for n,f in [('DV','DejaVuSans.ttf'),('DVB','DejaVuSans-Bold.ttf')]:pdfmetrics.registerFont(TTFont(n,'/usr/share/fonts/truetype/dejavu/'+f))
styles=getSampleStyleSheet()
for s in styles.byName.values():s.fontName='DV'
styles['BodyText'].fontSize=9;styles['BodyText'].leading=13
for h,sz in [('Heading1',17),('Heading2',12)]:styles[h].fontName='DVB';styles[h].fontSize=sz;styles[h].leading=sz+5
styles.add(ParagraphStyle('Small',fontName='DV',fontSize=7,leading=10,wordWrap='CJK'))
val=json.loads((R/'PX1_Current_Validation.json').read_text());registry=json.loads((R/'component_registry.json').read_text())
reuse_images=os.environ.get('PX1_DOCS_EXISTING_IMAGES')=='1'
original_drawings=(R/'PX1_Drawings_Current.pdf').read_bytes() if reuse_images else None
if reuse_images: meshes=[]
else:
    with gzip.open(I/'assembly_mesh.json.gz','rt') as f:meshes=json.load(f)
with (R/'PX1_Current_BOM.csv').open(encoding='utf-8-sig') as f:bom=list(csv.DictReader(f,delimiter=';'))
def p(t,style='BodyText'):
    t=html.escape(str(t)).replace(chr(96),'')
    t=re.sub(r'\[([^]]+)\]\((https?://[^)]+)\)',r'<link href="\2" color="#17627d">\1</link>',t)
    t=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',t)
    return Paragraph(t,styles[style])
def footer(c,d):
    c.setFont('DV',7);c.setFillColor(colors.HexColor('#65717a'))
    c.drawString(42,25,'PX1 Current · Rev.C · 14.09.2026 · HOLD / не производственный выпуск')
    c.drawRightString(A4[0]-42,25,str(d.page))
def table(rows,widths):
    t=Table([[p(x,'Small') for x in row] for row in rows],colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e4edf0')),('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),.25,colors.HexColor('#bbc8cf')),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
    return t
def markdown(text):
    result=[];lines=text.splitlines();k=0
    while k<len(lines):
        line=lines[k].strip();k+=1
        if not line:result.append(Spacer(1,5));continue
        if line.startswith('|'):
            block=[line]
            while k<len(lines) and lines[k].strip().startswith('|'):block.append(lines[k].strip());k+=1
            rows=[[v.strip() for v in x.strip('|').split('|')] for x in block if not re.match(r'^\|[\s:|\-]+\|$',x)]
            if rows:result.append(table(rows,[510/len(rows[0])]*len(rows[0])))
            continue
        style='Heading1' if line.startswith('# ') else 'Heading2' if line.startswith('## ') else 'BodyText'
        result.append(p(re.sub(r'^#+\s*','',line),style))
    return result
def view(selected,name,basis=((1,0,0),(0,0,1)),pipe=False):
    if reuse_images:
        fn=I/(name+'.png')
        if not fn.is_file():raise FileNotFoundError(fn)
        return fn
    u=np.array(basis[0],float);u/=np.linalg.norm(u)
    v=np.array(basis[1],float);v-=u*np.dot(v,u);v/=np.linalg.norm(v)
    depth=np.cross(u,v);faces=[];cols=[];zs=[];points=[]
    for m in selected:
        vertices=np.asarray(m['vertices']);tri=np.asarray(m['triangles'],dtype=int)
        if not len(tri):continue
        xyz=vertices[tri];xy=np.stack((xyz@u,xyz@v),axis=-1)
        norms=np.cross(xyz[:,1]-xyz[:,0],xyz[:,2]-xyz[:,0])
        norms/=np.maximum(1e-10,np.linalg.norm(norms,axis=1))[:,None]
        shade=.68+.3*np.abs(norms@np.array([.35,-.45,.82]))
        faces.append(xy);cols.append(np.clip(np.asarray(m['color'])[None,:]*shade[:,None],0,1));zs.append((xyz@depth).mean(axis=1));points.append(vertices@np.stack((u,v),axis=1))
    faces=np.concatenate(faces);cols=np.concatenate(cols);zs=np.concatenate(zs);pts=np.concatenate(points);order=np.argsort(zs)
    fig,ax=plt.subplots(figsize=(11.5,5),dpi=150)
    ax.add_collection(PolyCollection(faces[order],facecolors=cols[order],edgecolors='none',rasterized=True))
    if pipe:
        theta=np.linspace(0,2*np.pi,721);ax.plot(75*np.cos(theta),val['dn150']['assumed_pipe_center_z_mm']+75*np.sin(theta),color='#aa2437',lw=1.4,label='DN150')
        pts=np.vstack([pts,[[-75,-23],[75,128]]]);ax.legend(loc='upper right')
    lo=pts.min(axis=0);hi=pts.max(axis=0);pad=np.maximum((hi-lo)*.07,3)
    ax.set_xlim(lo[0]-pad[0],hi[0]+pad[0]);ax.set_ylim(lo[1]-pad[1],hi[1]+pad[1]);ax.set_aspect('equal')
    ax.set_xlabel('mm');ax.set_ylabel('mm');ax.grid(alpha=.13);fig.tight_layout()
    fn=I/(name+'.png');fig.savefig(fn,facecolor='white');plt.close(fig);return fn
allview=view(meshes,'PX1_Assembly_Isometric',((1,-.8,0),(.32,.4,1)))
inner=[m for m in meshes if m['category'] in ('purchased','electronics','electronics_hold','bearing','bevel','gear','shaft') and 'ACE' not in m['id']]
innerview=view(inner,'PX1_Drive_Electronics',((1,0,0),(0,1,0)))
sideview=view([m for m in meshes if 'Z50_-1' in m['id'] or '61903_SIDE_-1' in m['id'] or '61801_SIDE_-1' in m['id']],'PX1_Side_Drive')
liftview=view([m for m in meshes if m['category'] in ('lift','camera','cable','connector') or 'ACE' in m['id']],'PX1_Lift_Camera')
pipeview=view(meshes,'PX1_DN150',((0,1,0),(0,0,1)),True)
story=[p('PX1 · текущий комплект','Heading1'),p('Механический эталон — Proteus CRP-150. Собственная электроника на готовых модулях.','Heading2'),Image(str(allview),width=510,height=222),p('СТАТУС: HOLD. Это реконструкция по доступным источникам с явно обозначенными неразрешёнными сопряжениями. Полная сборка к изготовлению и эксплуатации не выпущена.'),p('Успешный экспорт не означает PASS конструкции.'),p('Геометрическая проверка','Heading2')]
rigid=[x for x in val['interferences'] if x['classification']=='RIGID_INTERFERENCE']
story.append(table([['Проверка','Результат'],['Объекты сборки',val['component_count']],['Ключевые количества',str(val['counts_match'])+'; '+str(val['counts'])],['Невалидные формы',str(val['invalid_shapes'])],['Все пары / Boolean',str(val['collision_method']['all_pairs'])+' / '+str(val['collision_method']['boolean_pairs_after_AABB'])],['Жёсткие пересечения',len(rigid)],['DN150','HOLD'],['Сервис моторов',val['service']['motor_vertical_extraction']['status']],['Съём камеры',val['service']['camera_forward_removal']['status']+'; дискретный screen'],['Металл','К изготовлению не выпущен'],['STL','4 примерочных файла']],[180,330]));story.append(PageBreak())
def schematic(path):
    # These two repository-owned SVGs use only rect/path/text. Explicitly embed
    # DejaVu in every text object: a CSS fallback silently lost Cyrillic in svglib.
    root=ET.parse(path).getroot();w=float(root.get('width'));h=float(root.get('height'))
    drawing=Drawing(w,h);rects=[]
    for el in root:
        tag=el.tag.split('}')[-1]
        if tag=='rect' and el.get('class')=='box':rects.append(el)
    for el in root:
        tag=el.tag.split('}')[-1];cl=el.get('class','')
        if tag=='rect':
            x=float(el.get('x',0));y=float(el.get('y',0));ww=float(el.get('width'));hh=float(el.get('height'))
            drawing.add(Rect(x,h-y-hh,ww,hh,rx=float(el.get('rx',0)),ry=float(el.get('rx',0)),fillColor=colors.HexColor('#eff4f6') if cl=='box' else colors.white,strokeColor=colors.HexColor('#617784') if cl=='box' else None,strokeWidth=1.5))
        elif tag=='path':
            tokens=re.findall(r'[A-Za-z]|[-+]?(?:\d*\.\d+|\d+)',el.get('d'));k=0;cmd=None;x=y=0;gp=GraphicsPath(strokeColor=colors.HexColor(el.get('stroke','#347b94')),fillColor=None,strokeWidth=2.5)
            while k<len(tokens):
                if tokens[k].isalpha():cmd=tokens[k];k+=1
                if cmd=='M':x=float(tokens[k]);y=float(tokens[k+1]);k+=2;gp.moveTo(x,h-y);cmd='L'
                elif cmd=='L':x=float(tokens[k]);y=float(tokens[k+1]);k+=2;gp.lineTo(x,h-y)
                elif cmd=='H':x=float(tokens[k]);k+=1;gp.lineTo(x,h-y)
                elif cmd=='V':y=float(tokens[k]);k+=1;gp.lineTo(x,h-y)
                else:raise ValueError('Unsupported schematic path command: '+str(cmd))
            drawing.add(gp)
        elif tag=='text':
            x=float(el.get('x'));y=float(el.get('y'));s=''.join(el.itertext())
            font='DVB' if cl=='title' else 'DV';size=25 if cl=='title' else 17
            available=w-x-25
            for rr in rects:
                rx=float(rr.get('x'));ry=float(rr.get('y'));rw=float(rr.get('width'));rh=float(rr.get('height'))
                if rx<=x<rx+rw and ry<=y<=ry+rh:available=rx+rw-x-8;break
            measured=pdfmetrics.stringWidth(s,font,size)
            if measured>available:size*=available/measured
            drawing.add(String(x,h-y,s,fontName=font,fontSize=size,fillColor=colors.HexColor('#182d39')))
    factor=510/w;drawing.scale(factor,factor);drawing.width=510;drawing.height=h*factor
    return drawing
for fn in ('ELECTRICAL_Current.md','ASSEMBLY_AND_TESTS_Current.md','SOURCE_REGISTER.md'):
    sv='PX1_Electrical_Current.svg' if fn=='ELECTRICAL_Current.md' else 'PX1_Pressure_Sealing_Current.svg' if fn=='ASSEMBLY_AND_TESTS_Current.md' else None
    if sv:
        drawing=schematic(R/sv)
        story.append(drawing);story.append(Spacer(1,14))
    story.extend(markdown((R/fn).read_text()));story.append(PageBreak())
story.append(p('Единственная текущая BOM','Heading1'));story.append(p(str(len(bom))+' строк: известный состав, незавершённые позиции и отдельные примерочные макеты. UNKNOWN/HOLD не является заказным артикулом. Цены и наличие в разрешённых магазинах не подтверждены.'))
for label,rows in [('Покупные и стандартные',[b for b in bom if b['route'] in ('BUY','SOURCE_PART')]),('Токарь / фрезеровщик / зубонарезание',[b for b in bom if b['route'] not in ('BUY','SOURCE_PART','PRINT')]),('Печатные макеты',[b for b in bom if b['route']=='PRINT'])]:
    story.append(p(label,'Heading2'));tb=[['ID / шт','Деталь / артикул','Размер / источник','Статус']]
    tb += [[b['item']+' / '+b['qty'],b['name_ru']+' · '+b['article'],b['dimensions']+' · '+b['source'],b['cad_state']+'; '+b['release']] for b in rows]
    story.append(table(tb,[47,176,167,120]));story.append(Spacer(1,12))
story.append(PageBreak());story.append(p('Оставшиеся конкретные неизвестные','Heading1'))
story.append(table([['ID','Узел','Что неизвестно / что блокирует']]+[[h['id'],h['title'],h['required']+' Блокирует: '+h['blocks']] for h in val['holds']],[30,130,350]))
story.append(PageBreak());story.append(p('Все жёсткие пересечения','Heading1'))
story.append(p('Контакты уплотнений, зацепления и резьбы не скрыты. Полный перечень, ошибки Boolean и доступ инструмента - в единственном PX1_Current_Validation.json.'))
story.append(table([['A','B','Объём mm³']]+[[r['a'],r['b'],r['volume_mm3']] for r in rigid],[222,222,66]))
SimpleDocTemplate(str(R/'PX1_Documentation_Current.pdf'),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=40,bottomMargin=42).build(story,onFirstPage=footer,onLaterPages=footer)
W,H=landscape(A3);c=canvas.Canvas(str(R/'PX1_Drawings_Current.pdf'),pagesize=(W,H));page=0
def sheet(title,notes):
    global page
    page+=1;c.setStrokeColor(colors.HexColor('#536571'));c.rect(20,20,W-40,H-40)
    c.setFont('DVB',14);c.drawString(38,H-47,title[:108])
    c.setFont('DV',9);c.setFillColor(colors.HexColor('#a02735'));c.drawString(38,H-65,'HOLD · НЕ ДЛЯ ИЗГОТОВЛЕНИЯ · размеры CAD не заменяют заводские допуски')
    c.setFillColor(colors.black);c.line(20,92,W-20,92);y=75
    for line in notes:c.setFont('DV',9);c.drawString(38,y,line[:170]);y-=14
    c.setFont('DV',8);c.drawRightString(W-38,36,'PX1 Current / Rev.C / лист '+str(page))
for title,im,notes in [('Общий вид PX1',allview,['Все размеры в мм. Покупные STEP не масштабированы.','6 колёс, X50/X150/X250, 5×Z50 на борт, задний X250 приводной.']),('Приводы и собственная электроника',innerview,['Корпус скрыт только на этом виде. В проверке участвуют все детали.','Проводка, крепёж и изоляция плат не завершены.']),('Боковая передача',sideview,['B4 подтверждено. m1 выведен из шага50. Профиль20° условный.','61801: 1на борт и ещё2на валахZ16.']),('Ручной лифт и камера',liftview,['Два боковых звена и центральное ASS002723: около200мм. БазыHOLD.','Газовая пружина150N; локальный жгут6жил.']),('Поперечная проекция DN150',pipeview,['Красный круг: Ø150. Включены все компоненты.','Реальный профиль шины и контакт с трубой неизвестны. PASS отсутствует.'])]:
    sheet(title,notes);c.drawImage(str(im),50,120,width=W-100,height=H-215,preserveAspectRatio=True,anchor='c');c.showPage()
byid={m['id']:m for m in meshes};reg={r['id']:r for r in registry}
for idx,(name,path) in enumerate(val['part_exports'].items(),1):
    rr=reg[name];im=view([] if reuse_images else [byid[name]],'part_%03d'%idx,((1,-.8,0),(.32,.4,1)))
    dims=' × '.join('%.3f'%x for x in rr['dimensions_mm'])
    sheet('Деталь '+str(idx)+' · '+name,['Габарит XYZ модели: '+dims+' мм. STEP в координатах сборки.','Посадки, шероховатость, материал и термообработка не выпущены.','Файл: '+path])
    c.drawImage(str(im),50,120,width=W-100,height=H-215,preserveAspectRatio=True,anchor='c');c.showPage()
c.save()
if original_drawings is not None:(R/'PX1_Drawings_Current.pdf').write_bytes(original_drawings)
qa=[]
for old in I.glob('PX1_*_Current_QA_*.png'):old.unlink()
for fn in ('PX1_Documentation_Current.pdf','PX1_Drawings_Current.pdf'):
    d=fitz.open(R/fn);blank=[]
    for i,pg in enumerate(d):
        if len(pg.get_text().strip())<20:blank.append(i+1)
        pix=pg.get_pixmap(matrix=fitz.Matrix(.6,.6))
        if i in (0,len(d)-1):pix.save(I/(fn.replace('.pdf','')+'_QA_%03d.png'%(i+1)))
    assert not blank,(fn,blank)
    qa.append({'file':fn,'pages':len(d),'rendered_pages':len(d),'blank_pages':blank,'human_visual_review':'NOT_PERFORMED_IN_REMOTE_RECOVERY'})
val['documentation_QA']=qa
(R/'PX1_Current_Validation.json').write_text(json.dumps(val,ensure_ascii=False,indent=2))
manifest=['PX1 CURRENT / Rev.C / 2026-09-14','MANUFACTURING RELEASE: HOLD','One master, one BOM, one validation, one changelog.','Part sheets show CAD bounding dimensions, not complete machining drawings.']
for fn in sorted(R.rglob('*')):
    if fn.is_file() and fn.suffix in ('.step','.stl','.pdf','.csv','.json','.py','.md','.svg') and '__pycache__' not in str(fn):
        manifest.append(hashlib.sha256(fn.read_bytes()).hexdigest()+'  '+str(fn.relative_to(R)))
(R/'PX1_RELEASE_MANIFEST.txt').write_text('\n'.join(manifest)+'\n')
print('Documentation emitted',qa,flush=True)
