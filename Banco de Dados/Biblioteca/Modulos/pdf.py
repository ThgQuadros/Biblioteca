from reportlab.pdfgen import canvas

pdf = canvas.Canvas("relatorio.pdf")
pdf.drawString(100, 750, "Relatório Biblioteca")
pdf.save()