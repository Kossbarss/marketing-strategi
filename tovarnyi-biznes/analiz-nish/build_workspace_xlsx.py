import csv
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.worksheet.datavalidation import DataValidation
F=lambda c: PatternFill('solid',start_color=c)
G,Y,R,H,K,S=F('B7E1CD'),F('FCE8B2'),F('F4C7C3'),F('CFF4F5'),F('FFF2CC'),F('EFEFEF')
bold=Font(bold=True); c=Alignment(horizontal='center',vertical='center',wrap_text=True); wrap=Alignment(wrap_text=True,vertical='top')
wb=Workbook(); wb.remove(wb.active)
def head(ws,row,col,names):
    for i,h in enumerate(names,col):
        x=ws.cell(row,i,h); x.fill=H; x.font=bold; x.alignment=c
def widths(ws,ws_):
    for i,w in enumerate(ws_):
        ws.column_dimensions[chr(65+i)].width=w
def dd(ws,rng,items):
    v=DataValidation(type='list',formula1='"'+','.join(items)+'"',allow_blank=True); ws.add_data_validation(v); v.add(rng)
N=['Дім','Сумки','Ніша 3']

# ---------- Старт
ws=wb.create_sheet('Старт')
ws['A1']='Товарний бізнес — робочий простір'; ws['A1'].font=Font(bold=True,size=14)
ws['A2']='Білі клітинки заповнюєте ви. Сірі рахуються самі — їх не чіпайте. Блакитні — заголовки.'; ws.merge_cells('A2:E2'); ws['A2'].fill=K
head(ws,4,1,['Крок','Що зробити','Де','Статус','Примітка'])
steps=[
('1','Створити профіль Instagram-магазину (назва будь-яка, зміните через 14 днів)','аркуш «Акаунти»'),
('2','Знайти або створити сторінку Facebook, увімкнути двофакторну автентифікацію','аркуш «Акаунти»'),
('3','Записати, на яку пошту й телефон зареєстровано акаунти (паролі — у менеджері паролів, не тут)','аркуш «Акаунти»'),
('4','Обрати три ніші для аналізу й вписати їх назви','аркуш «Порівняння ніш», стовпчик A'),
('5','З телефона: пошук в Instagram за кожним ключовим словом; відмітити пройдені слова','аркуші ніш, стовпчики A–B'),
('6','Занести колег: ключове слово, назва, підписники (тис.), посилання. Мінімум 30 на нішу, від 5 000 підписників','аркуші ніш, стовпчики E–G, I'),
('7','Бібліотека реклами: кількість активних оголошень і посилання. Немає реклами — 0; не знайшли — прочерк','аркуші ніш, стовпчики H, J'),
('8','Тип контенту кожного колеги — вибрати зі списку','аркуші ніш, стовпчик K'),
('9','Нові ключові слова із шапок профілів дописати у список і пройти їх','аркуші ніш, стовпчик A'),
('10','Порівняти ніші й записати висновок','аркуш «Порівняння ніш»'),
('11','Дати доступ редактора авторові й куратору та здати посилання','кнопка «Налаштування доступу»'),
]
for i,(n,t,w) in enumerate(steps,5):
    ws.cell(i,1,n).alignment=c; ws.cell(i,2,t).alignment=wrap; ws.cell(i,3,w).alignment=wrap; ws.cell(i,4,'не почато').alignment=c
dd(ws,'D5:D15',['не почато','в роботі','готово'])
ws.conditional_formatting.add('D5:D15',CellIsRule(operator='equal',formula=['"готово"'],fill=G))
ws.conditional_formatting.add('D5:D15',CellIsRule(operator='equal',formula=['"в роботі"'],fill=Y))
ws['B17']='Готово кроків'; ws['B17'].font=bold; ws['C17']='=COUNTIF(D5:D15,"готово")&" з "&COUNTA(A5:A15)'; ws['C17'].fill=S
ws['A19']='Правила категорій (з курсу)'; ws['A19'].font=bold
for i,(a,b,f) in enumerate([('5 і більше активних оголошень','категорія 1',G),('1–4 оголошення','категорія 2',Y),('0 оголошень','категорія 3',R)],20):
    ws.cell(i,2,a); x=ws.cell(i,3,b); x.fill=f
ws['A24']='Аркуші'; ws['A24'].font=bold
for i,(a,b) in enumerate([('Порівняння ніш','зведення по трьох нішах, рахується само'),('Дім / Сумки / Ніша 3','таблиці колег за шаблоном курсу'),('Акаунти','облік акаунтів без паролів (урок 8)'),('Замовлення','облік замовлень зі статусами і джерелом — знадобиться після запуску'),('Постачальники','заготовка, уточнимо після модуля про постачальників'),('Чернетка …','рекламодавці, знайдені в Бібліотеці реклами 11.11.2026; сировина, не для здачі')],25):
    ws.cell(i,2,a).font=bold; ws.cell(i,3,b)
