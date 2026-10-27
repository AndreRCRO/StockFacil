"""Exporta el plan sencillo y sus capturas reales al mismo archivo Word."""
import re
from pathlib import Path
from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from PIL import Image

root = Path(__file__).resolve().parents[1]
docs = root / 'docs'
document = Document()
section = document.sections[0]
section.page_width, section.page_height = Cm(21), Cm(29.7)
section.top_margin, section.bottom_margin = Cm(2), Cm(1.8)
section.left_margin = section.right_margin = Cm(2)
for style in ['Normal', 'Title', 'Subtitle', 'Heading 1', 'Heading 2', 'Heading 3']:
    document.styles[style].font.name = 'Arial'
    document.styles[style].font.color.rgb = RGBColor(0, 0, 0)
    for border in document.styles[style].element.xpath('./w:pPr/w:pBdr'):
        border.getparent().remove(border)
document.styles['Normal'].font.size = Pt(11)
document.styles['Normal'].paragraph_format.space_after = Pt(7)
document.styles['Normal'].paragraph_format.line_spacing = 1.1
document.styles['Title'].font.size = Pt(25)
for style, size in [('Heading 1', 16), ('Heading 2', 12.5), ('Heading 3', 11)]:
    document.styles[style].font.size = Pt(size)
    document.styles[style].font.bold = True
    document.styles[style].paragraph_format.space_before = Pt(14)
    document.styles[style].paragraph_format.space_after = Pt(7)
    document.styles[style].paragraph_format.keep_with_next = True

def inline(paragraph, text):
    for part in re.split(r'(\*\*.*?\*\*|`.*?`|\[[^\]]+\]\([^)]+\))', text):
        if part.startswith('**'):
            paragraph.add_run(part[2:-2]).bold = True
        elif part.startswith('`'):
            run = paragraph.add_run(part[1:-1])
            run.font.name, run.font.size = 'Consolas', Pt(9)
        elif (link := re.fullmatch(r'\[([^\]]+)\]\(([^)]+)\)', part)):
            hyperlink = OxmlElement('w:hyperlink')
            hyperlink.set(qn('r:id'), paragraph.part.relate_to(link[2], RT.HYPERLINK, is_external=True))
            run = OxmlElement('w:r')
            properties = OxmlElement('w:rPr')
            color = OxmlElement('w:color')
            color.set(qn('w:val'), '245B75')
            properties.append(color)
            run.append(properties)
            value = OxmlElement('w:t')
            value.text = link[1]
            run.append(value)
            hyperlink.append(run)
            paragraph._p.append(hyperlink)
        else:
            paragraph.add_run(part)

def screenshot(label, relative_path):
    source = docs / relative_path
    # Word recorta márgenes y navegación; el PNG original se incrusta sin modificar.
    focus = {
        'CP-03-producto-creado.png': (270, 108, 1090, 488),
        'CP-06-stock-insuficiente.png': (270, 104, 960, 770),
        'CP-07-alerta-minimo.png': (270, 300, 1090, 651),
    }
    with Image.open(source) as bitmap:
        width, height = bitmap.size
    left, top, right, bottom = focus[source.name]
    if document.paragraphs:
        document.paragraphs[-1].paragraph_format.keep_with_next = True
    paragraph = document.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.paragraph_format.space_after = Pt(10)
    display_width = 14.5 if source.name == 'CP-06-stock-insuficiente.png' else 17
    picture = paragraph.add_run().add_picture(str(source), width=Cm(display_width),
                                             height=Cm(display_width * (bottom - top) / (right - left)))
    rectangle = OxmlElement('a:srcRect')
    for side, value in {'l': left / width, 't': top / height,
                        'r': (width - right) / width, 'b': (height - bottom) / height}.items():
        rectangle.set(side, str(round(value * 100000)))
    picture._inline.xpath('.//pic:blipFill')[0].insert(1, rectangle)
    picture._inline.docPr.set('descr', label)

