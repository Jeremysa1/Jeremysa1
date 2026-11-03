"""Genera el ciclo de vida del software animado (CSS + SMIL).

Uso: python gen_ciclo.py <salida.svg> [es|en]
"""
import math
import sys

W, H = 854, 380
CX, CY, R = 235, 196, 118
STEP = 2.2  # segundos por fase
VIOLET, CYAN, INK, MUTED, BG, LINE = "#7F5AF0", "#00D4FF", "#E6EDF3", "#8B949E", "#0D1117", "#30363D"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"

LANG = sys.argv[2] if len(sys.argv) > 2 else "es"
TXT = {
    "es": {
        "phases": [
            ("Problema", "Entender el dolor real", "antes de escribir una línea."),
            ("Análisis", "Usuarios, requisitos", "y restricciones."),
            ("Diseño", "Arquitectura, modelo de datos", "e infraestructura."),
            ("Desarrollo", "Código limpio, revisado", "y versionado con Git."),
            ("Pruebas", "Validar que funciona", "y que no se rompe."),
            ("Despliegue", "Contenedores, CI/CD", "y entrega continua."),
            ("Solución", "Valor real para el usuario...", "y se vuelve a iterar."),
        ],
        "aria": "Ciclo de vida del software: del problema a la solución",
        "title": "Ciclo de vida del software", "kicker": "// ciclo de vida del software",
        "center": "problema → solución", "phase": "FASE", "footer": "Así construyo software.",
    },
    "en": {
        "phases": [
            ("Problem", "Understand the real pain", "before writing a single line."),
            ("Analysis", "Users, requirements", "and constraints."),
            ("Design", "Architecture, data model", "and infrastructure."),
            ("Build", "Clean, reviewed code", "versioned with Git."),
            ("Testing", "Prove it works", "and that it doesn't break."),
            ("Deploy", "Containers, CI/CD", "and continuous delivery."),
            ("Solution", "Real value for users...", "and then we iterate."),
        ],
        "aria": "Software development life cycle: from problem to solution",
        "title": "Software development life cycle", "kicker": "// software development life cycle",
        "center": "problem → solution", "phase": "PHASE", "footer": "This is how I build software.",
    },
}[LANG]
PHASES = TXT["phases"]
N = len(PHASES)
TOTAL = STEP * N
WIN = 100 / N  # % del ciclo que cada fase está activa


def pos(i, radius):
    a = math.radians(-90 + i * 360 / N)
    return CX + radius * math.cos(a), CY + radius * math.sin(a)


def delay(i):
    # cada fase se enciende medio paso antes de que llegue el cometa y se apaga medio paso después
    return f"{i * STEP - STEP / 2:.2f}s"


def step_keyframes():
    # fase i: activa (cian) en su turno, completada (violeta) hasta que el ciclo reinicia, pendiente (gris) después
    rules = []
    for i in range(N):
        done_end = 100 - i * WIN
        kf = [f"0%, {WIN - 0.5:.2f}% {{ fill: {CYAN}; stroke: {CYAN}; }}",
              f"{WIN:.2f}%, {done_end - 0.3:.2f}% {{ fill: {VIOLET}; stroke: {VIOLET}; }}"]
        if i:
            kf.append(f"{done_end:.2f}%, 100% {{ fill: {BG}; stroke: {LINE}; }}")
        rules.append(f"  @keyframes step{i} {{ {' '.join(kf)} }}")
        rules.append(f"  @keyframes seg{i} {{ {' '.join(kf).replace(f'fill: {BG}', f'fill: {LINE}')} }}")
    return "\n".join(rules)


def anim(name, i):
    return f"animation:{name}{i} {TOTAL:.1f}s linear infinite;animation-delay:{delay(i)}"


