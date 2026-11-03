"""Genera assets/jeremy-pixel.svg: Jeremy en pixel art 16-bit, escena retro animada.

Uso: python gen_scene.py <salida.svg> <fuente.woff2> [es|en]
"""
import base64
from html import escape
import sys

OUT, FONT = sys.argv[1], sys.argv[2]
LANG = sys.argv[3] if len(sys.argv) > 3 else "es"
TXT = {
    "es": {
        "aria": "Jeremy en pixel art saluda: ¡Hola! Soy Jeremy, ingeniero de software",
        "title": "¡Hola! Soy Jeremy",
        "board": "Ciclo de vida del software",
        "steps": ["Problema", "Análisis", "Diseño", "Código", "Tests", "Deploy", "Solución"],
        "iterate": "Iterar",
        "code": ["resolver", "analizar", "diseñar", "codear", "probar"],
        "msgs": [("¡Hola! Soy Jeremy.", "Bienvenido a mi GitHub"), ("Ingeniero de software", "Backend y datos"),
                 ("Del problema a", "la solución."), ("PRESS START", "> ver mis proyectos")],
    },
    "en": {
        "aria": "Pixel art Jeremy waves: Hi! I'm Jeremy, software engineer",
        "title": "Hi! I'm Jeremy",
        "board": "Software development life cycle",
        "steps": ["Problem", "Analysis", "Design", "Code", "Tests", "Deploy", "Solution"],
        "iterate": "Iterate",
        "code": ["solve", "analyze", "design", "build", "test"],
        "msgs": [("Hi! I'm Jeremy.", "Welcome to my GitHub"), ("Software engineer", "Backend & data"),
                 ("From the problem", "to the solution."), ("PRESS START", "> see my projects")],
    },
}[LANG]

W, H = 854, 440
P = 7            # tamaño de cada píxel
GW, GH = 52, 52  # cuadrícula del personaje
C = 26           # columna central
OX, OY = 64, H - GH * P - 6  # posición del personaje en el lienzo
LOOP = 14.0      # duración del ciclo (s)
SCENES = [(0, 4), (4, 7.5), (7.5, 11), (11, 14)]  # saludo, guiño, idea, press start

PAL = {
    "K": "#1A0F0A",  # contorno
    "H": "#16100C", "h": "#3B2A20", "f": "#4A3022",  # cabello, brillo, degradado
    "S": "#8A5232", "s": "#6B3C22", "L": "#A8693F",  # piel
    "W": "#F4ECE4", "D": "#FFFFFF",
    "M": "#3E1A12", "R": "#7A3A2A",
    "T": "#17171D", "t": "#2E2E3A",  # camiseta negra
    "G": "#E8BE4E", "g": "#B8892A",  # oro
    "V": "#7F5AF0", "Y": "#00D4FF",
    "r": "#C9CED6",  # anillo
}


class Layer:
    def __init__(self):
        self.px = {}

    def put(self, x, y, c):
        if c != ".":
            self.px[(x, y)] = c

    def sym(self, y, half):
        """Fila simétrica: half va de afuera hacia el centro."""
        n = len(half)
        for i, c in enumerate(half):
            self.put(C - n + i, y, c)
            self.put(C + n - 1 - i, y, c)

    def sprite(self, x0, y0, rows):
        for dy, row in enumerate(rows):
            for dx, c in enumerate(row):
                self.put(x0 + dx, y0 + dy, c)

    def outlined(self):
        out = Layer()
        out.px = dict(self.px)
        for (x, y) in list(self.px):
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if (nx, ny) not in self.px:
                    out.px.setdefault((nx, ny), "K")
        return out

    def svg(self):
        """Agrupa píxeles contiguos del mismo color por fila en un solo rect."""
        rects = []
        rows = {}
        for (x, y), c in self.px.items():
            rows.setdefault(y, []).append((x, c))
        for y, cells in rows.items():
            cells.sort()
            start, prev, col = cells[0][0], cells[0][0], cells[0][1]
            for x, c in cells[1:] + [(None, None)]:
                if x is not None and x == prev + 1 and c == col:
                    prev = x
                    continue
                rects.append(f'<rect x="{OX + start * P}" y="{OY + y * P}" width="{(prev - start + 1) * P}" height="{P}" fill="{PAL[col]}"/>')
                if x is not None:
                    start, prev, col = x, x, c
        return "".join(rects)


