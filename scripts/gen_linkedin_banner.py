"""Genera la portada de LinkedIn (1584x396) en el mismo estilo retro que la cabecera de GitHub, sin animaciones.

Uso: python gen_linkedin_banner.py <salida.svg> <fuente.woff2> <carpeta_iconos> [es|en]
Convertir a PNG, por ejemplo con Chrome: --headless --window-size=1584,396 --screenshot
"""
import base64
import math
import os
import random
import re
import sys
from html import escape

OUT, FONT, ICONS = sys.argv[1], sys.argv[2], sys.argv[3]
LANG = sys.argv[4] if len(sys.argv) > 4 else "es"
TAG = {"es": "Del problema a la solución", "en": "From problem to solution"}[LANG]

W, H, G = 1584, 396, 8
BG = "#0D1117"
BANDS = ["#0D1117", "#11162A", "#161B3A", "#1E2150", "#2A2766", "#3E2F86", "#5B3FB8", "#7F5AF0"]
FONT_CSS = ('@font-face { font-family: "PS2P"; src: url(data:font/woff2;base64,'
            + base64.b64encode(open(FONT, "rb").read()).decode() + ') format("woff2"); }'
            ' text { font-family: "PS2P", ui-monospace, monospace; }')


def bands():
    n = len(BANDS)
    bw = math.ceil(W / n / G) * G
    out = [f'<rect x="{i * bw}" y="0" width="{bw}" height="{H}" fill="{c}"/>' for i, c in enumerate(BANDS)]
    for i in range(1, n):  # tramado de tablero en cada frontera
        x0 = i * bw - G * 2
        for gx in range(4):
            for gy in range(0, H, G):
                if (gx + gy // G) % 2 == (0 if gx < 2 else 1):
                    out.append(f'<rect x="{x0 + gx * G}" y="{gy}" width="{G}" height="{G}" fill="{BANDS[i] if gx < 2 else BANDS[i - 1]}"/>')
    return "".join(out)


def stars():
    rnd = random.Random(5)
    out = []
    for k in range(60):
        x = rnd.randrange(0, W // G) * G
        y = rnd.randrange(1, 300 // G) * G
        if 560 < x < 1440 and 90 < y < 320:  # deja limpio el bloque de texto
            continue
        if k % 4 == 0:
            out.append(f'<g fill="#FFE45C"><rect x="{x}" y="{y - 5}" width="5" height="15"/><rect x="{x - 5}" y="{y}" width="15" height="5"/></g>')
        else:
            out.append(f'<rect x="{x}" y="{y}" width="5" height="5" fill="#E6EDF3" opacity="{rnd.choice((.5, .8, 1))}"/>')
    return "".join(out)


def wave():
    out = []
    for x in range(0, W, G):
        y = int(round((350 + 14 * math.sin(2 * math.pi * x / 640 + 0.6)) / G)) * G
        out.append(f'<rect x="{x}" y="{y}" width="{G}" height="{H - y}" fill="{BG}"/>')
    return "".join(out)


def shadow_text(x, y, size, txt, fill, shadow):
    s = max(2, size // 10)
    return (f'<text x="{x + s * 2}" y="{y + s * 2}" font-size="{size}" fill="{BG}" text-anchor="middle" opacity=".7">{txt}</text>'
            f'<text x="{x + s}" y="{y + s}" font-size="{size}" fill="{shadow}" text-anchor="middle">{txt}</text>'
            f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="middle">{txt}</text>')


def notes(x0, y0):
    """Notas BUG -> IDEA -> FIX, como en la escena de GitHub."""
    out = []
    for i, (label, col) in enumerate((("BUG", "#FF6B8A"), ("IDEA", "#FFD84A"), ("FIX", "#5BE49B"))):
        x = x0 + i * 112
        out.append(f'<rect x="{x + 5}" y="{y0 + 5}" width="76" height="62" fill="#05070C" opacity=".5"/>'
                   f'<rect x="{x}" y="{y0}" width="76" height="62" fill="{col}"/>'
                   f'<rect x="{x + 34}" y="{y0 - 6}" width="10" height="8" fill="#E43B44"/>'
                   f'<text x="{x + 38}" y="{y0 + 40}" font-size="13" fill="#1F2340" text-anchor="middle">{label}</text>')
        if i < 2:
            ax = x + 82
            out.append(f'<g fill="#B9A6FF"><rect x="{ax}" y="{y0 + 28}" width="14" height="6"/><rect x="{ax + 14}" y="{y0 + 22}" width="6" height="18"/></g>')
    return "".join(out)


def icons(names, x0, y0, step):
    out = []
    for k, n in enumerate(names):
        svg = open(os.path.join(ICONS, f"{n}.svg"), encoding="utf-8").read()
        rects = re.search(r"<g>(.*)</g>", svg).group(1)
        out.append(f'<g transform="translate({x0 + k * step} {y0 - 4})">{rects}</g>')
    return "".join(out)


CX = 1000
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" shape-rendering="crispEdges">',
       f'<style>{FONT_CSS}</style>',
       '<defs><pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".1"/></pattern></defs>',
       bands(), stars(),
       notes(64, 52),
       shadow_text(CX, 142, 56, "Jeremy Sánchez", "#F4F1FF", "#7F5AF0"),
       f'<text x="{CX}" y="190" font-size="18" fill="#B9F3FF" text-anchor="middle">SOFTWARE ENGINEER · BACKEND · DATA · CLOUD</text>',
       f'<g fill="#FFE45C"><rect x="{CX - len(TAG) * 8 - 26}" y="214" width="5" height="16"/><rect x="{CX - len(TAG) * 8 - 21}" y="217" width="5" height="10"/><rect x="{CX - len(TAG) * 8 - 16}" y="220" width="4" height="4"/></g>',
       f'<text x="{CX + 4}" y="230" font-size="16" fill="#FFE45C" text-anchor="middle">{escape(TAG)}</text>',
       icons(["py", "django", "postgres", "docker", "azure", "ts", "java", "git"], CX - 4 * 60 + 6, 262, 60),
       wave(),
       f'<rect width="{W}" height="{H}" fill="url(#scan)"/>', '</svg>']

with open(OUT, "w", encoding="utf-8") as fh:
    fh.write("".join(svg))
print("ok", LANG)
