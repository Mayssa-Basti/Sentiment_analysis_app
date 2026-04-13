from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def create_pdf_report(path, analysis_result: dict):
    doc = SimpleDocTemplate(path)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("EmotionCare AI Report", styles["Title"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph(f"Text: {analysis_result['text']}", styles["BodyText"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(f"Sentiment: {analysis_result['sentiment']}", styles["BodyText"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(f"Emotion: {analysis_result['emotion']}", styles["BodyText"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(f"Wellbeing Score: {analysis_result['wellbeing']}", styles["BodyText"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(f"Probabilities: {analysis_result['probs']}", styles["BodyText"]))

    doc.build(story)