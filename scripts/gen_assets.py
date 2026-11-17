"""Genera los recursos visuales del perfil en estilo sobrio.

Uso: python gen_assets.py <carpeta_assets>
Salida: header.svg, workspace(-en).svg, focus(-en).svg, footer.svg y los botones de idioma.
"""
import os
import sys
from html import escape

OUT = sys.argv[1]
W = 854
BG, PANEL, LINE, INK, MUTED = "#0D1117", "#161B22", "#30363D", "#E6EDF3", "#8B949E"
VIOLET, CYAN, GREEN = "#7F5AF0", "#00D4FF", "#3FB950"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"


def svg(w, h, body, label, css=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}">'
            f'<title>{escape(label)}</title>'
            f'<style>text {{ font-family: {SANS}; }} .m {{ font-family: {MONO}; }} {css}'
            f'@media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; opacity: 1 !important; }} }}</style>'
            f'{body}</svg>')


def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
        fh.write(content)


def appear(name, start, loop):
    """Regla CSS: el elemento aparece en `start` segundos y se mantiene hasta casi el final del ciclo."""
    a = 100 * start / loop
    return (f"@keyframes {name} {{ 0%, {a:.2f}% {{ opacity: 0; }} {a + 1.5:.2f}%, 96% {{ opacity: 1; }} 100% {{ opacity: 0; }} }} "
            f".{name} {{ opacity: 0; animation: {name} {loop}s linear infinite; }} ")


# ---------- cabecera ----------
def header():
    h = 190
    body = (
        '<defs>'
        '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0D1117"/><stop offset=".6" stop-color="#131829"/><stop offset="1" stop-color="#1D1B3F"/></linearGradient>'
        f'<radialGradient id="glow" cx=".85" cy=".2" r=".6"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".3"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>'
        f'<linearGradient id="accent" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{VIOLET}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>'
        '<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.1" fill="#FFFFFF" fill-opacity=".06"/></pattern>'
        '</defs>'
        f'<rect width="{W}" height="{h}" rx="14" fill="url(#bg)"/>'
        f'<rect width="{W}" height="{h}" rx="14" fill="url(#dots)"/>'
        f'<rect width="{W}" height="{h}" rx="14" fill="url(#glow)"/>'
        f'<rect x=".5" y=".5" width="{W - 1}" height="{h - 1}" rx="14" fill="none" stroke="{LINE}"/>'
        f'<text x="{W // 2}" y="70" font-size="13" font-weight="600" letter-spacing="3" fill="{CYAN}" text-anchor="middle">SOFTWARE ENGINEER  ·  BACKEND  ·  DATA  ·  CLOUD</text>'
        f'<text x="{W // 2}" y="122" font-size="46" font-weight="700" fill="{INK}" text-anchor="middle">Jeremy Sánchez</text>'
        f'<rect x="{W // 2 - 32}" y="142" width="64" height="4" rx="2" fill="url(#accent)"/>'
    )
    return svg(W, h, body, "Jeremy Sánchez — Software Engineer · Backend · Data · Cloud")


# ---------- espacio de trabajo: editor, terminal y del problema a la solución ----------
def window(x, y, w, h, title):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{BG}" stroke="{LINE}"/>'
            f'<path d="M{x} {y + 34} h{w}" stroke="{LINE}"/>'
            + "".join(f'<circle cx="{x + 18 + k * 16}" cy="{y + 17}" r="5" fill="{c}"/>' for k, c in enumerate(("#FF5F57", "#FEBC2E", "#28C840")))
            + f'<text class="m" x="{x + w // 2}" y="{y + 22}" font-size="12" fill="{MUTED}" text-anchor="middle">{escape(title)}</text>')


