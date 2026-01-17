import os
import random
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image, ImageDraw

def create_dummy_chart(filename, chart_type="bar"):
    """Creates a simple chart image (bar or pie)."""
    img = Image.new('RGB', (400, 300), color='white')
    d = ImageDraw.Draw(img)
    
    if chart_type == "bar":
        # Draw random bars
        h1 = random.randint(50, 200)
        h2 = random.randint(50, 200)
        d.rectangle([50, 300-h1, 100, 300], fill="blue")
        d.rectangle([150, 300-h2, 200, 300], fill="red")
        d.text((50, 310), "Product A", fill="black")
        d.text((150, 310), "Product B", fill="black")
    else:
        # Draw a circle for pie chart (Using pieslice instead of pie)
        # Background circle outline
        d.ellipse([100, 50, 300, 250], outline="black", width=2)
        
        # Draw slices using 'pieslice' which is safer across versions
        d.pieslice([100, 50, 300, 250], 0, 90, fill="yellow")
        d.pieslice([100, 50, 300, 250], 90, 360, fill="green")
    
    img.save(filename)
    print(f"Created image: {filename}")

def create_dummy_pdf(filename, topic, image_path=None):
    """Creates a PDF with random text and optional image."""
    c = canvas.Canvas(filename, pagesize=letter)
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, f"Report on {topic}")
    
    c.setFont("Helvetica", 12)
    c.drawString(100, 730, f"This document covers the latest trends in {topic}.")
    c.drawString(100, 710, "Data shows significant growth in this sector.")
    
    if image_path:
        c.drawImage(image_path, 100, 400, width=300, height=225)
        c.drawString(100, 380, f"Figure 1: Analysis of {topic}")
    
    c.save()
    print(f"Created PDF: {filename}")

if __name__ == "__main__":
    os.makedirs("sample_documents", exist_ok=True)
    
    topics = ["AI Trends", "Q3 Finance", "Supply Chain", "HR Policies", "Marketing"]
    
    # 1. Create 5 PDFs with embedded images
    for i, topic in enumerate(topics):
        img_name = f"sample_documents/chart_{i}.png"
        create_dummy_chart(img_name, chart_type="bar" if i % 2 == 0 else "pie")
        
        pdf_name = f"sample_documents/doc_{i}_{topic.replace(' ', '_')}.pdf"
        create_dummy_pdf(pdf_name, topic, img_name)

    # 2. Create 3 standalone images (Screenshots/Diagrams)
    for i in range(3):
        img_name = f"sample_documents/standalone_diagram_{i}.jpg"
        create_dummy_chart(img_name, chart_type="pie")

    # 3. Create 2 Text-only PDFs
    create_dummy_pdf("sample_documents/doc_text_only_1.pdf", "Legal Disclaimers")
    create_dummy_pdf("sample_documents/doc_text_only_2.pdf", "Meeting Minutes")

    print("\n✅ GENERATED 10+ DIVERSE DOCUMENTS!")