widths(ws,[7,70,44,14,30]); ws.freeze_panes='A5'

# ---------- Порівняння ніш
ws=wb.create_sheet('Порівняння ніш')
ws['A1']='Порівняння ніш'; ws['A1'].font=Font(bold=True,size=14)
ws['A2']='Назву ніші впишіть у стовпчик B. Решта рахується з аркушів ніш.'; ws.merge_cells('A2:J2'); ws['A2'].fill=K
head(ws,4,1,['Аркуш','Ніша','Колег внесено','До мінімуму (30)','Категорія 1','Категорія 2','Категорія 3','Частка категорії 1','Середня к-ть РО в категорії 1','Без обличчя, колег','Мій висновок'])
names=['товари для дому','сумки, жіночі сумки','']
for i,(sh,nm) in enumerate(zip(N,names),5):
    q="'"+sh+"'!"
    ws.cell(i,1,sh); ws.cell(i,2,nm)
    fs=[f'=COUNTA({q}F10:F69)', f'=MAX(0,30-C{i})', f'=COUNTIF({q}D10:D69,1)', f'=COUNTIF({q}D10:D69,2)', f'=COUNTIF({q}D10:D69,3)',
        f'=IF(C{i}=0,"",E{i}/C{i})', f'=IFERROR(AVERAGEIF({q}D10:D69,1,{q}H10:H69),"")', f'=COUNTIF({q}K10:K69,"без обличчя")']
    for j,f in enumerate(fs,3):
        x=ws.cell(i,j,f); x.fill=S; x.alignment=c
    ws.cell(i,8).number_format='0%'; ws.cell(i,9).number_format='0.0'
ws['A9']='Як читати'; ws['A9'].font=bold
for i,t in enumerate(['Що більше колег категорії 1 і що вища їхня частка — то живіша ніша (урок 6).','Не робіть висновку, доки в ніші менше 30 колег.','Точного порога «скільки категорії 1 достатньо» курс не дає — остаточну оцінку роблять на розборі з куратором.','Кількість оголошень — непрямий показник: бюджети реклами в бібліотеці не видно.'],10):
    ws.cell(i,1,t); ws.merge_cells(start_row=i,start_column=1,end_row=i,end_column=11)
widths(ws,[10,24,14,16,13,13,13,16,20,16,44]); ws.freeze_panes='A5'

# ---------- аркуші ніш
def niche(title, label, groups, rows):
    ws=wb.create_sheet(title)
    ws['A1']='Ніша:'; ws['A1'].font=bold; ws['B1']=label; ws['B1'].font=Font(bold=True,size=12)
    ws['A2']='к-ть РО'; ws['B2']='категорія'
    for x in ('A2','B2'): ws[x].fill=H; ws[x].font=bold; ws[x].alignment=c
    for r,(a,b,f) in enumerate([('5+',1,G),('1-4',2,Y),('0',3,R)],3):
        ws.cell(r,1,a).alignment=c; x=ws.cell(r,2,b); x.fill=f; x.alignment=c
    ws['K2']='контент який вони знімають'; ws['K2'].fill=H; ws['K2'].font=bold
    for r,t in enumerate(['із моделлю і обличчям','без обличчя','50/50'],3): ws.cell(r,11,t)
    ws['D2']='Заповнюйте E–M. Категорія (D) рахується сама з «кількість РО». Підписники — у тисячах, як у курсі (36,8 = 36 800). Реклами немає — 0; сторінку в бібліотеці не знайдено — прочерк.'
    ws['D2'].fill=K; ws['D2'].alignment=Alignment(wrap_text=True,vertical='center'); ws.merge_cells('D2:I5')
    for col,(t,f) in zip((4,6,8,10),[('Колег внесено','=COUNTA(F10:F69)'),('Категорія 1','=COUNTIF(D10:D69,1)'),('Категорія 2','=COUNTIF(D10:D69,2)'),('Категорія 3','=COUNTIF(D10:D69,3)')]):
        ws.cell(7,col,t).font=bold; x=ws.cell(7,col+1,f); x.fill=S; x.alignment=c
    ws['A7']='Ключові слова для пошуку'; ws['A7'].font=bold; ws['B7']='пройдено?'; ws['B7'].font=bold
    r=8
    for gname,kws in groups:
        if gname: ws.cell(r,1,gname).font=Font(bold=True,italic=True); r+=1
        for k in kws: ws.cell(r,1,k); ws.cell(r,2,'ні').alignment=c; r+=1
    dd(ws,'B8:B69',['ні','так'])
    ws.conditional_formatting.add('B8:B69',CellIsRule(operator='equal',formula=['"так"'],fill=G))
    head(ws,9,3,['н','категорія','ключове слово','назва','підписників','кількість РО','інстаграм','бібліотека','контент який вони знімають','дата перевірки','куди веде реклама','примітки'])
    if r>9:  # keywords overlap header row in col A/B only — fine, header starts at C
        pass
    for n in range(1,61):
        rr=9+n; ws.cell(rr,3,n).alignment=c
        x=ws.cell(rr,4,f'=IF(H{rr}="","",IF(ISNUMBER(H{rr}),IF(H{rr}>=5,1,IF(H{rr}>=1,2,3)),""))'); x.alignment=c; x.fill=S
    for i,row in enumerate(rows,10):
        for col,v in zip((5,6,7,8,9,10,11,12,13,14),row):
            if v!='' and v is not None: ws.cell(i,col,v)
    ws.conditional_formatting.add('D10:D69',CellIsRule(operator='equal',formula=['1'],fill=G))
    ws.conditional_formatting.add('D10:D69',CellIsRule(operator='equal',formula=['2'],fill=Y))
    ws.conditional_formatting.add('D10:D69',CellIsRule(operator='equal',formula=['3'],fill=R))
    ws.conditional_formatting.add('G10:G69',FormulaRule(formula=['AND(ISNUMBER(G10),G10<5)'],fill=R))
    dd(ws,'K10:K69',['із моделлю і обличчям','без обличчя','50/50'])
    dd(ws,'M10:M69',['директ Instagram','профіль Instagram','сайт або лендинг','змішано'])
    widths(ws,[26,11,6,11,20,26,13,13,34,34,26,15,20,34]); ws.freeze_panes='A10'
