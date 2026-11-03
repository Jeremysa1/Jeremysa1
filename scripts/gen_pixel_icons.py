"""Convierte la hoja de logos (sheet.png) en iconos pixel art 16x16 animados.

Uso: python gen_pixel_icons.py <sheet.png> <carpeta_salida> [ids,separados,por,coma]

sheet.png: los logos de skillicons.dev renderizados a 256 px en una cuadrícula de 5 columnas
sobre fondo magenta (por ejemplo con Chrome en modo headless).
"""
import os
import sys

from PIL import Image

SHEET, OUT = sys.argv[1], sys.argv[2]
IDS = sys.argv[3].split(",") if len(sys.argv) > 3 else "py django postgres mysql docker aws git github java js react html css dart flutter vercel postman figma linux vscode".split()
TILE, COLS, N, PX = 256, 5, 16, 3   # 16x16 celdas, 3 px cada una -> 48 px
os.makedirs(OUT, exist_ok=True)

sheet = Image.open(SHEET).convert("RGB")


def is_bg(c):
    return c[0] > 220 and c[1] < 40 and c[2] > 220  # magenta del fondo


for idx, name in enumerate(IDS):
    tile = sheet.crop(((idx % COLS) * TILE, (idx // COLS) * TILE, (idx % COLS + 1) * TILE, (idx // COLS + 1) * TILE))
    px = tile.load()
    step = TILE // N
    cells = {}
    for gy in range(N):
        for gx in range(N):
            rs = gs = bs = cnt = 0
            for y in range(gy * step, (gy + 1) * step, 2):
                for x in range(gx * step, (gx + 1) * step, 2):
                    c = px[x, y]
                    if not is_bg(c):
                        rs += c[0]; gs += c[1]; bs += c[2]; cnt += 1
            if cnt >= (step // 2) ** 2 * 0.5:
                cells[(gx, gy)] = (rs // cnt, gs // cnt, bs // cnt)

    # paleta reducida (look de sprite)
    small = Image.new("RGB", (N, N), (0, 0, 0))
    for (x, y), c in cells.items():
        small.putpixel((x, y), c)
    q = small.quantize(colors=7, method=Image.Quantize.MEDIANCUT).convert("RGB")

    rects = []
    for y in range(N):
        x = 0
        while x < N:
            if (x, y) not in cells:
                x += 1
                continue
            col = q.getpixel((x, y))
            x2 = x
            while x2 + 1 < N and (x2 + 1, y) in cells and q.getpixel((x2 + 1, y)) == col:
                x2 += 1
            rects.append(f'<rect x="{x * PX}" y="{y * PX + 4}" width="{(x2 - x + 1) * PX}" height="{PX}" fill="#{col[0]:02X}{col[1]:02X}{col[2]:02X}"/>')
            x = x2 + 1

    delay = idx % 10 * 0.12  # salto en cadena por fila
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="48" height="56" viewBox="0 0 48 56" shape-rendering="crispEdges" role="img" aria-label="{name}">'
           f'<style>g{{animation:hop 3.2s steps(1,end) {delay:.2f}s infinite}}'
           f'@keyframes hop{{0%{{transform:translateY(0)}}4%{{transform:translateY(-3px)}}8%{{transform:translateY(-1px)}}12%,100%{{transform:translateY(0)}}}}'
           f'@media (prefers-reduced-motion:reduce){{g{{animation:none}}}}</style>'
           f'<rect x="6" y="53" width="36" height="3" fill="#000" opacity=".25"/>'
           f'<g>{"".join(rects)}</g></svg>')
    with open(os.path.join(OUT, f"{name}.svg"), "w", encoding="utf-8") as fh:
        fh.write(svg)
print("ok", len(IDS))