# ---------- cuerpo base ----------
base = Layer()
HEAD = [
    # rizos: silueta cuadrada, arriba plano con relieve
    "..HH.HHH.HHH", ".HHHHhHHHHhH", "HHhHHHHHhHHH", "HHHHHHhHHHHH",
    "HhHHHHHHHHhH", "HHHHhHHHHHHH", "HHHHHHHhHHHH", "HHHHHHHHHHHH",
    "HHHSSSSSSSS",           # 8  line-up: frente recta, esquinas en la sien
    "HfSSSSSSSSS",           # 9  degradado
    "fSSSSSSSSS",            # 10 cara estrecha (20 px) y alargada
    "fHHHHHSSSS",            # 11 cejas
    "SSSSSSSSSS",            # 12 espacio entre cejas y ojos
    ".sSKKKKKSSSS",          # 13 párpado + oreja
    "ssSWKDKWSSSS",          # 14 pupila con brillo
    "ssSWWKWWSSSS",          # 15
    "ssSSSSSSSSSS",          # 16
    ".sSSSSSSSSSL",          # 17 puente de la nariz
    "SSSSSSKsss",            # 18 nariz ancha
    "SSSSSSssss",            # 19 bigote ligero
    "SSSSMRRRRR",            # 20 labio superior, comisuras arriba
    "SSSSSMMMMM",            # 21
    "SSSSSSRRRR",            # 22 labio inferior
    "sSSSSSSSSS", ".sSSSSSSSS", "..sSSSSSSS", "...ssSSSSS", ".....sssss",  # mentón largo
    "sssss",                 # 28 cuello
]
for y, half in enumerate(HEAD):
    base.sym(y, half)

TORSO = [
    "TTTTtttttt", "TTTTTTTGTTTT", "TTTTTTTTTTGTTT", "TTTTTTTTTTTTGTT", "TTTTTTTTTTTTTTGT",
    "TTTTTTTTTTTTTTTTG", "tTTTTTTTTTTTTTTTTG", "tTTTTTTTTTTTTTTGGG",
]
for i, half in enumerate(TORSO):
    base.sym(29 + i, half)
for y in range(37, GH):
    base.sym(y, "T" * 18)
for y in range(37, 41):          # cruz (vertical)
    base.put(C - 1, y, "G"); base.put(C, y, "g")
for y, x in ((42, C - 12), (43, C - 12), (44, C + 9), (45, C + 9)):  # pliegues
    base.put(x, y, "t")
# logo </> en el pecho
for x, y, c in ((C + 6, 39, "V"), (C + 5, 40, "V"), (C + 6, 41, "V"),
                (C + 9, 38, "Y"), (C + 9, 39, "Y"), (C + 8, 40, "Y"), (C + 8, 41, "Y"),
                (C + 11, 39, "V"), (C + 12, 40, "V"), (C + 11, 41, "V")):
    base.put(x, y, c)

# ---------- brazos ----------
def arm_down(side):
    a = Layer()
    for y in range(35, 41):
        for dx in range(3):
            a.put(C + side * (18 + dx) - (1 if side > 0 else 0), y, "T")
    for y in range(41, 47):
        for dx in range(3):
            a.put(C + side * (18 + dx) - (1 if side > 0 else 0), y, "S" if dx else "s")
    return a


def wave_arm(shift):
    a = Layer()
    for y in range(33, 38):
        for dx in range(16, 20):
            a.put(C + dx, y, "T")
    for y in range(26, 33):
        for dx in range(17, 20):
            a.put(C + dx, y, "s" if dx == 17 else "S")
    top = Layer()
    for y in range(22, 26):
        for dx in range(17, 20):
            top.put(C + dx, y, "s" if dx == 17 else "S")
    top.sprite(C + 16, 14, [
        ".LS.L.", ".LSLSL", "LLSLSL", "LSSSSL", "SSSSSS", "sSSSSS", "sSSSSs", ".SSSS.",
    ])
    top.put(C + 15, 19, "S"); top.put(C + 15, 20, "s")   # pulgar
    top.put(C + 18, 17, "r")                               # anillo
    for (x, y), c in top.px.items():
        a.put(x + shift, y - (1 if shift else 0), c)
    return a


