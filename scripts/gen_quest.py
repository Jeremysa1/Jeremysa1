"""Genera la sección "Ahora mismo" como un registro de misiones (quest log) retro.

Uso: python gen_quest.py <salida.svg> <fuente.woff2> <carpeta_iconos> [es|en]
"""
import base64
import os
import re
import sys
from html import escape

OUT, FONT, ICONS = sys.argv[1], sys.argv[2], sys.argv[3]
LANG = sys.argv[4] if len(sys.argv) > 4 else "es"
TXT = {
    "es": {
        "aria": "Ahora mismo: rumbo a la certificación de Arquitecto de Soluciones",
        "now": "AHORA MISMO", "main_label": "Misión principal",
        "main": "Certificación: Arquitecto de Soluciones", "status": "EN PROGRESO",
        "side": [("azure", "Azure: servicios y arquitectura", "CLOUD"),
                 ("cloud", "Infraestructura en la nube", "INFRA"),
                 ("iac", "Cómo se construye la infra (IaC)", "IaC"),
                 ("ts", "TypeScript a fondo", "LENGUAJE"),
                 ("java", "Java a fondo", "LENGUAJE")],
        "doing": "EN CURSO",
        "reward_label": "Recompensa", "reward": ["Diseñar soluciones cloud", "de punta a punta"],
    },
    "en": {
        "aria": "Right now: on the way to the Solutions Architect certification",
        "now": "RIGHT NOW", "main_label": "Main quest",
        "main": "Certification: Solutions Architect", "status": "IN PROGRESS",
        "side": [("azure", "Azure: services & architecture", "CLOUD"),
                 ("cloud", "Cloud infrastructure", "INFRA"),
                 ("iac", "How infra is built (IaC)", "IaC"),
                 ("ts", "TypeScript in depth", "LANGUAGE"),
                 ("java", "Java in depth", "LANGUAGE")],
        "doing": "ONGOING",
        "reward_label": "Reward", "reward": ["Designing cloud solutions", "end to end"],
    },
}[LANG]

W, H = 854, 372
PX = 3
FONT_CSS = ('@font-face { font-family: "PS2P"; src: url(data:font/woff2;base64,'
            + base64.b64encode(open(FONT, "rb").read()).decode() + ') format("woff2"); }'
            ' text { font-family: "PS2P", ui-monospace, monospace; }')

TILE = "#242938"


def sprite(x0, y0, rows, cmap, tile=True):
    """Icono 16x16 de 3 px; con tile dibuja el fondo redondeado como los de skillicons."""
    out = []
    if tile:
        for y in range(16):
            for x in range(16):
                corner = (x in (0, 15) and y in (0, 1, 14, 15)) or (y in (0, 15) and x in (0, 1, 14, 15))
                if not corner:
                    out.append((x, y, TILE))
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch != ".":
                out.append((x, y, cmap[ch]))
    return "".join(f'<rect x="{x0 + x * PX}" y="{y0 + y * PX}" width="{PX}" height="{PX}" fill="{c}"/>' for x, y, c in out)


def icon_from_file(name, x0, y0):
    """Reutiliza los iconos pixel del stack (assets/icons/<name>.svg)."""
    svg = open(os.path.join(ICONS, f"{name}.svg"), encoding="utf-8").read()
    rects = re.search(r"<g>(.*)</g>", svg).group(1)
    return f'<g transform="translate({x0} {y0 - 4})">{rects}</g>'


CLOUD = ["", "", "", "", "......cccc......", ".....cWWWWc.....", "...ccWWWWWWcc...", "..cWWWWWWWWWWc..",
         ".cWWWWWWWWWWWWc.", ".cWWWWWWWWWWWWc.", "..cccccccccccc..", "", "....Y..Y..Y.....", "....Y..Y..Y.....", "...YYYYYYYYY...."]
IAC = ["", "", "...vvvvvvvvvv...", "...vGvvvvvvvv...", "...vvvvvvvvvv...", "", "...vvvvvvvvvv...", "...vGvvvvvvvv...",
       "...vvvvvvvvvv...", "", "", "...Y....Y...Y...", "..Y....Y.....Y..", "...Y..Y.....Y...", ""]
STAR = ["", ".......YY.......", ".......YY.......", "......YYYY......", "YYYYYYYYYYYYYYYY", ".YYYYYYYYYYYYYY.", "..YYYYYYYYYYYY..",
        "...YYYYYYYYYY...", "...YYYYYYYYYY...", "..YYYYYYYYYYYY..", "..YYYYY..YYYYY..", ".YYYY......YYYY.", ".YYY........YYY.", "YY............YY"]
CHEST = ["", "", "...oooooooooo...", "..oBBBBBBBBBBo..", ".oBBBBBBBBBBBBo.", ".oooooooooooooo.", ".oBBBBBYYBBBBBo.", ".oBBBBBYYBBBBBo.",
         ".oBBBBBBBBBBBBo.", ".oBBBBBBBBBBBBo.", ".oooooooooooooo.", "", "", ""]
CMAP = {"c": "#00A3CC", "W": "#E6F6FF", "Y": "#FFE45C", "v": "#7F5AF0", "G": "#3CCB6E", "o": "#3A2410", "B": "#B8742A"}

