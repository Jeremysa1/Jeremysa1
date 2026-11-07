"""Genera la portada de LinkedIn (1584x396): sobria y corporativa, en azul marino y azul acero.

Uso: python gen_linkedin_banner.py <salida.svg> <carpeta_fuentes> [es|en]
Convertir a PNG, por ejemplo con Chrome: --headless --window-size=1584,396 --screenshot
La esquina inferior izquierda queda libre: ahí LinkedIn pone la foto de perfil.
"""
import base64
import os
import sys
from html import escape

OUT, FONTS = sys.argv[1], sys.argv[2]
LANG = sys.argv[3] if len(sys.argv) > 3 else "es"
TXT = {
    "es": {"kicker": "INGENIERO DE SOFTWARE  ·  BACKEND  ·  DATOS  ·  CLOUD",
           "title": "Del problema a la solución.",
           "sub": "Diseño sistemas backend, datos e infraestructura que escalan."},
    "en": {"kicker": "SOFTWARE ENGINEER  ·  BACKEND  ·  DATA  ·  CLOUD",
           "title": "From problem to solution.",
           "sub": "I design and build backend systems, data and infrastructure that scale."},
}[LANG]
TECH = ["Python", "Django", "PostgreSQL", "Docker", "Azure"]

W, H = 1584, 396
ACCENT, SKY, INK, MUTED = "#2F7BEB", "#7CC4F5", "#F3F6FA", "#A3B3C8"


def font_face(weight):
    data = base64.b64encode(open(os.path.join(FONTS, f"inter-{weight}.woff2"), "rb").read()).decode()
    return f'@font-face {{ font-family: "Inter"; font-weight: {weight}; src: url(data:font/woff2;base64,{data}) format("woff2"); }}'


