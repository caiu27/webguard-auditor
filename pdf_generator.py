import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf_report(results: dict) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=10
    )
    
    sub_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#64748B'),
        spaceAfter=15
    )

    story = []

    story.append(Paragraph("Reporte Ejecutivo de Auditoría Web", title_style))
    story.append(Paragraph(f"Objetivo analizado: <b>{results['url']}</b> | Estado HTTP: {results['status_code']}", sub_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#E2E8F0'), spaceAfter=15))

    score_color = "#16A34A" if results['score'] >= 80 else ("#D97706" if results['score'] >= 50 else "#DC2626")
    score_text = f"Calificación de Seguridad: <font color='{score_color}'><b>{results['score']} / 100</b></font>"
    story.append(Paragraph(score_text, styles['Heading2']))
    story.append(Spacer(1, 10))

    if results['missing']:
        story.append(Paragraph("Cabeceras Faltantes (Acciones Recomendadas)", styles['Heading3']))
        table_data = [["Cabecera / Riesgo", "Recomendación"]]
        
        for header, data in results['missing'].items():
            p_header = Paragraph(f"<b>{header}</b><br/><font color='#DC2626'>Riesgo: {data['risk']}</font>", styles['Normal'])
            p_recom = Paragraph(data['recommendation'], styles['Normal'])
            table_data.append([p_header, p_recom])

        t = Table(table_data, colWidths=[180, 350])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F1F5F9')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(t)
        story.append(Spacer(1, 15))

    if results['found']:
        story.append(Paragraph("Cabeceras Correctamente Configuradas", styles['Heading3']))
        found_data = [["Cabecera", "Valor Detectado"]]
        
        for header, data in results['found'].items():
            p_h = Paragraph(f"<b>{header}</b>", styles['Normal'])
            p_v = Paragraph(f"<font color='#16A34A'>{data['value'][:60]}...</font>" if len(data['value']) > 60 else f"<font color='#16A34A'>{data['value']}</font>", styles['Normal'])
            found_data.append([p_h, p_v])

        t_found = Table(found_data, colWidths=[180, 350])
        t_found.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F1F5F9')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(t_found)

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()