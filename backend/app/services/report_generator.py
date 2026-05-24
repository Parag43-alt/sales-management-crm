import csv
import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def export_to_csv(headers: list, rows: list) -> io.StringIO:
    """
    Takes headers and a list of lists (rows) and returns a StringIO CSV buffer.
    """
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(headers)
    writer.writerows(rows)
    output.seek(0)
    return output

def export_to_pdf(title: str, headers: list, rows: list) -> io.BytesIO:
    """
    Takes a title, headers, and rows and returns a BytesIO PDF buffer.
    Uses ReportLab to generate a clean, enterprise-style table.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    # Title Style
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    elements.append(Paragraph(title, title_style))
    elements.append(Spacer(1, 20))
    
    # Table Data Formulation
    data = [headers] + rows
    
    # Create Table
    t = Table(data)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')), # Header background
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),           # Header text
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ecf0f1')),# Row background
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),   # Grid lines
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ]))
    
    elements.append(t)
    doc.build(elements)
    buffer.seek(0)
    
    return buffer