out = []
out.append(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{TXT['aria']}">
<title>{TXT['title']}</title>
<defs>
  <linearGradient id="ring" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{VIOLET}"/>
  </linearGradient>
  <radialGradient id="glow"><stop offset="0" stop-color="{CYAN}" stop-opacity=".9"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
  <radialGradient id="bgGlow" cx="{CX / W:.3f}" cy=".5" r=".55"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".16"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>
</defs>
<style>
  text {{ font-family: {MONO}; }}
  .node {{ fill: {BG}; stroke: {LINE}; stroke-width: 2; }}
  .lbl {{ fill: {MUTED}; font-size: 13px; animation: lblOn {TOTAL:.1f}s linear infinite; }}
  .seg {{ fill: {LINE}; stroke: none; }}
  .panel {{ opacity: 0; animation: show {TOTAL:.1f}s linear infinite; }}
  @keyframes lblOn {{ 0%, {WIN - 0.5:.2f}% {{ fill: {INK}; font-weight: 700; }} {WIN:.2f}%, 100% {{ fill: {MUTED}; font-weight: 400; }} }}
{step_keyframes()}
  @keyframes show {{
    0% {{ opacity: 0; transform: translateY(6px); }}
    2% {{ opacity: 1; transform: none; }}
    {WIN - 1.5:.2f}% {{ opacity: 1; transform: none; }}
    {WIN - 0.3:.2f}%, 100% {{ opacity: 0; }}
  }}
  @media (prefers-reduced-motion: reduce) {{ .node, .lbl, .seg, .panel {{ animation: none !important; }} .panel.p0 {{ opacity: 1; }} }}
</style>
<rect width="{W}" height="{H}" rx="14" fill="{BG}"/>
<rect width="{W}" height="{H}" rx="14" fill="url(#bgGlow)"/>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="none" stroke="{LINE}"/>
<text x="500" y="84" font-size="13" fill="{MUTED}">{TXT['kicker']}</text>
''')

# anillo base y arco de progreso animado
circ = 2 * math.pi * R
out.append(f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="none" stroke="{LINE}" stroke-width="2"/>')
out.append(
    f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="none" stroke="url(#ring)" stroke-width="3" stroke-linecap="round" '
    f'stroke-dasharray="{circ:.1f}" transform="rotate(-90 {CX} {CY})">'
    f'<animate attributeName="stroke-dashoffset" values="{circ:.1f};0" dur="{TOTAL:.1f}s" repeatCount="indefinite"/></circle>'
)

# centro
out.append(f'<text x="{CX}" y="{CY - 6}" text-anchor="middle" font-size="30" font-weight="700" fill="{INK}">&lt;/&gt;</text>')
out.append(f'<text x="{CX}" y="{CY + 20}" text-anchor="middle" font-size="12" fill="{MUTED}">{TXT["center"]}</text>')

# nodos y etiquetas
for i, (name, _, _) in enumerate(PHASES):
    x, y = pos(i, R)
    lx, ly = pos(i, R + 24)
    anchor = "middle" if abs(lx - CX) < 12 else ("start" if lx > CX else "end")
    ly += 4 if abs(ly - CY) < R else (-4 if ly < CY else 12)
    out.append(f'<circle class="node" cx="{x:.1f}" cy="{y:.1f}" r="8" style="{anim('step', i)}"/>')
    out.append(f'<text class="lbl" x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}" style="animation-delay:{delay(i)}">{name}</text>')

# cometa que recorre el ciclo
path = f"M {CX} {CY - R} A {R} {R} 0 1 1 {CX} {CY + R} A {R} {R} 0 1 1 {CX} {CY - R}"
out.append(f'<g><circle r="16" fill="url(#glow)"/><circle r="5" fill="#fff"/>'
           f'<animateMotion dur="{TOTAL:.1f}s" repeatCount="indefinite" path="{path}"/></g>')

# separador
out.append(f'<line x1="468" y1="70" x2="468" y2="{H - 50}" stroke="{LINE}"/>')

# panel de la derecha: una fase visible a la vez
PX = 500
for i, (name, l1, l2) in enumerate(PHASES):
    out.append(f'<g class="panel p{i}" style="animation-delay:{delay(i)}">')
    out.append(f'<text x="{PX}" y="128" font-size="14" fill="{VIOLET}" font-weight="700">{TXT["phase"]} {i + 1:02d} / {N:02d}</text>')
    out.append(f'<text x="{PX}" y="176" font-size="38" font-weight="700" fill="{INK}">{name}</text>')
    out.append(f'<text x="{PX}" y="214" font-size="16" fill="{MUTED}">{l1}</text>')
    out.append(f'<text x="{PX}" y="238" font-size="16" fill="{MUTED}">{l2}</text>')
    out.append('</g>')

# barra de progreso por segmentos
seg_w, gap = 40, 6
for i in range(N):
    x = PX + i * (seg_w + gap)
    out.append(f'<rect class="seg" x="{x}" y="282" width="{seg_w}" height="5" rx="2.5" style="{anim('seg', i)}"/>')

out.append(f'<text x="{PX}" y="318" font-size="12" fill="{MUTED}">{TXT["footer"]}</text>')
out.append('</svg>')

with open(sys.argv[1], "w", encoding="utf-8") as f:
    f.write("\n".join(out) + "\n")