def thumbs_up():
    a = Layer()
    for y in range(35, 41):
        for dx in range(16, 19):
            a.put(C - dx - 1, y, "T")
    a.sprite(C - 17, 38, ["SSSSSSSSS", "sSSSSSSSS", ".sssssss."])     # antebrazo cruzando
    a.sprite(C - 10, 32, ["..LS.", "..SS.", "SSSSS", "LSSSs", "SSSSs", "sSSSs", ".sss."])  # puño + pulgar
    return a


# ---------- capas de cara ----------
def eye_cols(left):
    return range(C - 9, C - 4) if left else range(C + 4, C + 9)


def blank_eyes(layer, left=True, right=True):
    for side, on in ((True, left), (False, right)):
        if on:
            for y in (13, 14, 15):
                for x in eye_cols(side):
                    layer.put(x, y, "S")


catch = Layer()  # el brillo de la pupila ya está en la base

blink = Layer(); blank_eyes(blink)
for side in (True, False):
    for x in eye_cols(side):
        blink.put(x, 15, "K")

happy = Layer(); blank_eyes(happy)
for side in (True, False):
    xs = list(eye_cols(side))
    for x in xs[1:4]:
        happy.put(x, 13, "K")
    happy.put(xs[0], 14, "K"); happy.put(xs[4], 14, "K")

wink = Layer(); blank_eyes(wink, left=True, right=False)
xs = list(eye_cols(True))
for x in xs[1:4]:
    wink.put(x, 14, "K")
wink.put(xs[0], 13, "K"); wink.put(xs[4], 13, "K")

grin = Layer()
grin.sprite(C - 6, 20,["MWWWWWWWWWWM", ".MKKRRRRKKM.", "..RRRRRRRR.."])

# ---------- portátil visto por detrás (reemplaza la consola) ----------
console = Layer()
LID, LID_SH, LID_HI, BASE_C, BASE_D = "#A7AFC0", "#8A93A8", "#CDD3DF", "#5A6170", "#3A3F4B"
for col in (LID, LID_SH, LID_HI, BASE_C, BASE_D, "#E43B44", "#F7C33C", "#3C8DFF", "#3CCB6E", "#FFFFFF"):
    PAL[col] = col
for y in range(39, 50):
    for x in range(C - 14, C + 14):
        c = LID
        if x in (C - 14, C + 13) or y == 49:
            c = LID_SH
        if y == 39:
            c = LID_HI
        console.put(x, y, c)
for x in range(C - 17, C + 17):
    console.put(x, 50, BASE_C)
    console.put(x, 51, BASE_D)
# pegatinas de dev: Python, check verde, corazón
for x in range(C - 12, C - 9):
    console.put(x, 41, "#3C8DFF"); console.put(x, 42, "#3C8DFF"); console.put(x, 43, "#F7C33C"); console.put(x, 44, "#F7C33C")
for (x, y) in ((C + 8, 42), (C + 9, 43), (C + 10, 42), (C + 11, 41)):
    console.put(x, y, "#3CCB6E")
for (x, y) in ((C + 8, 45), (C + 10, 45), (C + 8, 46), (C + 9, 46), (C + 10, 46), (C + 9, 47)):
    console.put(x, y, "#E43B44")

# logo </> que brilla en la tapa
laptop_logo = Layer()
PAL["#C9B8FF"] = "#C9B8FF"
for (x, y) in ((C - 4, 42), (C - 5, 43), (C - 6, 44), (C - 5, 45), (C - 4, 46),
               (C + 3, 42), (C + 4, 43), (C + 5, 44), (C + 4, 45), (C + 3, 46)):
    laptop_logo.put(x, y, "V")
for (x, y) in ((C + 1, 42), (C, 43), (C, 44), (C - 1, 45), (C - 2, 46)):
    laptop_logo.put(x, y, "Y")


# ---------- animación ----------
def pct(t):
    return 100 * t / LOOP