def diagram(x0, y0):
    """Diagrama de arquitectura abstracto: cliente -> servicios -> datos / nube, en líneas finas."""
    node = 'rx="8" fill="#0E1F38" stroke="{c}" stroke-width="1.5"'
    out = []
    # conexiones
    lines = [(x0 + 70, y0 + 150, x0 + 130, y0 + 150), (x0 + 210, y0 + 150, x0 + 250, y0 + 150),
             (x0 + 250, y0 + 70, x0 + 250, y0 + 230), (x0 + 250, y0 + 70, x0 + 290, y0 + 70),
             (x0 + 250, y0 + 150, x0 + 290, y0 + 150), (x0 + 250, y0 + 230, x0 + 290, y0 + 230)]
    for a, b, c, d in lines:
        out.append(f'<line x1="{a}" y1="{b}" x2="{c}" y2="{d}" stroke="#2A4468" stroke-width="1.5"/>')
    # cliente
    out.append(f'<rect x="{x0}" y="{y0 + 120}" width="70" height="60" {node.format(c="#2A4468")}/>'
               f'<rect x="{x0 + 14}" y="{y0 + 134}" width="42" height="26" rx="3" fill="none" stroke="{MUTED}" stroke-opacity=".6"/>'
               f'<rect x="{x0 + 28}" y="{y0 + 164}" width="14" height="4" rx="1" fill="{MUTED}" fill-opacity=".6"/>')
    # servicio central
    out.append(f'<rect x="{x0 + 130}" y="{y0 + 115}" width="80" height="70" {node.format(c=ACCENT)}/>'
               f'<path d="M{x0 + 157} {y0 + 140} l-9 10 l9 10 M{x0 + 183} {y0 + 140} l9 10 l-9 10 M{x0 + 175} {y0 + 136} l-10 28" fill="none" stroke="{ACCENT}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
    # tres destinos: nube, servicio, base de datos
    out.append(f'<rect x="{x0 + 290}" y="{y0 + 40}" width="70" height="60" {node.format(c=SKY)}/>'
               f'<path d="M{x0 + 309} {y0 + 80} a9 9 0 0 1 2 -17 a12 12 0 0 1 23 -3 a9 9 0 0 1 7 20 z" fill="none" stroke="{SKY}" stroke-width="1.8" stroke-linejoin="round"/>')
    out.append(f'<rect x="{x0 + 290}" y="{y0 + 120}" width="70" height="60" {node.format(c="#2A4468")}/>'
               + "".join(f'<rect x="{x0 + 306}" y="{y0 + 133 + k * 12}" width="38" height="8" rx="2" fill="none" stroke="{MUTED}" stroke-opacity=".6"/>' for k in range(3)))
    out.append(f'<rect x="{x0 + 290}" y="{y0 + 200}" width="70" height="60" {node.format(c="#2A4468")}/>'
               f'<ellipse cx="{x0 + 325}" cy="{y0 + 216}" rx="16" ry="5" fill="none" stroke="{MUTED}" stroke-opacity=".7"/>'
               f'<path d="M{x0 + 309} {y0 + 216} v22 a16 5 0 0 0 32 0 v-22 M{x0 + 309} {y0 + 227} a16 5 0 0 0 32 0" fill="none" stroke="{MUTED}" stroke-opacity=".7"/>')
    # puntos de conexión
    for cx, cy in ((x0 + 250, y0 + 150), (x0 + 250, y0 + 70), (x0 + 250, y0 + 230)):
        out.append(f'<circle cx="{cx}" cy="{cy}" r="3.5" fill="{ACCENT}"/>')
    return "".join(out)


def pills(x, y):
    out = []
    for t in TECH:
        w = 22 + len(t) * 9.4
        out.append(f'<rect x="{x}" y="{y}" width="{w:.0f}" height="32" rx="16" fill="#0F223D" stroke="#24406A"/>'
                   f'<text x="{x + w / 2:.0f}" y="{y + 21}" font-size="15" font-weight="600" fill="#D3E1F2" text-anchor="middle">{escape(t)}</text>')
        x += w + 10
    return "".join(out)


TX = 520  # bloque de texto a la derecha de la zona de la foto
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
       f'<style>{font_face(400)}{font_face(600)}{font_face(700)} text {{ font-family: "Inter", "Segoe UI", sans-serif; }}</style>',
       '<defs>'
       '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#07111F"/><stop offset=".55" stop-color="#0B1B31"/><stop offset="1" stop-color="#10284A"/></linearGradient>'
       f'<radialGradient id="glow" cx=".82" cy=".45" r=".5"><stop offset="0" stop-color="{ACCENT}" stop-opacity=".22"/><stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/></radialGradient>'
       f'<linearGradient id="accent" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{ACCENT}"/><stop offset="1" stop-color="{SKY}"/></linearGradient>'
       '<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.1" fill="#FFFFFF" fill-opacity=".06"/></pattern>'
       '</defs>',
       f'<rect width="{W}" height="{H}" fill="url(#bg)"/>',
       f'<rect width="{W}" height="{H}" fill="url(#dots)"/>',
       f'<rect width="{W}" height="{H}" fill="url(#glow)"/>',
       f'<text x="{TX}" y="128" font-size="16" font-weight="600" letter-spacing="2" fill="{SKY}">{escape(TXT["kicker"])}</text>',
       f'<rect x="{TX}" y="146" width="64" height="4" rx="2" fill="url(#accent)"/>',
       f'<text x="{TX}" y="204" font-size="44" font-weight="700" fill="{INK}">{escape(TXT["title"])}</text>',
       f'<text x="{TX}" y="244" font-size="19" font-weight="400" fill="{MUTED}">{escape(TXT["sub"])}</text>',
       pills(TX, 282),
       diagram(1196, 60),
       f'<rect y="{H - 4}" width="{W}" height="4" fill="url(#accent)" opacity=".85"/>',
       '</svg>']

with open(OUT, "w", encoding="utf-8") as fh:
    fh.write("".join(svg))
print("ok", LANG)
