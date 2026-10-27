"""Exportación PDF sin dependencias nuevas: reportlab y pypdf del entorno.

Markdown en docs/sqa/06-informes-finales es la fuente principal.
"""
from pathlib import Path
from html import escape
import re
import json
from xml.sax.saxutils import quoteattr
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, LongTable, TableStyle, Image, PageBreak, KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / 'output/pdf'
OUTPUT.mkdir(parents=True, exist_ok=True)
FONT = Path('C:/Windows/Fonts')
pdfmetrics.registerFont(TTFont('SQA-Regular', str(FONT / 'segoeui.ttf')))
pdfmetrics.registerFont(TTFont('SQA-Bold', str(FONT / 'segoeuib.ttf')))
pdfmetrics.registerFont(TTFont('SQA-Italic', str(FONT / 'segoeuii.ttf')))
pdfmetrics.registerFontFamily('SQA', normal='SQA-Regular', bold='SQA-Bold', italic='SQA-Italic', boldItalic='SQA-Bold')
INK = colors.HexColor('#26362f')
ACCENT = colors.HexColor('#234e43')
MUTED = colors.HexColor('#59665e')
LINE = colors.HexColor('#dce3dc')
styles = {
    'body': ParagraphStyle('body', fontName='SQA-Regular', fontSize=10, leading=14.2, textColor=INK, spaceAfter=7, splitLongWords=True),
    'h1': ParagraphStyle('h1', fontName='SQA-Bold', fontSize=22, leading=28, textColor=ACCENT, spaceAfter=18, keepWithNext=True),
    'h2': ParagraphStyle('h2', fontName='SQA-Bold', fontSize=14, leading=18, textColor=ACCENT, spaceBefore=15, spaceAfter=9, keepWithNext=True),
    'h3': ParagraphStyle('h3', fontName='SQA-Bold', fontSize=11, leading=15, textColor=INK, spaceBefore=11, spaceAfter=7, keepWithNext=True),
    'table': ParagraphStyle('table', fontName='SQA-Regular', fontSize=8.5, leading=11.8, textColor=INK, splitLongWords=True, spaceAfter=0),
    'table-head': ParagraphStyle('table-head', fontName='SQA-Bold', fontSize=8.4, leading=11.2, textColor=ACCENT, splitLongWords=True),
    'code': ParagraphStyle('code', fontName='Courier', fontSize=8, leading=11, textColor=INK, leftIndent=9, spaceAfter=4, splitLongWords=True),
    'caption': ParagraphStyle('caption', fontName='SQA-Italic', fontSize=8.5, leading=12, textColor=MUTED, spaceAfter=9),
}
WIDTH = A4[0] - 90
HEIGHT = A4[1] - 102
CURRENT_SOURCE = None
CURRENT_DESTINATION = None

def rendered_link(match):
    label, target = match.group(1), match.group(2)
    if '://' not in target and not target.startswith('#'):
        import os
        clean_target, _, anchor = target.partition('#')
        resolved = (CURRENT_SOURCE.parent / clean_target).resolve()
        target = os.path.relpath(resolved, CURRENT_DESTINATION.parent).replace('\\', '/')
        if anchor:
            target += '#' + anchor
    return '<link href='+quoteattr(target)+' color="#234e43"><u>'+label+'</u></link>'

def inline(text):
    text = text.replace('—', '-').replace('–', '-').replace('‑', '-')
    text = escape(text)
    text = re.sub(r'`([^`]+)`', lambda match: '<font face="SQA-Regular" color="#385949">'+match.group(1)+'</font>', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\[([^]]+)\]\(([^)]+)\)', rendered_link, text)
    return text

def p(text, kind='body'):
    return Paragraph(inline(text), styles[kind])

def table_widths(headers):
    n = len(headers)
    if n == 2: return [WIDTH*.21, WIDTH*.79]
    if n == 3:
        if headers[0] == 'Ref.': return [WIDTH*.07, WIDTH*.49, WIDTH*.44]
        return [WIDTH*.24, WIDTH*.25, WIDTH*.51]
    if n == 4:
        if headers == ['ID','Importancia','Descripción','Estado']: return [WIDTH*.1,WIDTH*.18,WIDTH*.47,WIDTH*.25]
        if headers[0] == 'CA': return [WIDTH*.08,WIDTH*.44,WIDTH*.13,WIDTH*.35]
        if headers[0] in ['CA','ID','N.º']: return [WIDTH*.08,WIDTH*.23,WIDTH*.13,WIDTH*.56]
        return [WIDTH*.2,WIDTH*.2,WIDTH*.17,WIDTH*.43]
    if n == 5: return [WIDTH*.42,WIDTH*.145,WIDTH*.145,WIDTH*.135,WIDTH*.135]
    if n == 6: return [WIDTH*.24,WIDTH*.14,WIDTH*.14,WIDTH*.16,WIDTH*.16,WIDTH*.16]
    return [WIDTH/n]*n

