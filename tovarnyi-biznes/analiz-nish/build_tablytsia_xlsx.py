import ast, json
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.comments import Comment
# --- дані з попередньої версії (рядки акаунтів, ключові слова)
tree=ast.parse(open('build_tpl6_data.py',encoding='utf-8').read())
calls=[n.value for n in tree.body if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and getattr(n.value.func,'id','')=='niche']
D={}
for c in calls:
    a=[ast.literal_eval(x) for x in c.args]; D[a[0]]=a
EX=json.load(open('example_ads.json',encoding='utf-8'))
# ключові слова на акаунт: лише ті, що видно в шапці профілю або в запиті, за яким знайдено
KW={'ksuu__store':'фен-браш, гофре, плойка','dezli.store':'фен-браш, плойка','verii.shop':'фен-браш, фен, стайлер, вирівнювач',
 'daviden.ua':'аерофритюрниця, аерогриль, фен','styler_shop_':'плойка, фен','terka.com.ua':'відпарювач','adalin.posh':'плойка, фен, стайлер',
 'cecotec.ua':'аерофритюрниця','gelius.ua':'навушники, смарт годинники','wookie.ua':'навушники','itbox.ua':'навушники',
 'comfy_ua':'плойка','cosmetics_v_store':'фен-браш','Art De Luxe Shop':'навушники, смарт годинники',
 'sumki.in.ukraine':'жіночі сумки, рюкзаки','likemood.ua':'жіночі сумки, рюкзаки, бананки','sumci_turkey':'жіночі сумки','sumka.in.ua':'жіночі сумки','bags_dnepr_':'сумки, валізи'}
# медіана переглядів рілса (тис.), останні рілси без закріплених, дані vidIQ 12.11.2026
VIEWS={'ksuu__store':19,'dezli.store':5,'verii.shop':2.6,'daviden.ua':3.7,'styler_shop_':13.9,'terka.com.ua':10.4,'adalin.posh':1.6,
 'sumki.in.ukraine':26.7,'likemood.ua':25.3,'sumka.in.ua':1.3,'bags_dnepr_':1.7}
LINK=Font(name='Arial',size=10,color='1155CC',underline='single')
F=lambda c: PatternFill('solid',start_color=c)
G,Y,R,H,K,S,P,O=F('B7E1CD'),F('FCE8B2'),F('F4C7C3'),F('CFF4F5'),F('FFF2CC'),F('EFEFEF'),F('FBE9E7'),F('F9CB9C')
A10=Font(name='Arial',size=10); B10=Font(name='Arial',size=10,bold=True)
c=Alignment(horizontal='center',vertical='center')
wb=Workbook(); wb.remove(wb.active)
NICHES=['ТОВАРИ ДЛЯ ДОМУ','СУМКИ, ЖІНОЧІ СУМКИ','НІША 3']
def dd(ws,rng,items):
    v=DataValidation(type='list',formula1='"'+','.join(items)+'"',allow_blank=True); ws.add_data_validation(v); v.add(rng)