L='https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=UA&search_type=page&view_all_page_id='
niche('Дім','товари для дому',[('копії',['навушники','смарт годинники','фітнес трекери','дайсон','dyson']),('техніка',['аерогриль','фен','фен-браш','вирівнювач','гофре','утюжок','відпарювач','аерофритюрниця'])],
 [['фен-браш','cosmetics_v_store','',162,'',L+'413979872482083','','2026-11-11','директ Instagram','з Бібліотеки реклами; підписників і контент дописати'],
  ['фен-браш','Со стор юа асн','',25,'',L+'104543875745596','','2026-11-11','директ Instagram','назва сторінки в бібліотеці; знайти профіль в Instagram']])
niche('Сумки','сумки, жіночі сумки',[('',['сумки','жіночі сумки']),('із шапок профілів (урок 6)',['шопери','гаманці','рюкзаки','брендові сумки','бананки'])],
 [['жіночі сумки','sumka.in.ua',36.8,18,'https://www.instagram.com/sumka.in.ua/','','без обличчя','','','приклад з уроку 6 — цифри застарілі, перевірити'],
  ['жіночі сумки','bagaura.ua',5.2,3,'https://www.instagram.com/bagaura.ua/','','50/50','','','приклад з уроку 6 — перевірити'],
  ['жіночі сумки','sumki.in.ukraine',210,3,'https://www.instagram.com/sumki.in.ukraine/','','50/50','','','приклад з уроку 6 — перевірити; у бібліотеці сторінка «Barbaris bags»'],
  ['жіночі сумки','sumci_turkey',109,2,'https://www.instagram.com/sumci_turkey/','','без обличчя','','','приклад з уроку 6 — перевірити'],
  ['жіночі сумки','lavanda_bags_',5.9,0,'https://www.instagram.com/lavanda_bags_/','','50/50','','','приклад з уроку 6 — перевірити'],
  ['жіночі сумки','Likemood.ua','',21,'',L+'650614318716815','','2026-11-11','профіль Instagram','з Бібліотеки реклами; підписників і контент дописати']])
niche('Ніша 3','',[('',[])],[])

# ---------- Акаунти
ws=wb.create_sheet('Акаунти')
ws['A1']='Облік акаунтів (урок 8)'; ws['A1'].font=Font(bold=True,size=14)
ws['A2']='Паролі сюди не вписуйте: таблицею ви ділитесь із куратором. Зберігайте їх у менеджері паролів, а тут лише позначте, де саме.'; ws.merge_cells('A2:H2'); ws['A2'].fill=R
head(ws,4,1,['Акаунт','Посилання / нік','Пошта реєстрації','Телефон реєстрації','Двофакторна автентифікація','Де зберігається пароль','Дата створення','Примітки'])
for i,a in enumerate(['Instagram-магазин','Facebook (особистий, для реклами)','Пошта Gmail','Telegram-бот для замовлень (пізніше)'],5): ws.cell(i,1,a)
dd(ws,'E5:E14',['так','ні']); ws.conditional_formatting.add('E5:E14',CellIsRule(operator='equal',formula=['"так"'],fill=G)); ws.conditional_formatting.add('E5:E14',CellIsRule(operator='equal',formula=['"ні"'],fill=R))
widths(ws,[36,32,28,22,26,28,16,36]); ws.freeze_panes='A5'