def footer(canvas, document):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.line(45, 40, A4[0]-45, 40)
    canvas.setFont('SQA-Regular', 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(45, 27, 'StockFácil | Evaluación técnica preliminar - validación independiente pendiente')
    canvas.drawRightString(A4[0]-45, 27, str(document.page))
    if document.page > 1:
        canvas.setFont('SQA-Bold', 8)
        canvas.setFillColor(ACCENT)
        canvas.drawString(45, A4[1]-28, document.report_label)
    canvas.restoreState()

def convert(source, destination, label):
    global CURRENT_SOURCE, CURRENT_DESTINATION
    CURRENT_SOURCE, CURRENT_DESTINATION = source, destination
    lines = source.read_text(encoding='utf-8').splitlines()
    flow = []
    index = 0
    while index < len(lines):
        line = lines[index].strip()
        if not line:
            index += 1
            continue
        if line.startswith('```'):
            index += 1
            while index < len(lines) and not lines[index].startswith('```'):
                flow.append(p(lines[index], 'code'))
                index += 1
            index += 1
            flow.append(Spacer(1, 8))
            continue
        if line.startswith('|'):
            rows=[]
            while index < len(lines) and lines[index].lstrip().startswith('|'):
                cells=[cell.strip() for cell in lines[index].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?', cell) for cell in cells): rows.append(cells)
                index += 1
            widths=table_widths(rows[0])
            formatted=[[p(value, 'table-head' if row_index==0 else 'table') for value in row] for row_index,row in enumerate(rows)]
            grid=LongTable(formatted,colWidths=widths,repeatRows=1,hAlign='LEFT')
            grid.setStyle(TableStyle([
                ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e9efe6')),
                ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f8faf6')]),
                ('VALIGN',(0,0),(-1,-1),'TOP'),
                ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),
                ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
                ('LINEBELOW',(0,0),(-1,0),.65,LINE),('LINEBELOW',(0,1),(-1,-1),.35,LINE),
            ]))
            flow.extend([grid,Spacer(1,10)])
            continue
        image = re.fullmatch(r'!\[([^]]*)\]\(([^)]+)\)',line)
        if image:
            file=(source.parent/image.group(2)).resolve()
            assert file.is_file(),file
            picture=Image(str(file))
            factor=min(WIDTH/picture.imageWidth,620/picture.imageHeight)
            picture.drawWidth=picture.imageWidth*factor
            picture.drawHeight=picture.imageHeight*factor
            picture.hAlign='LEFT'
            flow.extend([picture,Spacer(1,10)])
            index+=1
            continue
        heading=re.match(r'^(#{1,3})\s+(.*)',line)
        if heading:
            level=len(heading.group(1)); text=heading.group(2)
            if level==3 and (text.startswith('Figura ') or text.startswith('Captura:')):
                flow.append(PageBreak())
            flow.append(p(text, 'h'+str(level)))
            index+=1
            continue
        if line.startswith('- '):
            flow.append(Paragraph(inline(line[2:]),ParagraphStyle('bullet',parent=styles['body'],leftIndent=12,bulletIndent=0),bulletText='-'))
            index+=1
            continue
        paragraph=[line]
        index+=1
        while index<len(lines) and lines[index].strip() and not lines[index].lstrip().startswith(('#','|','- ','!','```')):
            paragraph.append(lines[index].strip());index+=1
        flow.append(p(' '.join(paragraph)))
    document=SimpleDocTemplate(str(destination),pagesize=A4,rightMargin=45,leftMargin=45,topMargin=48,bottomMargin=54,title=label,author='Elaboración técnica asistida con Codex; participantes académicos pendientes',pageCompression=1)
    document.report_label=label
    document.build(flow,onFirstPage=footer,onLaterPages=footer)
    reader=PdfReader(destination)
    text='\n'.join(page.extract_text() or '' for page in reader.pages)
    assert all(word in text for word in ['StockFácil','100%','pendiente']),destination
    assert not any(ord(char)==0xfffd for char in text)
    return {'file':str(destination.relative_to(ROOT)).replace('\\','/'),'pages':len(reader.pages),'characters':len(text),'source':str(source.relative_to(ROOT)).replace('\\','/')}

results=[]
for stem,label in [('informe-sqa-hu01','Informe SQA - HU-01 Registro de productos'),('informe-sqa-hu02','Informe SQA - HU-02 Control de existencias'),('informe-sqa-general','Informe general de aseguramiento de la calidad - StockFácil')]:
    results.append(convert(ROOT/f'docs/sqa/06-informes-finales/{stem}.md',OUTPUT/f'{stem}.pdf',label))
(ROOT/'docs/sqa/04-pruebas/evidencias/exportacion-pdf.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(results,ensure_ascii=False,indent=2))