def niche(title,idx):
    _,banner,keywords,rows=(D[title]+[()])[:4] if len(D[title])>=4 else (D[title]+[(),()])[:4]
    ws=wb.create_sheet(title)
    for x,t in (('A2','к-ть РО'),('B2','категорія')):
        ws[x]=t; ws[x].fill=H; ws[x].font=B10; ws[x].alignment=c
    for r,(a,b,f) in enumerate([('5+',1,G),('1-4',2,Y),('0',3,R)],3):
        x=ws.cell(r,1,a); x.alignment=c; x.font=A10
        y=ws.cell(r,2,b); y.fill=f; y.alignment=c; y.font=A10
    ws['D2']='НІША: '+NICHES[idx]; ws['D2'].fill=K; ws['D2'].font=Font(name='Arial',size=10,bold=True,italic=True); ws['D2'].alignment=c; ws.merge_cells('D2:I4')
    ws['L3']='контент який вони знімають'; ws['L3'].fill=H; ws['L3'].font=B10
    for r,t in enumerate(['із моделлю і обличчям','без обличчя','50/50'],4): ws.cell(r,12,t).font=A10
    ws['F6']='всього:'; ws['G6']='=COUNTA(F10:F109)'; ws['H6']='категорія 1:'; ws['I6']='=COUNTIF(D10:D109,1)'
    for x in ('F6','G6','H6','I6'): ws[x].font=A10
    ws['G6'].alignment=c; ws['I6'].alignment=c
    ws['A7']='Ключові Слова для пошуку'; ws['A7'].font=A10
    # як у шаблоні: список ніш, далі блок ключових слів своєї ніші
    for i,n in enumerate(NICHES): ws.cell(10+i,1,n).font=B10
    ws.cell(14,1,NICHES[idx]).font=B10; ws.cell(15,1,'ключові').font=A10
    r=16; first=True
    for k in keywords:
        if k in ('',None) and not first: r+=1; continue
        if k in ('',None): continue
        if k.isupper(): continue   # назва ніші вже виведена
        x=ws.cell(r,1,k); x.font=A10
        if first and not k.endswith(':'): x.fill=K; first=False
        r+=1
    heads=['н','категорія','ключове слово','назва','підписників','кількість РО','інстаграм','бібліотека','оголошення','контент який вони знімають','перегляди рілса, тис.','% від підписників']
    for i,h in enumerate(heads,3):
        x=ws.cell(9,i,h); x.fill=H; x.font=B10; x.alignment=c
    for n in range(1,31):
        x=ws.cell(9+n,3,n); x.alignment=Alignment(horizontal='right'); x.font=A10
    for rr in range(10,110):
        x=ws.cell(rr,4,f'=IF(ISNUMBER(H{rr}),IF(H{rr}>=5,1,IF(H{rr}>=1,2,3)),"")'); x.alignment=c; x.font=A10
        y=ws.cell(rr,14,f'=IF(AND(ISNUMBER(M{rr}),ISNUMBER(G{rr})),M{rr}/G{rr},"")'); y.number_format='0%'; y.font=A10; y.alignment=c
    for i,(kw,name,fol,ro,ig,lib,content,note) in enumerate(rows,10):
        ex=('https://www.facebook.com/ads/library/?id='+EX[name]) if name in EX else ''
        for col,v in ((5,KW.get(name,kw)),(6,name),(7,fol),(8,ro),(9,ig),(10,lib),(11,ex),(12,content),(13,VIEWS.get(name))):
            if v is not None and v!='':
                x=ws.cell(i,col,v); x.font=A10
                if col in (9,10,11) and str(v).startswith('http'): x.hyperlink=str(v); x.font=LINK
        if fol not in (None,''): ws.cell(i,7).number_format='0.0'; ws.cell(i,7).alignment=Alignment(horizontal='right')
        if note: ws.cell(i,8).comment=Comment(note,'')
    cf=ws.conditional_formatting
    cf.add('D10:D109',CellIsRule(operator='equal',formula=['1'],fill=G))
    cf.add('D10:D109',CellIsRule(operator='equal',formula=['2'],fill=Y))
    cf.add('D10:D109',CellIsRule(operator='equal',formula=['3'],fill=R))
    cf.add('F10:F109',FormulaRule(formula=['AND(F10<>"",COUNTIF($F$10:$F$109,F10)>1)'],fill=O))      # дубль акаунта
    cf.add('E10:E109 G10:J109 L10:L109',FormulaRule(formula=['AND($F10<>"",E10="")'],fill=P))        # неповний рядок
    dd(ws,'L10:L109',['із моделлю і обличчям','без обличчя','50/50'])
    for col,w in zip('ABCDEFGHIJKLMN',[26,13,6,11,38,22,13,14,18,18,18,28,22,18]): ws.column_dimensions[col].width=w
    ws.freeze_panes='A10'
niche('Товари для дому',0); niche('Сумки',1)
D['Ніша 3']=['Ніша 3','',[''],[]]; niche('Ніша 3',2)
wb.create_sheet('Робота із постачальниками')
# ---------- Замовлення
ws=wb.create_sheet('Замовлення')
for col,(t,f) in zip((1,3,5,7,9),[('замовлень','=COUNTA(C5:C504)'),('виручка, грн','=SUM(E5:E504)'),('середній чек, грн','=IFERROR(AVERAGE(E5:E504),"")'),('частка повторних','=IF(COUNTA(C5:C504)=0,"",COUNTIF(I5:I504,"так")/COUNTA(C5:C504))'),('відмов','=COUNTIF(H5:H504,"відмова")')]):
    ws.cell(1,col,t).font=B10; x=ws.cell(1,col+1,f); x.fill=S; x.alignment=c; x.font=A10
ws['H1'].number_format='0%'; ws['F1'].number_format='0'
for i,h in enumerate(['н','дата','клієнт','товар','сума','джерело','кампанія / оголошення','статус','повторний клієнт','примітка'],1):
    x=ws.cell(4,i,h); x.fill=H; x.font=B10; x.alignment=c
for n in range(1,31):
    x=ws.cell(4+n,1,n); x.font=A10; x.alignment=Alignment(horizontal='right')
for i,h in enumerate(['джерело','замовлень','виручка, грн'],12):
    x=ws.cell(4,i,h); x.fill=H; x.font=B10; x.alignment=c
for r,s in enumerate(['реклама','органіка','рекомендація','повторний'],5):
    ws.cell(r,12,s).font=A10
    for col,f in ((13,f'=COUNTIF($F$5:$F$504,L{r})'),(14,f'=SUMIF($F$5:$F$504,L{r},$E$5:$E$504)')):
        x=ws.cell(r,col,f); x.fill=S; x.alignment=c; x.font=A10
dd(ws,'F5:F504',['реклама','органіка','рекомендація','повторний'])
dd(ws,'H5:H504',['новий','в роботі','оплачено','відправлено','отримано','відмова'])
dd(ws,'I5:I504',['так','ні'])
for t,fl in (('отримано',G),('новий',Y),('відмова',R)):
    ws.conditional_formatting.add('H5:H504',CellIsRule(operator='equal',formula=[f'"{t}"'],fill=fl))
for col,w in zip('ABCDEFGHIJKLMN',[6,13,22,28,12,16,24,15,18,30,3,16,12,14]): ws.column_dimensions[col].width=w
ws.freeze_panes='A5'
wb.save('tablytsia_final.xlsx')
