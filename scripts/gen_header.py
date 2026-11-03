"""Genera la cabecera, el pie de página y los botones de idioma en estilo retro pixel.

Uso: python gen_header.py <carpeta_assets> <fuente.woff2>
Salida: header.svg, footer.svg, footer-en.svg, btn-es-on.svg, btn-es-off.svg, btn-en-on.svg, btn-en-off.svg
"""
import base64
import math
import os
import random
import sys

OUT, FONT = sys.argv[1], sys.argv[2]
FONT_CSS = ('@font-face { font-family: "PS2P"; src: url(data:font/woff2;base64,'
            + base64.b64encode(open(FONT, "rb").read()).decode() + ') format("woff2"); }'
            ' text { font-family: "PS2P", ui-monospace, monospace; }')
BG = "#0D1117"
BANDS = ["#0D1117", "#11162A", "#161B3A", "#1E2150", "#2A2766", "#3E2F86", "#5B3FB8", "#7F5AF0"]
G = 6  # tamaño del píxel


def write(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
        fh.write(svg)


def bands(w, h, reverse=False):
    """Degradado en bandas verticales con tramado de tablero en cada frontera."""
    cols = BANDS[::-1] if reverse else BANDS
    n = len(cols)
    bw = math.ceil(w / n / G) * G
    out = []
    for i, c in enumerate(cols):
        out.append(f'<rect x="{i * bw}" y="0" width="{bw}" height="{h}" fill="{c}"/>')
    for i in range(1, n):
        x0 = i * bw - G * 2
        for gx in range(4):
            for gy in range(0, h, G):
                if (gx + gy // G) % 2 == (0 if gx < 2 else 1):
                    col = cols[i] if gx < 2 else cols[i - 1]
                    out.append(f'<rect x="{x0 + gx * G}" y="{gy}" width="{G}" height="{G}" fill="{col}"/>')
    return "".join(out)


def stepped_wave(w, top, amp, period, phase, fill, h_total, invert=False):
    """Ola escalonada: columnas de G px cuantizadas a G px."""
    out = []
    for x in range(0, w, G):
        y = top + amp * math.sin(2 * math.pi * x / period + phase)
        y = int(round(y / G)) * G
        if invert:
            out.append(f'<rect x="{x}" y="0" width="{G}" height="{y}" fill="{fill}"/>')
        else:
            out.append(f'<rect x="{x}" y="{y}" width="{G}" height="{h_total - y}" fill="{fill}"/>')
    return "".join(out)


def stars(w, h, count, seed, y_max):
    rnd = random.Random(seed)
    out = []
    for k in range(count):
        x = rnd.randrange(0, w // G) * G
        y = rnd.randrange(1, y_max // G) * G
        d = rnd.uniform(0, 2.4)
        if k % 4 == 0:  # estrella en cruz
            out.append(f'<g class="tw" style="animation-delay:{d:.2f}s" fill="#FFE45C"><rect x="{x}" y="{y - 4}" width="4" height="12"/><rect x="{x - 4}" y="{y}" width="12" height="4"/></g>')
        else:
            out.append(f'<rect class="tw" style="animation-delay:{d:.2f}s" x="{x}" y="{y}" width="4" height="4" fill="#E6EDF3"/>')
    return "".join(out)


STYLE = (f'<style>{FONT_CSS}'
         '.tw { animation: tw 2.4s steps(1, end) infinite; } @keyframes tw { 0%, 60% { opacity: 1; } 61%, 100% { opacity: .2; } }'
         '.blink { animation: bl 1.2s steps(1, end) infinite; } @keyframes bl { 0%, 55% { opacity: 1; } 56%, 100% { opacity: 0; } }'
         '@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }</style>'
         '<defs><pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".12"/></pattern></defs>')


def shadow_text(x, y, size, txt, fill, shadow, anchor="middle"):
    s = max(2, size // 10)
    return (f'<text x="{x + s * 2}" y="{y + s * 2}" font-size="{size}" fill="{BG}" text-anchor="{anchor}" opacity=".7">{txt}</text>'
            f'<text x="{x + s}" y="{y + s}" font-size="{size}" fill="{shadow}" text-anchor="{anchor}">{txt}</text>'
            f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}">{txt}</text>')


# ---------- cabecera ----------
W, H = 854, 230
header = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" shape-rendering="crispEdges" role="img" aria-label="Jeremy Sánchez — Software Engineer · Backend · Data · Cloud">',
          '<title>Jeremy Sánchez</title>', STYLE,
          bands(W, H), stars(W, H, 34, 3, 150),
          shadow_text(W // 2, 104, 42, "Jeremy Sánchez", "#F4F1FF", "#7F5AF0"),
          f'<text x="{W // 2}" y="142" font-size="12" fill="#B9F3FF" text-anchor="middle">SOFTWARE ENGINEER · BACKEND · DATA · CLOUD</text>',
          f'<g class="blink" fill="#FFE45C"><rect x="{W // 2 - 92}" y="161" width="3" height="9"/><rect x="{W // 2 - 89}" y="163" width="3" height="5"/><rect x="{W // 2 - 86}" y="165" width="2" height="1"/><text x="{W // 2 + 8}" y="170" font-size="10" text-anchor="middle">PLAYER 1 READY</text></g>',
          stepped_wave(W, 196, 12, 427, 0.6, BG, H),
          f'<rect width="{W}" height="{H}" fill="url(#scan)"/>',
          '</svg>']
write("header.svg", "".join(header))

# ---------- pie de página ----------
FH = 150
for lang, (msg, cont) in {"es": ("GRACIAS POR JUGAR", "CONTINUE?"), "en": ("THANKS FOR PLAYING", "CONTINUE?")}.items():
    count = "".join(
        f'<text class="cd" style="animation-delay:{(9 - n) * 1.0:.1f}s" x="{W // 2 + 96}" y="122" font-size="14" fill="#FFE45C">{n}</text>'
        for n in range(9, -1, -1))
    footer = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{FH}" viewBox="0 0 {W} {FH}" shape-rendering="crispEdges" role="img" aria-label="{msg}">',
              STYLE.replace('</style>', '.cd { opacity: 0; animation: cd 10s steps(1, end) infinite; } @keyframes cd { 0%, 9.9% { opacity: 1; } 10%, 100% { opacity: 0; } }</style>'),
              bands(W, FH, reverse=True), stars(W, FH, 18, 11, FH),
              stepped_wave(W, 34, 12, 427, 2.4, BG, FH, invert=True),
              shadow_text(W // 2, 92, 20, msg, "#F4F1FF", "#7F5AF0"),
              f'<text x="{W // 2 - 20}" y="122" font-size="14" fill="#B9F3FF" text-anchor="middle">{cont}</text>',
              count,
              f'<rect width="{W}" height="{FH}" fill="url(#scan)"/>', '</svg>']
    write("footer.svg" if lang == "es" else "footer-en.svg", "".join(footer))


# ---------- botones de idioma ----------
def flag_co(x, y):
    return (f'<rect x="{x}" y="{y}" width="24" height="8" fill="#FCD116"/>'
            f'<rect x="{x}" y="{y + 8}" width="24" height="4" fill="#003893"/>'
            f'<rect x="{x}" y="{y + 12}" width="24" height="4" fill="#CE1126"/>')


def flag_us(x, y):
    out = [f'<rect x="{x}" y="{y}" width="24" height="16" fill="#F4F1FF"/>']
    for k in range(0, 16, 4):
        out.append(f'<rect x="{x}" y="{y + k}" width="24" height="2" fill="#B22234"/>')
    out.append(f'<rect x="{x}" y="{y}" width="10" height="8" fill="#3C3B6E"/>')
    return "".join(out)


for lang, label, flag in (("es", "ESPAÑOL", flag_co), ("en", "ENGLISH", flag_us)):
    for state in ("on", "off"):
        on = state == "on"
        bw, bh = 168, 40
        face = "#7F5AF0" if on else "#161B22"
        edge = "#B9A6FF" if on else "#30363D"
        txt = "#FFFFFF" if on else "#8B949E"
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{bw}" height="{bh + 4}" viewBox="0 0 {bw} {bh + 4}" shape-rendering="crispEdges" role="img" aria-label="{label}">'
               f'<style>{FONT_CSS}</style>'
               f'<rect x="4" y="4" width="{bw - 4}" height="{bh}" fill="#05070C"/>'
               f'<rect x="0" y="0" width="{bw - 4}" height="{bh}" fill="{edge}"/>'
               f'<rect x="4" y="4" width="{bw - 12}" height="{bh - 8}" fill="{face}"/>'
               + flag(16, 12) +
               f'<text x="50" y="26" font-size="11" fill="{txt}">{label}</text>'
               + (f'<rect x="{bw - 22}" y="16" width="6" height="8" fill="#FFE45C"/>' if on else "")
               + '</svg>')
        write(f"btn-{lang}-{state}.svg", svg)
print("ok")