def workspace(lang):
    t = {"es": {"steps": ["Problema", "Idea", "Solución"], "caption": "// del problema a la solución",
                "aria": "Editor con el proceso de un ingeniero, terminal con pruebas y despliegue, y el paso del problema a la solución"},
         "en": {"steps": ["Problem", "Idea", "Solution"], "caption": "// from problem to solution",
                "aria": "Editor with an engineer's process, terminal with tests and deploy, and the path from problem to solution"}}[lang]
    h, loop = 340, 14.0
    k, f, s = '<tspan fill="#B392F0">', '<tspan fill="#79C0FF">', '<tspan fill="#A5D6FF">'
    e = "</tspan>"
    code = [
        f'{k}class{e} {f}Engineer{e}:',
        f'    name  = {s}"Jeremy Sánchez"{e}',
        f'    focus = [{s}"backend"{e}, {s}"data"{e}, {s}"cloud"{e}]',
        '',
        f'    {k}def{e} {f}solve{e}(self, problem):',
        f'        req  = {f}analyze{e}(problem)',
        f'        arch = {f}design{e}(req)',
        f'        app  = {f}build{e}(arch)',
        f'        {f}test{e}(app)',
        f'        {k}return{e} {f}deploy{e}(app)',
    ]
    term = [("$ pytest -q", "#C9D1D9"), ("12 passed in 0.84s", GREEN), ("$ docker build -t app .", "#C9D1D9"),
            ("$ git push origin main", "#C9D1D9"), ("✓ deploy: ok", GREEN)]
    css, body = [], []
    body.append(f'<rect width="{W}" height="{h}" rx="14" fill="{PANEL}"/><rect x=".5" y=".5" width="{W - 1}" height="{h - 1}" rx="14" fill="none" stroke="{LINE}"/>')

    # editor
    ex, ey, ew, eh = 24, 24, 470, 292
    body.append(window(ex, ey, ew, eh, "engineer.py"))
    for i, ln in enumerate(code):
        y = ey + 62 + i * 23
        body.append(f'<text class="m" x="{ex + 30}" y="{y}" font-size="12" fill="#484F58" text-anchor="end">{i + 1}</text>')
        if ln:
            css.append(appear(f"c{i}", 0.4 + i * 0.4, loop))
            body.append(f'<text class="m c{i}" x="{ex + 46}" y="{y}" font-size="13" fill="#C9D1D9" xml:space="preserve">{ln}</text>')

    # terminal
    tx, ty, tw, th = 510, 24, 320, 172
    body.append(window(tx, ty, tw, th, "terminal"))
    for i, (txt, col) in enumerate(term):
        css.append(appear(f"t{i}", 5.0 + i * 0.9, loop))
        body.append(f'<text class="m t{i}" x="{tx + 18}" y="{ty + 60 + i * 23}" font-size="13" fill="{col}">{escape(txt)}</text>')

    # del problema a la solución
    px, py, pw, ph = 510, 208, 320, 108
    body.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="10" fill="{BG}" stroke="{LINE}"/>'
                f'<text class="m" x="{px + 18}" y="{py + 28}" font-size="12" fill="{MUTED}">{escape(t["caption"])}</text>')
    colors = ("#F85149", "#D29922", GREEN)
    step_loop = 6.0
    css.append(f"@keyframes chip {{ 0%, 30% {{ fill-opacity: .22; stroke-opacity: 1; }} 34%, 100% {{ fill-opacity: 0; stroke-opacity: .45; }} }} "
               f".chip {{ fill-opacity: 0; stroke-opacity: .45; animation: chip {step_loop}s linear infinite; }} ")
    for i, (label, col) in enumerate(zip(t["steps"], colors)):
        cx = px + 16 + i * 104
        body.append(f'<rect class="chip" style="animation-delay:{i * step_loop / 3:.1f}s" x="{cx}" y="{py + 48}" width="80" height="36" rx="8" fill="{col}" stroke="{col}"/>'
                    f'<text x="{cx + 40}" y="{py + 71}" font-size="13" font-weight="600" fill="{INK}" text-anchor="middle">{escape(label)}</text>')
        if i < 2:
            ax = cx + 86
            body.append(f'<path d="M{ax} {py + 66} h12 m-4 -4 l4 4 l-4 4" fill="none" stroke="{MUTED}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>')
    return svg(W, h, "".join(body), t["aria"], "".join(css))


