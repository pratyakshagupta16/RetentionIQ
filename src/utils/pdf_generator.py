import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

def generate_pdf_report(metrics, segments_summary, top_churn_drivers, recommendations):




    buffer = io.BytesIO()


    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40, leftMargin=40,
        topMargin=40, bottomMargin=40
    )

    styles = getSampleStyleSheet()


    PRIMARY_COLOR = colors.HexColor("#0B1220")
    SECONDARY_COLOR = colors.HexColor("#8B5CF6")
    ACCENT_COLOR = colors.HexColor("#0D9488")
    TEXT_COLOR = colors.HexColor("#1F2937")
    LIGHT_BG = colors.HexColor("#F3F4F6")


    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28,
        textColor=colors.white,
        spaceAfter=15
    )

    subtitle_style = ParagraphStyle(
        "ReportSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#9CA3AF"),
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        "Heading1_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=PRIMARY_COLOR,
        spaceBefore=15,
        spaceAfter=10,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        "Heading2_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=SECONDARY_COLOR,
        spaceBefore=12,
        spaceAfter=8,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        "Body_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=14,
        textColor=TEXT_COLOR,
        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        "Bullet_Custom",
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=5
    )

    story = []


    header_data = [
        [Paragraph("CUSTOMER ANALYTICS & SEGMENTATION", title_style)],
        [Paragraph(f"Executive Report  |  Generated on: {metrics.get('run_date', 'Today')}", subtitle_style)]
    ]
    header_table = Table(header_data, colWidths=[7.2 * inch])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), PRIMARY_COLOR),
        ('PADDING', (0,0), (-1,-1), 18),
        ('BOTTOMPADDING', (0,0), (-1,0), 4),
        ('TOPPADDING', (0,0), (-1,0), 16),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
    ]))

    story.append(header_table)
    story.append(Spacer(1, 0.25 * inch))


    story.append(Paragraph("Executive Summary", h1_style))
    story.append(Paragraph(
        "This intelligence report provides synthesized insights regarding customer engagement, purchasing behavior, "
        "RFM-based segmentation, churn risk predictions, and Customer Lifetime Value (CLV) estimations. "
        "Marketing strategy and financial projections should adjust in alignment with these findings.",
        body_style
    ))
    story.append(Spacer(1, 0.15 * inch))


    story.append(Paragraph("Key Metrics Overview", h2_style))

    kpi_data = [
        [
            Paragraph("<b>Metric</b>", body_style),
            Paragraph("<b>Value</b>", body_style),
            Paragraph("<b>Description</b>", body_style)
        ],
        [
            Paragraph("Total Revenue", body_style),
            Paragraph(f"${metrics.get('total_revenue', '0.00'):,}", body_style),
            Paragraph("Cumulative purchase amount across history", body_style)
        ],
        [
            Paragraph("Total Customers", body_style),
            Paragraph(f"{metrics.get('total_customers', 0):,}", body_style),
            Paragraph("Count of unique buying customer profiles", body_style)
        ],
        [
            Paragraph("Average Order Value", body_style),
            Paragraph(f"${metrics.get('aov', '0.00'):,}", body_style),
            Paragraph("Average revenue generated per transaction", body_style)
        ],
        [
            Paragraph("Customer Retention Rate", body_style),
            Paragraph(f"{metrics.get('retention_rate', '0.0')}%", body_style),
            Paragraph("Ratio of active (non-churned) customer bases", body_style)
        ],
        [
            Paragraph("Projected Future Revenue", body_style),
            Paragraph(f"${metrics.get('projected_clv', '0.00'):,}", body_style),
            Paragraph("Aggregated predicted customer spending capacity", body_style)
        ]
    ]

    kpi_table = Table(kpi_data, colWidths=[2.0 * inch, 1.8 * inch, 3.4 * inch])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), LIGHT_BG),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 0.25 * inch))


    story.append(Paragraph("Segment Revenue Contribution", h1_style))
    story.append(Paragraph(
        "Below is the classification of customer cohorts grouped by the K-Means RFM clustering algorithm. "
        "High-value cohorts should be preserved via loyalty programs, while inactive groups require reactivation campaigns.",
        body_style
    ))
    story.append(Spacer(1, 0.1 * inch))

    segment_table_data = [
        [
            Paragraph("<b>Segment Label</b>", body_style),
            Paragraph("<b>Customer Count</b>", body_style),
            Paragraph("<b>Share %</b>", body_style),
            Paragraph("<b>Monetary Contribution</b>", body_style)
        ]
    ]

    for row in segments_summary:
        segment_table_data.append([
            Paragraph(f"{row.get('Segment', 'Unknown')}", body_style),
            Paragraph(f"{row.get('Customers', 0):,}", body_style),
            Paragraph(f"{row.get('Share_Pct', 0.0):.1f}%", body_style),
            Paragraph(f"${row.get('Revenue', 0.0):,.2f}", body_style)
        ])

    seg_table = Table(segment_table_data, colWidths=[2.2 * inch, 1.5 * inch, 1.3 * inch, 2.2 * inch])
    seg_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), LIGHT_BG),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
    ]))
    story.append(seg_table)
    story.append(Spacer(1, 0.25 * inch))

    story.append(PageBreak())


    story.append(Paragraph("Retention & Churn Analytics", h1_style))
    story.append(Paragraph(
        "Predictive classification modeling identifies customer accounts displaying behaviors highly indicative of churn. "
        "The top drivers calculated globally across the feature library point to key friction markers.",
        body_style
    ))
    story.append(Spacer(1, 0.1 * inch))

    story.append(Paragraph("Top Predicted Churn Drivers", h2_style))
    for driver in top_churn_drivers:
        story.append(Paragraph(f"• <b>{driver.get('Feature', 'N/A')}</b> (Relative influence: {driver.get('Importance', 0.0)*100:.1f}%)", bullet_style))
    story.append(Spacer(1, 0.2 * inch))


    story.append(Paragraph("Strategic Recommendations", h1_style))
    story.append(Paragraph(
        "Based on multi-dimensional customer behavioral data, we suggest the following actionable steps:",
        body_style
    ))
    story.append(Spacer(1, 0.1 * inch))

    for idx, rec in enumerate(recommendations):
        story.append(Paragraph(f"{idx+1}. {rec}", bullet_style))

    doc.build(story)

    buffer.seek(0)
    pdf_data = buffer.getvalue()
    buffer.close()

    return pdf_data
