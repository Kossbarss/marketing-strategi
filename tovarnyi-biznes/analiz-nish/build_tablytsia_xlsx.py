from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.formatting.rule import CellIsRule
from openpyxl.worksheet.datavalidation import DataValidation
F=lambda c: PatternFill('solid',start_color=c)
G,Y,R,H,K=F('B7E1CD'),F('FCE8B2'),F('F4C7C3'),F('CFF4F5'),F('FFF2CC')
A10=Font(name='Arial',size=10); B10=Font(name='Arial',size=10,bold=True)
c=Alignment(horizontal='center',vertical='center')
wb=Workbook(); wb.remove(wb.active)
def dd(ws,rng,items):
    v=DataValidation(type='list',formula1='"'+','.join(items)+'"',allow_blank=True); ws.add_data_validation(v); v.add(rng)
def niche(title, banner, keywords):
    ws=wb.create_sheet(title)
    for x,t in (('A2','к-ть РО'),('B2','категорія')):
        ws[x]=t; ws[x].fill=H; ws[x].font=B10; ws[x].alignment=c
    for r,(a,b,f) in enumerate([('5+',1,G),('1-4',2,Y),('0',3,R)],3):
        x=ws.cell(r,1,a); x.alignment=c; x.font=A10
        y=ws.cell(r,2,b); y.fill=f; y.alignment=c; y.font=A10
    ws['D2']=banner; ws['D2'].fill=K; ws['D2'].font=Font(name='Arial',size=10,bold=True,italic=True); ws['D2'].alignment=c; ws.merge_cells('D2:I4')
    ws['K3']='контент який вони знімають'; ws['K3'].fill=H; ws['K3'].font=B10
    for r,t in enumerate(['із моделлю і обличчям','без обличчя','50/50'],4): ws.cell(r,11,t).font=A10
    ws['F6']='всього:'; ws['G6']='=COUNTA(F10:F109)'; ws['H6']='категорія 1:'; ws['I6']='=COUNTIF(D10:D109,1)'
    for x in ('F6','G6','H6','I6'): ws[x].font=A10
    ws['G6'].alignment=c; ws['I6'].alignment=c
    ws['A7']='Ключові Слова для пошуку'; ws['A7'].font=A10
    r=9
    for k in keywords:
        if k is None: r+=1; continue
        x=ws.cell(r,1,k); x.font=B10 if k.isupper() else A10; r+=1
    for i,h in enumerate(['н','категорія','ключове слово','назва','підписників','кількість РО','інстаграм','бібліотека','контент який вони знімають'],3):
        x=ws.cell(9,i,h); x.fill=H; x.font=B10; x.alignment=c
    for n in range(1,31):
        rr=9+n; x=ws.cell(rr,3,n); x.alignment=Alignment(horizontal='right'); x.font=A10
    for rr in range(10,110):
        x=ws.cell(rr,4,f'=IF(ISNUMBER(H{rr}),IF(H{rr}>=5,1,IF(H{rr}>=1,2,3)),"")'); x.alignment=c; x.font=A10
    ws.conditional_formatting.add('D10:D109',CellIsRule(operator='equal',formula=['1'],fill=G))
    ws.conditional_formatting.add('D10:D109',CellIsRule(operator='equal',formula=['2'],fill=Y))
    ws.conditional_formatting.add('D10:D109',CellIsRule(operator='equal',formula=['3'],fill=R))
    dd(ws,'K10:K109',['із моделлю і обличчям','без обличчя','50/50'])
    for col,w in zip('ABCDEFGHIJK',[24,13,13,13,18,22,13,14,18,18,28]): ws.column_dimensions[col].width=w
niche('Товари для дому','НІША: ТОВАРИ ДЛЯ ДОМУ',['ТОВАРИ ДЛЯ ДОМУ','копії:','навушники','смарт годинники','фітнес трекери','дайсон','dyson',None,'аерогриль','фен','фен-браш','вирівнювач','гофре','утюжок','відпарювач','аерофритюрниця'])
niche('Сумки','НІША: СУМКИ, ЖІНОЧІ СУМКИ',['СУМКИ','сумки','жіночі сумки'])
wb.create_sheet('Робота із постачальниками')
ws=wb.create_sheet('Замовлення')
for i,h in enumerate(['н','дата','клієнт','товар','сума','джерело','статус','повторний клієнт','примітка'],1):
    x=ws.cell(2,i,h); x.fill=H; x.font=B10; x.alignment=c
for n in range(1,31):
    x=ws.cell(2+n,1,n); x.font=A10; x.alignment=Alignment(horizontal='right')
dd(ws,'F3:F502',['реклама','органіка','рекомендація','повторний'])
dd(ws,'G3:G502',['новий','в роботі','оплачено','відправлено','отримано','відмова'])
dd(ws,'H3:H502',['так','ні'])
ws.conditional_formatting.add('G3:G502',CellIsRule(operator='equal',formula=['"отримано"'],fill=G))
ws.conditional_formatting.add('G3:G502',CellIsRule(operator='equal',formula=['"новий"'],fill=Y))
ws.conditional_formatting.add('G3:G502',CellIsRule(operator='equal',formula=['"відмова"'],fill=R))
for col,w in zip('ABCDEFGHI',[6,13,22,28,12,16,15,18,30]): ws.column_dimensions[col].width=w
wb.save('tablytsia_v3.xlsx')
