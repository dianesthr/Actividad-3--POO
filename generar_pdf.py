"""
Genera Actividad3_POO.pdf (portada, código, interfaz de usuario, diagramas de clases,
de objetos y casos de uso). Edite NOMBRE, CODIGO y las URL de GitHub y ejecute:
    python3 generar_pdf.py
Requiere: pip install reportlab pillow
"""
import os
from PIL import Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (Image as RLImage, PageBreak, Paragraph, Preformatted,
                                SimpleDocTemplate, Spacer, KeepTogether)

# ------------------------- DATOS A COMPLETAR -------------------------
NOMBRE = "[Escriba aquí su nombre completo]"
URL_REPO = "[Enlace del repositorio de GitHub]"
URL_82 = "[Enlace GitHub: actividad8_2.py]"
URL_83 = "[Enlace GitHub: actividad8_3.py]"
# ---------------------------------------------------------------------

AQUI = os.path.dirname(os.path.abspath(__file__))
def ruta(*p): return os.path.join(AQUI, *p)

ss = getSampleStyleSheet()
TITULO = ParagraphStyle("t", parent=ss["Title"], fontSize=20, leading=26)
H1 = ParagraphStyle("h1", parent=ss["Heading1"], fontSize=15, textColor=colors.HexColor("#1F4E79"))
H2 = ParagraphStyle("h2", parent=ss["Heading2"], fontSize=12, textColor=colors.HexColor("#1F4E79"))
CUERPO = ParagraphStyle("c", parent=ss["BodyText"], fontSize=10, leading=14)
CENTRO = ParagraphStyle("ce", parent=CUERPO, alignment=TA_CENTER)
CODIGO = ParagraphStyle("cod", fontName="Courier", fontSize=6.6, leading=7.8)
PIE = ParagraphStyle("pie", parent=CENTRO, fontSize=8, textColor=colors.grey)

def imagen(path, ancho_max=16.5 * cm, alto_max=None):
    w, h = Image.open(path).size
    esc = ancho_max / w
    if alto_max and h * esc > alto_max:
        esc = alto_max / h
    return RLImage(path, width=w * esc, height=h * esc)

def codigo(archivo):
    texto = open(ruta(archivo), encoding="utf-8").read().replace("\t", "    ")
    return Preformatted(texto, CODIGO)

def pegar(imgs, destino, separacion=12):
    """Une varias capturas en una sola imagen (en fila)."""
    ims = [Image.open(ruta("capturas", f)) for f in imgs]
    W = sum(i.width for i in ims) + separacion * (len(ims) - 1)
    H = max(i.height for i in ims)
    lienzo = Image.new("RGB", (W, H), "white")
    x = 0
    for i in ims:
        lienzo.paste(i, (x, 0)); x += i.width + separacion
    lienzo.save(ruta("capturas", destino))
    return ruta("capturas", destino)

def pie(canvas, doc):
    canvas.saveState(); canvas.setFont("Helvetica", 8); canvas.setFillColor(colors.grey)
    canvas.drawCentredString(A4[0] / 2, 1.2 * cm, f"POO 2026-2 - Actividad 3 - Página {doc.page}")
    canvas.restoreState()

H = []
# ------------------------------- Portada -------------------------------
H += [Spacer(1, 4 * cm), Paragraph("UNIVERSIDAD NACIONAL DE COLOMBIA", CENTRO), Spacer(1, 1 * cm),
      Paragraph("Programación Orientada a Objetos 2026-2", TITULO),
      Paragraph("Docente: Walter Hugo Arboleda Mazo", CENTRO), Spacer(1, 1.5 * cm),
      Paragraph("<b>Actividad 3</b> (10% individual)", CENTRO),
      Paragraph("Ejercicios 8.2 (p. 483) y 8.3 (p. 495) del libro <i>Ejercicios de Programación Orientada "
                "a Objetos con Java y UML</i> - Leonardo Bermón Angarita", CENTRO), Spacer(1, 1.5 * cm),
      Paragraph(f"<b>Estudiante:</b> {NOMBRE}", CENTRO), Spacer(1, 0.4 * cm),
      Paragraph(f"<b>Repositorio:</b> {URL_REPO}", CENTRO), Spacer(1, 0.4 * cm),
      Paragraph("Fecha de entrega: jueves 22 de octubre de 2026", CENTRO), PageBreak()]