def vis_keyframes(name, windows):
    """opacity 1 dentro de las ventanas de tiempo, 0 fuera (cambios secos)."""
    merged = []
    for a, b in sorted(windows):
        if merged and a <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(b, merged[-1][1]))
        else:
            merged.append((a, b))
    marks = [f"0% {{ opacity: {1 if merged[0][0] == 0 else 0}; }}"]
    for a, b in merged:
        if a > 0:
            marks.append(f"{pct(a) - 0.01:.2f}% {{ opacity: 0; }} {pct(a):.2f}% {{ opacity: 1; }}")
        if b < LOOP:
            marks.append(f"{pct(b) - 0.01:.2f}% {{ opacity: 1; }} {pct(b):.2f}% {{ opacity: 0; }}")
    marks.append(f"100% {{ opacity: {1 if merged[-1][1] >= LOOP else 0}; }}")
    return f"@keyframes {name} {{ {' '.join(marks)} }}\n.{name} {{ animation: {name} {LOOP}s linear infinite; }}"


css = []
for i, (a, b) in enumerate(SCENES):
    css.append(vis_keyframes(f"sc{i}", [(a, b)]))
css.append(vis_keyframes("armdownR", [SCENES[1], SCENES[2], SCENES[3]]))
css.append(vis_keyframes("armdownL", [SCENES[0], SCENES[2], SCENES[3]]))
css.append(vis_keyframes("eyesopen", [SCENES[0], SCENES[3]]))


def typing(name, start, chars, adv, x, y, w_box):
    """Cubre el texto y lo descubre letra a letra (steps)."""
    a, b = pct(start), pct(start + chars * 0.055)
    dist = chars * adv
    css.append(
        f"@keyframes {name} {{ 0% {{ transform: translateX(0); }} {a:.2f}% {{ transform: translateX(0); animation-timing-function: steps({chars}, end); }} "
        f"{b:.2f}% {{ transform: translateX({dist}px); }} 100% {{ transform: translateX({dist}px); }} }}\n"
        f".{name} {{ animation: {name} {LOOP}s linear infinite; }}")
    return (f'<clipPath id="c{name}"><rect x="{x}" y="{y - 14}" width="{w_box}" height="20"/></clipPath>'
            f'<g clip-path="url(#c{name})"><rect class="{name}" x="{x}" y="{y - 14}" width="{dist + 4}" height="20" fill="#1D3C8C"/></g>')


font_b64 = base64.b64encode(open(FONT, "rb").read()).decode()