# ---------- enfoque actual ----------
def focus(lang):
    t = {"es": {"kicker": "OBJETIVO ACTUAL", "title": "Certificación de Arquitecto de Soluciones", "status": "En progreso",
                "items": [("Azure", "Servicios y arquitectura cloud"), ("Infraestructura cloud", "Cómo se construye la infraestructura"),
                          ("Infraestructura como código", "Infra reproducible y versionada"), ("TypeScript", "A mayor profundidad"),
                          ("Java", "A mayor profundidad")],
                "goal": ("Meta", "Diseñar soluciones cloud de punta a punta"),
                "aria": "Objetivo actual: certificación de Arquitecto de Soluciones. Aprendiendo Azure, infraestructura cloud, infraestructura como código, TypeScript y Java"},
         "en": {"kicker": "CURRENT GOAL", "title": "Solutions Architect certification", "status": "In progress",
                "items": [("Azure", "Cloud services and architecture"), ("Cloud infrastructure", "How infrastructure is built"),
                          ("Infrastructure as code", "Reproducible, versioned infra"), ("TypeScript", "Going deeper"),
                          ("Java", "Going deeper")],
                "goal": ("Goal", "Designing cloud solutions end to end"),
                "aria": "Current goal: Solutions Architect certification. Learning Azure, cloud infrastructure, infrastructure as code, TypeScript and Java"}}[lang]
    h = 262
    css = "@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: .35; } } .pulse { animation: pulse 2s ease-in-out infinite; } "
    sw = 30 + len(t["status"]) * 7.2
    body = [f'<rect width="{W}" height="{h}" rx="14" fill="{PANEL}"/><rect x=".5" y=".5" width="{W - 1}" height="{h - 1}" rx="14" fill="none" stroke="{LINE}"/>',
            f'<text x="28" y="40" font-size="12" font-weight="600" letter-spacing="2" fill="{CYAN}">{escape(t["kicker"])}</text>',
            f'<text x="28" y="72" font-size="22" font-weight="700" fill="{INK}">{escape(t["title"])}</text>',
            f'<rect x="{W - 28 - sw:.0f}" y="24" width="{sw:.0f}" height="26" rx="13" fill="{BG}" stroke="{LINE}"/>',
            f'<circle class="pulse" cx="{W - 28 - sw + 15:.0f}" cy="37" r="4" fill="{GREEN}"/>',
            f'<text x="{W - 28 - sw + 26:.0f}" y="41.5" font-size="12" font-weight="600" fill="{INK}">{escape(t["status"])}</text>',
            f'<path d="M28 92 H{W - 28}" stroke="{LINE}"/>']
    cells = t["items"] + [t["goal"]]
    for i, (title, sub) in enumerate(cells):
        x, y = 28 + (i % 2) * 410, 112 + (i // 2) * 48
        goal = i == len(cells) - 1
        col = CYAN if goal else VIOLET
        body.append(f'<rect x="{x}" y="{y}" width="4" height="34" rx="2" fill="{col}"/>'
                    f'<text x="{x + 16}" y="{y + 14}" font-size="14" font-weight="600" fill="{INK}">{escape(title)}</text>'
                    f'<text x="{x + 16}" y="{y + 31}" font-size="12" fill="{MUTED}">{escape(sub)}</text>')
    return svg(W, h, "".join(body), t["aria"], css)


# ---------- pie y botones de idioma ----------
def footer():
    body = (f'<defs><linearGradient id="l" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{VIOLET}" stop-opacity="0"/>'
            f'<stop offset=".35" stop-color="{VIOLET}"/><stop offset=".65" stop-color="{CYAN}"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient></defs>'
            f'<rect x="0" y="9" width="{W}" height="2" rx="1" fill="url(#l)"/>')
    return svg(W, 20, body, "")


def button(label, on):
    w = 124
    body = (f'<rect x=".5" y=".5" width="{w - 1}" height="33" rx="17" fill="{"#1B1F3B" if on else BG}" stroke="{VIOLET if on else LINE}"/>'
            f'<text x="{w // 2}" y="22" font-size="13" font-weight="600" fill="{INK if on else MUTED}" text-anchor="middle">{escape(label)}</text>')
    return svg(w, 34, body, label)


write("header.svg", header())
write("footer.svg", footer())
for lang in ("es", "en"):
    sfx = "" if lang == "es" else "-en"
    write(f"workspace{sfx}.svg", workspace(lang))
    write(f"focus{sfx}.svg", focus(lang))
    for state in ("on", "off"):
        write(f"btn-{lang}-{state}.svg", button({"es": "ES · Español", "en": "EN · English"}[lang], state == "on"))
print("ok")