# ---------- Замовлення
ws=wb.create_sheet('Замовлення')
ws['A1']='Облік замовлень'; ws['A1'].font=Font(bold=True,size=14)
ws['A2']='Знадобиться після запуску. Ідея з lead-tracker-kit: кожне замовлення має статус і джерело — видно, яка реклама приносить гроші і скільки клієнтів повертається.'; ws.merge_cells('A2:L2'); ws['A2'].fill=K
for col,(t,f) in zip((1,3,5,7,9),[('Замовлень','=COUNTA(B8:B507)'),('Виручка, грн','=SUM(F8:F507)'),('Середній чек, грн','=IFERROR(AVERAGE(F8:F507),"")'),('Частка повторних','=IF(COUNTA(B8:B507)=0,"",COUNTIF(I8:I507,"так")/COUNTA(B8:B507))'),('Відмов і повернень','=COUNTIF(J8:J507,"відмова")+COUNTIF(J8:J507,"повернення")')]):
    ws.cell(4,col,t).font=bold; x=ws.cell(4,col+1,f); x.fill=S; x.alignment=c
ws['H4'].number_format='0%'; ws['F4'].number_format='0'
ws['A5']='Орієнтир автора курсу: повторні продажі близько 20% обороту (цифра з його слів).'
head(ws,7,1,['н','Дата','Клієнт (нік)','Товар','К-ть','Сума, грн','Джерело','Оголошення / креатив','Повторний клієнт','Статус','ТТН','Примітка'])
for n in range(1,31): ws.cell(7+n,1,n).alignment=c
dd(ws,'G8:G507',['реклама','органіка','повторний','рекомендація','блогер','інше'])
dd(ws,'I8:I507',['ні','так'])
dd(ws,'J8:J507',['новий','в роботі','оплачено','відправлено','отримано','відмова','повернення'])
ws.conditional_formatting.add('J8:J507',CellIsRule(operator='equal',formula=['"отримано"'],fill=G))
ws.conditional_formatting.add('J8:J507',CellIsRule(operator='equal',formula=['"відмова"'],fill=R))
ws.conditional_formatting.add('J8:J507',CellIsRule(operator='equal',formula=['"повернення"'],fill=R))
ws.conditional_formatting.add('J8:J507',CellIsRule(operator='equal',formula=['"новий"'],fill=Y))
widths(ws,[6,13,22,30,7,13,16,28,17,15,20,30]); ws.freeze_panes='A8'

# ---------- Постачальники
ws=wb.create_sheet('Постачальники')
ws['A1']='Постачальники'; ws['A1'].font=Font(bold=True,size=14)
ws['A2']='Заготовка. Шаблон курсу для цього аркуша ще не надано — стовпчики попередні, уточнимо після модуля про постачальників.'; ws.merge_cells('A2:J2'); ws['A2'].fill=K
head(ws,4,1,['н','Постачальник','Країна','Контакт / посилання','Товар','Ціна закупівлі','Мін. партія','Доставка, строк','Умови (дроп / опт)','Примітки'])
for n in range(1,21): ws.cell(4+n,1,n).alignment=c
dd(ws,'C5:C104',['Україна','Китай','інша']); dd(ws,'I5:I104',['дроп','опт','дроп і опт'])
widths(ws,[6,28,12,34,28,16,13,20,18,34]); ws.freeze_panes='A5'

# ---------- чернетки
import os; B=os.path.dirname(os.path.abspath(__file__))+'/'
for title,fn in (('Чернетка дім','tovary-dlia-domu-reklamodavtsi.csv'),('Чернетка сумки','sumky-reklamodavtsi.csv')):
    ws=wb.create_sheet(title)
    ws['A1']='Чернетка: рекламодавці з Бібліотеки реклами Meta, перевірено 2026-11-11. «≥N» — щонайменше N оголошень у вибірці з 30; точна кількість може бути більшою. Не для здачі: перевірте в Instagram і перенесіть потрібних на аркуш ніші.'
    ws.merge_cells('A1:M1'); ws['A1'].alignment=Alignment(wrap_text=True); ws['A1'].fill=K; ws.row_dimensions[1].height=45
    for i,row in enumerate(csv.reader(open(B+fn,encoding='utf-8')),2):
        for j,v in enumerate(row,1):
            x=ws.cell(i,j,v)
            if i==2: x.fill=H; x.font=bold; x.alignment=c
    widths(ws,[5,11,24,30,12,12,12,40,14,14,24,26,16]); ws.freeze_panes='A3'
wb.save('workspace.xlsx'); print([s.title for s in wb])