def table(rows):
    count = len(rows[0])
    lengths = [sum(min(100, len(row[column])) for row in rows) / len(rows) for column in range(count)]
    weights = [max(10, size) ** .65 for size in lengths]
    widths = [17 * size / sum(weights) for size in weights]
    if 'Probabilidad' in rows[0]:
        widths = [5.2, 2.5, 2.1, 7.2]
    if rows[0][0] == 'Caso':
        widths = [1.5, 6, 9.5]
    elif rows[0][0] == 'Riesgo':
        widths = [5.2, 3.5, 8.3]
    grid = document.add_table(rows=1, cols=count)
    grid.autofit = False
    for column, width in zip(grid.columns, widths):
        column.width = Cm(width)
    for index, values in enumerate(rows):
        cells = grid.rows[0].cells if index == 0 else grid.add_row().cells
        for position, (cell, value) in enumerate(zip(cells, values)):
            cell.width = Cm(widths[position])
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            properties = cell._tc.get_or_add_tcPr()
            margin = OxmlElement('w:tcMar')
            for name in ['top', 'left', 'bottom', 'right']:
                side = OxmlElement(f'w:{name}')
                side.set(qn('w:w'), '80' if name in ['top', 'bottom'] else '100')
                side.set(qn('w:type'), 'dxa')
                margin.append(side)
            properties.append(margin)
            shade = OxmlElement('w:shd')
            shade.set(qn('w:fill'), 'E4EEEB' if index == 0 else 'FFFFFF')
            properties.append(shade)
            paragraph = cell.paragraphs[0]
            paragraph.paragraph_format.space_after = Pt(1)
            paragraph.paragraph_format.line_spacing = 1.05
            inline(paragraph, value)
            for run in paragraph.runs:
                run.font.size = Pt(10)
                if index == 0:
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(0, 0, 0)
        # Keep rows intact; headings repeat when a table spans pages.
        row_property = grid.rows[index]._tr.get_or_add_trPr()
        row_property.append(OxmlElement('w:cantSplit'))
        if index == 0:
            row_property.append(OxmlElement('w:tblHeader'))
    borders = OxmlElement('w:tblBorders')
    for name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        border = OxmlElement(f'w:{name}')
        for key, value in [('val', 'single'), ('sz', '4'), ('color', 'D9D9D9')]:
            border.set(qn(f'w:{key}'), value)
        borders.append(border)
    grid._tbl.tblPr.append(borders)
    document.add_paragraph().paragraph_format.space_after = Pt(2)

def markdown(source, heading_shift=0, skip_title=True):
    lines = source.splitlines()
    index = 0
    code = False
    while index < len(lines):
        line = lines[index].strip()
        if line.startswith('```'):
            code = not code
            index += 1
            continue
        if not line:
            index += 1
            continue
        picture = re.fullmatch(r'!\[([^\]]*)\]\(([^)]+)\)', line)
        if picture:
            screenshot(picture[1], picture[2])
            index += 1
            continue
        if line.startswith('|'):
            rows = []
            while index < len(lines) and lines[index].strip().startswith('|'):
                row = [value.strip() for value in lines[index].strip().strip('|').split('|')]
                if not all(re.fullmatch(r'[:\- ]+', value) for value in row):
                    rows.append(row)
                index += 1
            table(rows)
            continue
        heading = re.match(r'^(#{1,6}) (.+)$', line)
        if heading:
            level = len(heading[1])
            if not (skip_title and level == 1):
                document.add_heading(heading[2], min(3, max(1, level - 1 + heading_shift)))
        else:
            bullet = line.startswith('- ')
            paragraph = document.add_paragraph(style='List Bullet' if bullet else None)
            if bullet:
                line = line[2:]
            if code:
                paragraph.add_run(line).font.name = 'Consolas'
            else:
                inline(paragraph, line)
        index += 1

document.add_paragraph('Universidad del Valle Univalle')
document.add_paragraph('Software Quality Assurance')
document.add_paragraph('\n')
document.add_paragraph('Plan de pruebas de StockFácil', style='Title')
document.add_paragraph('Organización del trabajo y resultados de las pruebas')
document.add_paragraph('\n')
document.add_paragraph('Andre Romero Caballero\nSantiago Camacho Echalar')
document.add_paragraph('Docente Rolando Lara')
document.add_paragraph('27 de octubre de 2026')
document.add_page_break()
source = (docs / 'Test_Plan_SQA.md').read_text(encoding='utf-8')
body = source[source.index('## 1 Introducción'):]
markdown(body)
footer = section.footer.paragraphs[0]
footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
field = OxmlElement('w:fldSimple')
field.set(qn('w:instr'), 'PAGE')
footer._p.append(field)
for run in footer.runs:
    run.font.size = Pt(8)
document.core_properties.title = 'Plan de pruebas de StockFácil'
document.core_properties.subject = 'Pruebas y resultados explicados con capturas reales'
document.core_properties.author = 'Andre Romero Caballero y Santiago Camacho Echalar'
document.core_properties.comments = 'Revisión humana y aceptación pendientes según el informe.'
destination = docs / 'Test_Plan_SQA.docx'
document.save(destination)
print(f'DOCX generado: {destination}; tablas: {len(document.tables)}')