# ---------- escena ----------
parts = []
parts.append(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" shape-rendering="crispEdges" role="img" aria-label="{TXT['aria']}">
<title>{TXT['title']}</title>
<defs>
<clipPath id="frame"><rect width="{W}" height="{H}" rx="14"/></clipPath>
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".07"/></pattern>
</defs>
<style>
@font-face {{ font-family: "PS2P"; src: url(data:font/woff2;base64,{font_b64}) format("woff2"); }}
text {{ font-family: "PS2P", ui-monospace, monospace; }}
.wa {{ animation: wa .5s linear infinite; }} .wb {{ animation: wa .5s linear infinite reverse; }}
@keyframes wa {{ 0%, 49.9% {{ opacity: 1; }} 50%, 100% {{ opacity: 0; }} }}
.tw {{ animation: tw 1.6s linear infinite; }}
.glowlogo {{ animation: glow 2.4s ease-in-out infinite; }}
@keyframes glow {{ 0%, 100% {{ opacity: .65; }} 50% {{ opacity: 1; }} }}
@keyframes tw {{ 0%, 59.9% {{ opacity: 1; }} 60%, 100% {{ opacity: .25; }} }}
.blinkfast {{ animation: tw .8s linear infinite; }}
.eyeblink {{ opacity: 0; animation: eb 3s linear infinite; }}
@keyframes eb {{ 0%, 84.9% {{ opacity: 0; }} 85%, 92% {{ opacity: 1; }} 92.1%, 100% {{ opacity: 0; }} }}
%%CSS%%
@media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
</style>
<g clip-path="url(#frame)">
<rect width="{W}" height="{H}" fill="#171A36"/>
''')

# ---------- fondo: cuarto de desarrollo de noche ----------
INKB = "#1F2340"
for x in range(36, W, 96):                       # paneles de la pared
    parts.append(f'<rect x="{x}" y="0" width="4" height="{H}" fill="#1C2043"/>')
CX_PX = OX + C * P                               # luz detrás del personaje (contraste)
parts.append(f'<rect x="{CX_PX - 92}" y="56" width="184" height="{H}" fill="#22274E"/>'
             f'<rect x="{CX_PX - 76}" y="66" width="152" height="{H}" fill="#293062"/>')

# notas adhesivas: problema -> idea -> solución
for i, (label, col) in enumerate((("BUG", "#FF6B8A"), ("IDEA", "#FFD84A"), ("FIX", "#5BE49B"))):
    x = 140 + i * 70
    parts.append(f'<rect x="{x + 3}" y="17" width="48" height="40" fill="#0E1024" opacity=".5"/>'
                 f'<rect x="{x}" y="14" width="48" height="40" fill="{col}"/>'
                 f'<rect x="{x + 40}" y="46" width="8" height="8" fill="#171A36"/><rect x="{x + 40}" y="46" width="8" height="8" fill="{col}" opacity=".55"/>'
                 f'<rect x="{x + 20}" y="10" width="8" height="6" fill="#E43B44"/>'
                 f'<text x="{x + 24}" y="40" font-size="8" fill="{INKB}" text-anchor="middle">{label}</text>')
    if i < 2:
        ax = x + 52
        parts.append(f'<g fill="#9FA6D8"><rect x="{ax}" y="32" width="10" height="4"/><rect x="{ax + 10}" y="28" width="4" height="12"/><rect x="{ax + 14}" y="32" width="2" height="4"/></g>')


def monitor(x, y, w, h):
    return (f'<rect x="{x + 4}" y="{y + 4}" width="{w}" height="{h}" fill="#0E1024" opacity=".6"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#2B2F45"/>'
            f'<rect x="{x + 6}" y="{y + 6}" width="{w - 12}" height="{h - 14}" fill="#0B1020"/>'
            f'<rect x="{x + 6}" y="{y + 6}" width="{w - 12}" height="3" fill="#18213F"/>'
            f'<rect class="tw" x="{x + w - 12}" y="{y + h - 6}" width="4" height="3" fill="#3CCB6E"/>'
            f'<rect x="{x + w // 2 - 6}" y="{y - 10}" width="12" height="10" fill="#2B2F45"/>')


# monitor A: el código que resuelve problemas
MAX, MAY = 8, 70
parts.append(monitor(MAX, MAY, 148, 108))
code = [
    (f'<tspan fill="#B392F0">def</tspan> <tspan fill="#00D4FF">{TXT["code"][0]}</tspan>(p):'),
    (f'  a=<tspan fill="#00D4FF">{TXT["code"][1]}</tspan>(p)'),
    (f'  d=<tspan fill="#00D4FF">{TXT["code"][2]}</tspan>(a)'),
    (f'  c=<tspan fill="#00D4FF">{TXT["code"][3]}</tspan>(d)'),
    (f'  <tspan fill="#00D4FF">{TXT["code"][4]}</tspan>(c)'),
    ('  <tspan fill="#B392F0">return</tspan> c'),
]
for i, line in enumerate(code):
    parts.append(f'<text x="{MAX + 12}" y="{MAY + 26 + i * 13}" font-size="8" fill="#C9D1D9" xml:space="preserve">{line}</text>')
parts.append(f'<rect class="blinkfast" x="{MAX + 100}" y="{MAY + 85}" width="7" height="8" fill="#C9D1D9"/>')

# monitor B: terminal, los tests pasan y se despliega
MBX, MBY = 338, 70
parts.append(monitor(MBX, MBY, 122, 108))
term = [("$ pytest", "#C9D1D9"), ("12 passed", "#5BE49B"), ("$ git push", "#C9D1D9"), ("deploy: OK", "#5BE49B")]
TERM_LOOP = 7.0
for i, (txt, col) in enumerate(term):
    a = 100 * (0.4 + i * 1.1) / TERM_LOOP
    css.append(f"@keyframes tl{i} {{ 0%, {a - 0.01:.2f}% {{ opacity: 0; }} {a:.2f}%, 95% {{ opacity: 1; }} 95.01%, 100% {{ opacity: 0; }} }}\n"
               f".tl{i} {{ opacity: 0; animation: tl{i} {TERM_LOOP}s linear infinite; }}")
    parts.append(f'<text class="tl{i}" x="{MBX + 12}" y="{MBY + 28 + i * 16}" font-size="8" fill="{col}">{txt}</text>')
parts.append(f'<rect class="blinkfast" x="{MBX + 12}" y="{MBY + 86}" width="7" height="8" fill="#C9D1D9"/>')

# pizarra: ciclo de vida del software, la fase activa se ilumina
WBX, WBY, WBW, WBH = 470, 78, 360, 138
parts.append(f'<rect x="{WBX + 5}" y="{WBY + 5}" width="{WBW}" height="{WBH}" fill="#0E1024" opacity=".6"/>'
             f'<rect x="{WBX}" y="{WBY}" width="{WBW}" height="{WBH}" fill="#8A93A8"/>'
             f'<rect x="{WBX + 5}" y="{WBY + 5}" width="{WBW - 10}" height="{WBH - 10}" fill="#E4E9F4"/>'
             f'<text x="{WBX + WBW // 2}" y="{WBY + 22}" font-size="8" fill="{INKB}" text-anchor="middle">{TXT["board"]}</text>')
BOXW, BOXH, R1, R2 = 76, 24, WBY + 32, WBY + 92
BXS = [478, 566, 654, 742]
steps = [(TXT["steps"][0], BXS[0], R1, "#E5484D"), (TXT["steps"][1], BXS[1], R1, "#7F5AF0"), (TXT["steps"][2], BXS[2], R1, "#7F5AF0"),
         (TXT["steps"][3], BXS[3], R1, "#7F5AF0"), (TXT["steps"][4], BXS[3], R2, "#00A3CC"), (TXT["steps"][5], BXS[2], R2, "#00A3CC"),
         (TXT["steps"][6], BXS[1], R2, "#30A46C")]
SDLC_LOOP = 7.0
win = 100 / len(steps)
for i, (label, bx, by, col) in enumerate(steps):
    css.append(f"@keyframes wb{i} {{ 0%, {win - 0.1:.2f}% {{ fill: {col}; }} {win:.2f}%, 100% {{ fill: #E4E9F4; }} }}\n"
               f"@keyframes wt{i} {{ 0%, {win - 0.1:.2f}% {{ fill: #FFFFFF; }} {win:.2f}%, 100% {{ fill: {INKB}; }} }}\n"
               f".wb{i} {{ fill: #E4E9F4; animation: wb{i} {SDLC_LOOP}s linear {i:.0f}s infinite; }}\n"
               f".wt{i} {{ fill: {INKB}; animation: wt{i} {SDLC_LOOP}s linear {i:.0f}s infinite; }}")
    parts.append(f'<rect x="{bx}" y="{by}" width="{BOXW}" height="{BOXH}" fill="{col}"/>'
                 f'<rect class="wb{i}" x="{bx + 3}" y="{by + 3}" width="{BOXW - 6}" height="{BOXH - 6}"/>'
                 f'<text class="wt{i}" x="{bx + BOXW // 2}" y="{by + 16}" font-size="8" text-anchor="middle">{label}</text>')
ARW = "#5A6382"
for bx in BXS[:3]:                                # fila 1: hacia la derecha
    ax, ay = bx + BOXW + 1, R1 + 10
    parts.append(f'<g fill="{ARW}"><rect x="{ax}" y="{ay}" width="7" height="4"/><rect x="{ax + 6}" y="{ay - 2}" width="3" height="8"/></g>')
parts.append(f'<g fill="{ARW}"><rect x="{BXS[3] + 36}" y="{R1 + BOXH + 1}" width="4" height="30"/><rect x="{BXS[3] + 34}" y="{R2 - 6}" width="8" height="4"/></g>')
for bx in BXS[1:3]:                               # fila 2: hacia la izquierda
    ax, ay = bx + BOXW + 3, R2 + 10
    parts.append(f'<g fill="{ARW}"><rect x="{ax}" y="{ay}" width="7" height="4"/><rect x="{ax - 2}" y="{ay - 2}" width="3" height="8"/></g>')
# vuelta al inicio: de la solución a un nuevo problema
parts.append(f'<g fill="{ARW}"><rect x="{BXS[0] + 36}" y="{R2 + 10}" width="{BXS[1] - BXS[0] - 38}" height="4"/>'
             f'<rect x="{BXS[0] + 36}" y="{R1 + BOXH + 6}" width="4" height="{R2 - R1 - BOXH - 2}"/>'
             f'<rect x="{BXS[0] + 33}" y="{R1 + BOXH + 2}" width="10" height="4"/></g>'
             f'<text x="{BXS[0] + 4}" y="{R2 + 30}" font-size="6" fill="#5A6382">{TXT["iterate"]}</text>')
parts.append(f'<rect x="{WBX + 30}" y="{WBY + WBH}" width="{WBW - 60}" height="5" fill="#6E7690"/>'
             f'<rect x="{WBX + 60}" y="{WBY + WBH - 3}" width="18" height="4" fill="#E43B44"/><rect x="{WBX + 84}" y="{WBY + WBH - 3}" width="18" height="4" fill="#3C8DFF"/>')

# escritorio
parts.append(f'<rect y="{H - 53}" width="{W}" height="7" fill="#4A3A62"/><rect y="{H - 46}" width="{W}" height="46" fill="#3B2C4F"/>')
for x in range(0, W, 28):
    parts.append(f'<rect x="{x}" y="{H - 30}" width="14" height="4" fill="#33264A"/>')

# taza de café con vapor
MX, MY = 404, H - 75
parts.append(f'<rect x="{MX}" y="{MY}" width="20" height="22" fill="#E8ECF5"/><rect x="{MX}" y="{MY + 8}" width="20" height="5" fill="#7F5AF0"/>'
             f'<rect x="{MX + 20}" y="{MY + 5}" width="6" height="3" fill="#E8ECF5"/><rect x="{MX + 23}" y="{MY + 5}" width="3" height="12" fill="#E8ECF5"/><rect x="{MX + 20}" y="{MY + 14}" width="6" height="3" fill="#E8ECF5"/>'
             f'<rect x="{MX + 2}" y="{MY}" width="16" height="3" fill="#5B3A25"/>')
css.append("@keyframes steam { 0% { transform: translateY(0); opacity: 0; } 30% { opacity: .8; } 100% { transform: translateY(-14px); opacity: 0; } }\n"
           ".steam { animation: steam 2.4s steps(6, end) infinite; }")
for k, dx in enumerate((4, 12)):
    parts.append(f'<g class="steam" style="animation-delay:{k * 1.2}s" fill="#C9D1D9"><rect x="{MX + dx}" y="{MY - 8}" width="3" height="3"/><rect x="{MX + dx + 2}" y="{MY - 12}" width="3" height="3"/></g>')

# personaje
def g(cls, layer, outline=True):
    l = layer.outlined() if outline else layer
    return f'<g class="{cls}">{l.svg()}</g>'


parts.append(g("", base))
parts.append(g("armdownL", arm_down(-1)))
parts.append(g("armdownR", arm_down(1)))
parts.append(f'<g class="sc0">{g("wa", wave_arm(0))}{g("wb", wave_arm(1))}</g>')
parts.append(f'<g class="sc1">{g("", thumbs_up())}{g("", wink, False)}</g>')
parts.append(f'<g class="eyesopen">{g("", catch, False)}</g>')
parts.append(f'<g class="sc2">{g("", happy, False)}</g>')
parts.append(f'<g class="sc0">{g("", grin, False)}</g><g class="sc2">{g("", grin, False)}</g>')
parts.append(f'<g class="sc3"><g class="eyeblink">{blink.svg()}</g></g>')
# aretes de diamante con brillo
for x in (C - 11, C + 10):
    parts.append(f'<rect class="tw" x="{OX + x * P}" y="{OY + 17 * P}" width="{P}" height="{P}" fill="#FFFFFF"/>')
parts.append(g("", console))
parts.append(f'<g class="glowlogo">{laptop_logo.svg()}</g>')


def bulb(x, y):
    o = []
    rays = [(-3, 2, 2, 1), (9, 2, 2, 1), (3, -4, 1, 2), (-2, -2, 1, 1), (8, -2, 1, 1)]
    for dx, dy, w_, h_ in rays:
        o.append(f'<rect class="blinkfast" x="{x + dx * 6}" y="{y + dy * 6}" width="{w_ * 6}" height="{h_ * 6}" fill="#FFE45C"/>')
    shape = [".KKKKK.", "KYYYYWK", "KYYYYYK", "KYYYYYK", ".KYYYK.", "..KGK..", "..KgK..", "...K..."]
    cmap = {"K": "#3A2410", "Y": "#FFE45C", "W": "#FFFFFF", "G": "#9AA3B5", "g": "#6E7686"}
    for r, row in enumerate(shape):
        for cidx, ch in enumerate(row):
            if ch != ".":
                o.append(f'<rect x="{x + cidx * 6}" y="{y + r * 6}" width="6" height="6" fill="{cmap[ch]}"/>')
    return "".join(o)


parts.append(f'<g class="sc2">{bulb(OX + (C - 22) * P, OY + 2 * P)}{bulb(OX + (C + 15) * P, OY + 2 * P)}</g>')

# HUD
parts.append('<text class="blinkfast" x="700" y="38" font-size="18" fill="#FFFFFF" stroke="#3A2410" stroke-width="1">1-UP</text>')
for i, sc in enumerate(("000128", "004096", "065536", "999999")):
    parts.append(f'<text class="sc{i}" x="664" y="66" font-size="18" fill="#FFFFFF" stroke="#3A2410" stroke-width="1">{sc}</text>')
parts.append(f'<g fill="#E43B44">' + "".join(
    f'<rect x="{30 + k * 26}" y="22" width="6" height="6"/><rect x="{42 + k * 26}" y="22" width="6" height="6"/><rect x="{28 + k * 26}" y="26" width="22" height="8"/><rect x="{32 + k * 26}" y="34" width="14" height="5"/><rect x="{36 + k * 26}" y="39" width="6" height="4"/>'
    for k in range(3)) + '</g>')

# caja de diálogo
BX, BY, BW, BH = 462, 250, 368, 132
parts.append(f'<rect x="{BX - 4}" y="{BY - 4}" width="{BW + 8}" height="{BH + 8}" fill="#0E1A3A"/>'
             f'<rect x="{BX}" y="{BY}" width="{BW}" height="{BH}" fill="#1D3C8C"/>'
             f'<rect x="{BX}" y="{BY}" width="{BW}" height="4" fill="#3E63C4"/>'
             f'<rect x="{BX - 4}" y="{BY - 4}" width="{BW + 8}" height="{BH + 8}" fill="none" stroke="#9FB8F5" stroke-width="2"/>')
parts.append(f'<rect x="{BX + 8}" y="{BY - 26}" width="138" height="26" fill="#1D3C8C" stroke="#9FB8F5" stroke-width="2"/>'
             f'<text x="{BX + 18}" y="{BY - 7}" font-size="12" fill="#FFFFFF">JEREMY</text>'
             f'<g fill="#FF5A6E"><rect x="{BX + 120}" y="{BY - 18}" width="4" height="4"/><rect x="{BX + 128}" y="{BY - 18}" width="4" height="4"/>'
             f'<rect x="{BX + 118}" y="{BY - 15}" width="16" height="5"/><rect x="{BX + 121}" y="{BY - 10}" width="10" height="3"/><rect x="{BX + 124}" y="{BY - 7}" width="4" height="3"/></g>')

FS, ADV = 13, 13
MSGS = TXT["msgs"]
for i, (l1, l2) in enumerate(MSGS):
    t0 = SCENES[i][0] + 0.15
    y1, y2 = BY + 46, BY + 82
    color2 = "#FFE45C" if i == 3 else "#CFE0FF"
    parts.append(f'<g class="sc{i}">'
                 f'<text x="{BX + 20}" y="{y1}" font-size="{FS}" fill="#FFFFFF">{escape(l1)}</text>'
                 f'<text x="{BX + 20}" y="{y2}" font-size="{FS}" fill="{color2}">{escape(l2)}</text>'
                 + typing(f"ty{i}a", t0, len(l1), ADV, BX + 20, y1, BW - 30)
                 + typing(f"ty{i}b", t0 + len(l1) * 0.055 + 0.1, len(l2), ADV, BX + 20, y2, BW - 30)
                 + '</g>')
# indicador ▼
parts.append(f'<g class="blinkfast" fill="#FFFFFF"><rect x="{BX + BW - 30}" y="{BY + BH - 22}" width="12" height="4"/><rect x="{BX + BW - 27}" y="{BY + BH - 18}" width="6" height="4"/></g>')

parts.append(f'<rect width="{W}" height="{H}" fill="url(#scan)"/></g>')
parts.append(f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="none" stroke="#30363D" stroke-width="2"/></svg>')

with open(OUT, "w", encoding="utf-8") as fh:
    # el CSS se inserta al final: typing() agrega reglas mientras se arma la escena
    fh.write("\n".join(parts).replace("%%CSS%%", "\n".join(css), 1) + "\n")
