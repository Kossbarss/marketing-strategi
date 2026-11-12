from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.formatting.rule import CellIsRule
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.comments import Comment
F=lambda c: PatternFill('solid',start_color=c)
G,Y,R,H,K=F('B7E1CD'),F('FCE8B2'),F('F4C7C3'),F('CFF4F5'),F('FFF2CC')
A10=Font(name='Arial',size=10); B10=Font(name='Arial',size=10,bold=True)
c=Alignment(horizontal='center',vertical='center')
wb=Workbook(); wb.remove(wb.active)
def dd(ws,rng,items):
    v=DataValidation(type='list',formula1='"'+','.join(items)+'"',allow_blank=True); ws.add_data_validation(v); v.add(rng)
def niche(title, banner, keywords, rows=()):
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
    for i,(kw,name,fol,ro,ig,lib,content,note) in enumerate(rows,10):
        for col,v in ((5,kw),(6,name),(7,fol),(8,ro),(9,ig),(10,lib),(11,content)):
            if v is not None and v!='': 
                x=ws.cell(i,col,v); x.font=A10
        if fol is not None and fol!='': ws.cell(i,7).number_format='0.0'; ws.cell(i,7).alignment=Alignment(horizontal='right')
        if note: ws.cell(i,8).comment=Comment(note,'')
    ws.conditional_formatting.add('D10:D109',CellIsRule(operator='equal',formula=['1'],fill=G))
    ws.conditional_formatting.add('D10:D109',CellIsRule(operator='equal',formula=['2'],fill=Y))
    ws.conditional_formatting.add('D10:D109',CellIsRule(operator='equal',formula=['3'],fill=R))
    dd(ws,'K10:K109',['із моделлю і обличчям','без обличчя','50/50'])
    for col,w in zip('ABCDEFGHIJK',[24,13,13,13,18,22,13,14,18,18,28]): ws.column_dimensions[col].width=w
niche('Товари для дому','НІША: ТОВАРИ ДЛЯ ДОМУ',['ТОВАРИ ДЛЯ ДОМУ','копії:','навушники','смарт годинники','фітнес трекери','дайсон','dyson',None,'аерогриль','фен','фен-браш','вирівнювач','гофре','утюжок','відпарювач','аерофритюрниця'],[('фен-браш', 'ksuu__store', 723.7, None, 'https://www.instagram.com/ksuu__store/', 'https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=UA&search_type=page&view_all_page_id=101232031238358', '50/50', 'Бачив щонайменше 4 оголошення; точне число — зі скриншота Бібліотеки реклами.'), ('фен-браш', 'dezli.store', 31.2, 11, 'https://www.instagram.com/dezli.store/', 'https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=UA&search_type=page&view_all_page_id=103082896054249', '50/50', 'Сторінка в бібліотеці називається Dezli_market. Перевірено 12.11.2026.'), ('фен-браш', 'verii.shop', 22.2, 9, 'https://www.instagram.com/verii.shop/', 'https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=UA&search_type=page&view_all_page_id=103510324833506', '50/50', 'Перевірено 12.11.2026.'), ('аерофритюрниця', 'daviden.ua', 10, None, 'https://www.instagram.com/daviden.ua/', 'https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=UA&search_type=page&view_all_page_id=185889211273739', 'без обличчя', 'Бачив щонайменше 1 оголошення; точне число — зі скриншота.'), ('плойка', 'styler_shop_', 102.8, None, 'https://www.instagram.com/styler_shop_/', 'https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=UA&search_type=page&view_all_page_id=114918324847834', 'із моделлю і обличчям', 'Бачив щонайменше 3 оголошення; точне число — зі скриншота.'), ('відпарювач', 'terka.com.ua', 274.4, None, 'https://www.instagram.com/terka.com.ua/', 'https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=UA&search_type=page&view_all_page_id=905789992892579', '50/50', 'Бачив щонайменше 3 оголошення; точне число — зі скриншота.'), ('плойка', 'adalin.posh', 35.2, 8, 'https://www.instagram.com/adalin.posh/', 'https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=UA&search_type=page&view_all_page_id=356386747560904', 'із моделлю і обличчям', 'Щонайменше 8 оголошень (бачив 8 у вибірці); точне число — зі скриншота.'), ('аерофритюрниця', 'cecotec.ua', 90.2, None, 'https://www.instagram.com/cecotec.ua/', 'https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=UA&search_type=page&view_all_page_id=108532907564330', '', 'Бачив щонайменше 3 оголошення; точне число — зі скриншота.'), ('навушники', 'gelius.ua', 76.8, None, 'https://www.instagram.com/gelius.ua/', 'https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=UA&search_type=page&view_all_page_id=348708312635450', '', 'Бачив щонайменше 3 оголошення; точне число — зі скриншота.'), ('навушники', 'wookie.ua', 6.9, None, 'https://www.instagram.com/wookie.ua/', 'https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=UA&search_type=page&view_all_page_id=211344865650700', '', 'Бачив щонайменше 2 оголошення; точне число — зі скриншота.'), ('навушники', 'itbox.ua', 6.5, None, 'https://www.instagram.com/itbox.ua/', 'https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=UA&search_type=page&view_all_page_id=208626165891330', '', 'Бачив щонайменше 1 оголошення; точне число — зі скриншота.'), ('плойка', 'comfy_ua', 304.9, 5, 'https://www.instagram.com/comfy_ua/', 'https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=UA&search_type=page&view_all_page_id=134105919952663', '', 'Щонайменше 5 оголошень (бачив 5 у вибірці); точне число — зі скриншота.'), ('', 'rezatto_com.ua', 169.6, None, 'https://www.instagram.com/rezatto_com.ua/', 'https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=UA&search_type=keyword_unordered&q=rezatto', '', ''), ('фен-браш', 'cosmetics_v_store', None, 162, '', 'https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=UA&search_type=page&view_all_page_id=413979872482083', '', '162 оголошення станом на 11.11.2026. Нік в Instagram не знайдено.'), ('навушники', 'Art De Luxe Shop', None, 17, '', 'https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=UA&search_type=page&view_all_page_id=112028044722633', '', 'Щонайменше 17 оголошень (бачив 17 у вибірці). Нік в Instagram не знайдено.')])
niche('Сумки','НІША: СУМКИ, ЖІНОЧІ СУМКИ',['СУМКИ','сумки','жіночі сумки'],[('жіночі сумки', 'sumki.in.ukraine', 214.2, None, 'https://www.instagram.com/sumki.in.ukraine/', 'https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=UA&search_type=keyword_unordered&q=Barbaris%20bags', '', ''), ('жіночі сумки', 'likemood.ua', 198.3, 21, 'https://www.instagram.com/likemood.ua/', 'https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=UA&search_type=page&view_all_page_id=650614318716815', '', '21 оголошення станом на 11.11.2026.'), ('жіночі сумки', 'sumci_turkey', 110.8, None, 'https://www.instagram.com/sumci_turkey/', 'https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=UA&search_type=keyword_unordered&q=Sumci_shop_turkey', '', ''), ('жіночі сумки', 'sumka.in.ua', 43.1, None, 'https://www.instagram.com/sumka.in.ua/', 'https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=UA&search_type=keyword_unordered&q=sumka.in.ua', '', ''), ('сумки', 'bags_dnepr_', 39.8, None, 'https://www.instagram.com/bags_dnepr_/', 'https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=UA&search_type=keyword_unordered&q=bags_dnepr_', '', '')])
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
wb.save('tablytsia_v4.xlsx')