out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" shape-rendering="crispEdges" role="img" aria-label="{escape(TXT["aria"])}">',
       f'<title>{escape(TXT["now"])}</title>',
       f'<style>{FONT_CSS}'
       '.blink { animation: bl 1.1s steps(1, end) infinite; } @keyframes bl { 0%, 55% { opacity: 1; } 56%, 100% { opacity: 0; } }'
       '.run { animation: run 2.4s steps(24, end) infinite; } @keyframes run { from { transform: translateX(-120px); } to { transform: translateX(600px); } }'
       '.tw { animation: tw 1.8s steps(1, end) infinite; } @keyframes tw { 0%, 50% { opacity: 1; } 51%, 100% { opacity: .45; } }'
       '@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }</style>',
       '<defs><clipPath id="bar"><rect x="236" y="122" width="584" height="12"/></clipPath>'
       '<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".1"/></pattern></defs>']

# ventana con borde doble y esquinas pixeladas
out.append(f'<rect x="6" y="0" width="{W - 12}" height="{H}" fill="#7F5AF0"/><rect x="0" y="6" width="{W}" height="{H - 12}" fill="#7F5AF0"/>'
           f'<rect x="6" y="6" width="{W - 12}" height="{H - 12}" fill="#0F1328"/>'
           f'<rect x="10" y="10" width="{W - 20}" height="{H - 20}" fill="none" stroke="#3E2F86" stroke-width="2"/>')
# barra de título
out.append(f'<rect x="12" y="12" width="{W - 24}" height="36" fill="#1B1F3B"/>'
           f'<text x="28" y="38" font-size="14" fill="#FFE45C">QUEST LOG</text>'
           f'<rect class="blink" x="{W - 40}" y="24" width="10" height="10" fill="#3CCB6E"/>'
           f'<text x="{W - 52}" y="38" font-size="12" fill="#00D4FF" text-anchor="end">{escape(TXT["now"])}</text>')

# misión principal
out.append(sprite(28, 66, STAR, CMAP, tile=False))
out.append(f'<text x="92" y="80" font-size="9" fill="#8B949E">{escape(TXT["main_label"])}</text>'
           f'<text x="92" y="104" font-size="14" fill="#F4F1FF">{escape(TXT["main"])}</text>'
           f'<text x="92" y="133" font-size="9" fill="#FFE45C">{escape(TXT["status"])}</text>')
# barra de progreso indeterminada (en curso, sin porcentaje inventado)
out.append('<rect x="232" y="118" width="592" height="20" fill="#7F5AF0"/><rect x="236" y="122" width="584" height="12" fill="#161B3A"/>')
for k in range(0, 584, 12):
    out.append(f'<rect x="{236 + k}" y="122" width="6" height="12" fill="#1E2150"/>')
out.append('<g clip-path="url(#bar)"><g class="run">' + "".join(
    f'<rect x="{236 + k * 12}" y="122" width="10" height="12" fill="{c}"/>' for k, c in enumerate(["#3E2F86", "#5B3FB8", "#7F5AF0", "#00D4FF", "#B9F3FF"])) + '</g></g>')

out.append(f'<rect x="28" y="156" width="{W - 56}" height="2" fill="#3E2F86"/>')

# misiones secundarias en 2 columnas y la recompensa en la última celda
cells = [(28, 172), (440, 172), (28, 232), (440, 232), (28, 292), (440, 292)]
for k, (icon, label, tag) in enumerate(TXT["side"]):
    x, y = cells[k]
    if icon == "cloud":
        out.append(sprite(x, y, CLOUD, CMAP))
    elif icon == "iac":
        out.append(sprite(x, y, IAC, CMAP))
    else:
        out.append(icon_from_file(icon, x, y))
    out.append(f'<text x="{x + 62}" y="{y + 20}" font-size="10" fill="#E6EDF3">{escape(label)}</text>'
               f'<text x="{x + 62}" y="{y + 40}" font-size="8" fill="#7F8CC4">{escape(tag)} · </text>'
               f'<text class="tw" style="animation-delay:{k * 0.3:.1f}s" x="{x + 62 + (len(tag) + 3) * 8}" y="{y + 40}" font-size="8" fill="#3CCB6E">{escape(TXT["doing"])}</text>')
x, y = cells[5]
out.append(sprite(x, y, CHEST, CMAP, tile=False))
out.append(f'<text x="{x + 62}" y="{y + 12}" font-size="8" fill="#FFE45C">{escape(TXT["reward_label"])}</text>'
           f'<text x="{x + 62}" y="{y + 30}" font-size="9" fill="#E6EDF3">{escape(TXT["reward"][0])}</text>'
           f'<text x="{x + 62}" y="{y + 46}" font-size="9" fill="#E6EDF3">{escape(TXT["reward"][1])}</text>')

out.append(f'<rect x="6" y="6" width="{W - 12}" height="{H - 12}" fill="url(#scan)"/></svg>')

with open(OUT, "w", encoding="utf-8") as fh:
    fh.write("".join(out))
print("ok", LANG)