# ------------------------------- 8.2 -------------------------------
H += [Paragraph("Punto 1 - Ejercicio 8.2 (p. 483): Notas", H1),
      Paragraph("<b>Enunciado.</b> Programa con interfaz gráfica que solicita cinco notas de un estudiante y "
                "muestra el promedio, la desviación estándar, la mayor nota y la menor nota. "
                "<b>Parte propuesta:</b> (1) mensaje de alerta cuando se ingresan datos no numéricos; "
                "(2) es obligatorio ingresar las cinco notas, con alerta si alguna falta.", CUERPO),
      Paragraph(f"<b>Enlace del repositorio:</b> {URL_82}", CUERPO), Spacer(1, 6),
      Paragraph("Código (Python, tkinter)", H2), codigo("actividad8_2.py"), PageBreak(),
      Paragraph("Interfaz de usuario - Ejercicio 8.2", H2),
      Paragraph("Ventana inicial y ventana con los resultados calculados (notas 3.5, 4.2, 5, 2.8 y 1.5).", CUERPO),
      imagen(pegar(["8_2_a_inicial.png", "8_2_b_resultados.png"], "_8_2_ui.png"), 12 * cm),
      Paragraph("Diagrama de clases - Ejercicio 8.2", H2), imagen(ruta("diagramas", "8_2_clases.png"), 9 * cm),
      PageBreak(),
      Paragraph("Diagrama de objetos - Ejercicio 8.2", H2), imagen(ruta("diagramas", "8_2_objetos.png"), 16 * cm),
      Paragraph("Casos de uso - Ejercicio 8.2", H2), imagen(ruta("diagramas", "8_2_casos_uso.png"), 14 * cm),
      PageBreak()]

# ------------------------------- 8.3 -------------------------------
fila1 = pegar(["8_3_a_principal.png"], "_8_3_ui_principal.png")
fila2 = pegar(["8_3_b_cilindro.png", "8_3_c_esfera.png", "8_3_d_piramide.png"], "_8_3_ui_1.png")
fila3 = pegar(["8_3_e_cubo.png", "8_3_f_prisma.png"], "_8_3_ui_2.png")
H += [Paragraph("Punto 2 - Ejercicio 8.3 (p. 495): Figuras geométricas", H1),
      Paragraph("<b>Enunciado.</b> Programa con interfaz gráfica que calcula el volumen y la superficie del "
                "cilindro (radio y altura), la esfera (radio) y la pirámide (base, altura y apotema), todo en "
                "centímetros, mediante una jerarquía de clases. <b>Parte propuesta:</b> (1) agregar el cubo y el "
                "prisma; (2) mostrar la imagen correspondiente de cada figura.", CUERPO),
      Paragraph(f"<b>Enlace del repositorio:</b> {URL_83}", CUERPO), Spacer(1, 6),
      Paragraph("Código (Python, tkinter)", H2), codigo("actividad8_3.py"), PageBreak(),
      Paragraph("Interfaz de usuario - Ejercicio 8.3", H2),
      Paragraph("Ventana principal y ventanas de cada figura con un cálculo de ejemplo.", CUERPO),
      imagen(fila1, 9 * cm), Spacer(1, 6), imagen(fila2, 17 * cm), Spacer(1, 6), imagen(fila3, 12 * cm),
      PageBreak(),
      Paragraph("Diagrama de clases - Ejercicio 8.3", H2), imagen(ruta("diagramas", "8_3_clases.png"), 17 * cm),
      Paragraph("Diagrama de objetos - Ejercicio 8.3", H2), imagen(ruta("diagramas", "8_3_objetos.png"), 17 * cm),
      PageBreak(),
      Paragraph("Casos de uso - Ejercicio 8.3", H2), imagen(ruta("diagramas", "8_3_casos_uso.png"), 15 * cm)]

doc = SimpleDocTemplate(ruta("Actividad3_POO.pdf"), pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm,
                        topMargin=2 * cm, bottomMargin=2 * cm, title="Actividad 3 - POO 2026-2")
doc.build(H, onFirstPage=lambda c, d: None, onLaterPages=pie)
print("Generado:", ruta("Actividad3_POO.pdf"))
