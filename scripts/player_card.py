"""Genera la tarjeta de jugador (estadísticas reales de GitHub) en estilo RPG retro.

Uso: python player_card.py <carpeta_assets> <fuente.woff2> [usuario]
Con GH_TOKEN usa la API GraphQL (contribuciones, commits, racha); sin token usa la API REST pública.
Salida: player-card.svg (es) y player-card-en.svg (en).
"""
import ast
import base64
import datetime as dt
import json
import math
import os
import sys
import urllib.request
from html import escape

OUT, FONT = sys.argv[1], sys.argv[2]
LOGIN = sys.argv[3] if len(sys.argv) > 3 else "Jeremysa1"
TOKEN = os.environ.get("GH_TOKEN", "")
HERE = os.path.dirname(os.path.abspath(__file__))


def api(url, body=None):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "player-card"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def graphql(query, variables):
    res = api("https://api.github.com/graphql", {"query": query, "variables": variables})
    if "errors" in res:
        raise RuntimeError(res["errors"])
    return res["data"]


Q_MAIN = """query($login: String!) { user(login: $login) {
  createdAt followers { totalCount } pullRequests { totalCount }
  repositories(ownerAffiliations: OWNER, privacy: PUBLIC, isFork: false, first: 100) {
    totalCount nodes { stargazerCount languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name color } } } } }
  contributionsCollection { contributionYears totalCommitContributions
    contributionCalendar { weeks { contributionDays { date contributionCount } } } } } }"""


def collect():
    s = {"commits": None, "streak": None, "best": None, "xp": None}
    langs = {}
    if TOKEN:
        u = graphql(Q_MAIN, {"login": LOGIN})["user"]
        repos = u["repositories"]["nodes"]
        s["repos"] = u["repositories"]["totalCount"]
        s["stars"] = sum(r["stargazerCount"] for r in repos)
        s["prs"] = u["pullRequests"]["totalCount"]
        cc = u["contributionsCollection"]
        s["commits"] = cc["totalCommitContributions"]
        for r in repos:
            for e in r["languages"]["edges"]:
                n = e["node"]["name"]
                langs.setdefault(n, [0, e["node"]["color"] or "#8B949E"])[0] += e["size"]
        days = [d for w in cc["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
        best = cur = 0
        for d in days:
            cur = cur + 1 if d["contributionCount"] else 0
            best = max(best, cur)
        streak = 0
        for i, d in enumerate(reversed(days)):
            if d["contributionCount"]:
                streak += 1
            elif i > 0:  # hoy puede no tener contribuciones todavía
                break
        s["streak"], s["best"] = streak, best
        # XP = contribuciones de todos los años
        years = cc["contributionYears"]
        parts = " ".join(
            f'y{y}: contributionsCollection(from: "{y}-01-01T00:00:00Z", to: "{y}-12-31T23:59:59Z") {{ contributionCalendar {{ totalContributions }} }}'
            for y in years)
        yu = graphql(f"query($login: String!) {{ user(login: $login) {{ {parts} }} }}", {"login": LOGIN})["user"]
        s["xp"] = sum(v["contributionCalendar"]["totalContributions"] for v in yu.values())
    else:
        repos = [r for r in api(f"https://api.github.com/users/{LOGIN}/repos?per_page=100&type=owner") if not r["fork"]]
        s["repos"] = len(repos)
        s["stars"] = sum(r["stargazers_count"] for r in repos)
        s["prs"] = api(f"https://api.github.com/search/issues?q=author:{LOGIN}+type:pr")["total_count"]
        for r in repos:
            for n, b in api(r["languages_url"]).items():
                langs.setdefault(n, [0, "#8B949E"])[0] += b
    total = sum(v[0] for v in langs.values()) or 1
    top = sorted(langs.items(), key=lambda kv: -kv[1][0])[:4]
    s["langs"] = [(n, v[1], v[0] / total) for n, v in top]
    return s


# ---------- avatar: la misma cabeza pixel de la escena ----------
def load_head():
    tree = ast.parse(open(os.path.join(HERE, "gen_scene.py"), encoding="utf-8").read())
    found = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id in ("HEAD", "PAL"):
            found[node.targets[0].id] = ast.literal_eval(node.value)
    return found["HEAD"], found["PAL"]


def avatar(x0, y0, p):
    head, pal = load_head()
    px = {}
    c = 14
    for y, half in enumerate(head):
        n = len(half)
        for i, ch in enumerate(half):
            if ch != ".":
                px[(c - n + i, y)] = ch
                px[(c + n - 1 - i, y)] = ch
    for (x, y) in list(px):
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if (nx, ny) not in px:
                px.setdefault((nx, ny), "K")
    return "".join(f'<rect x="{x0 + x * p}" y="{y0 + y * p}" width="{p}" height="{p}" fill="{pal[ch]}"/>' for (x, y), ch in px.items())


TXT = {
    "es": {"class": "INGENIERO BACKEND", "stats": "Estadísticas", "skills": "Habilidades",
           "rows": [("COMMITS 12M", "commits", 1000), ("PULL REQUESTS", "prs", 100), ("REPOS", "repos", 30),
                    ("ESTRELLAS", "stars", 50), ("RACHA", "streak", 60), ("MEJOR RACHA", "best", 100)],
           "updated": "Actualizado", "daily": "se renueva cada día", "aria": "Tarjeta de jugador de Jeremy con sus estadísticas de GitHub"},
    "en": {"class": "BACKEND ENGINEER", "stats": "Stats", "skills": "Skills",
           "rows": [("COMMITS 12M", "commits", 1000), ("PULL REQUESTS", "prs", 100), ("REPOS", "repos", 30),
                    ("STARS", "stars", 50), ("STREAK", "streak", 60), ("BEST STREAK", "best", 100)],
           "updated": "Updated", "daily": "refreshes daily", "aria": "Jeremy's player card with GitHub stats"},
}


def seg_bar(x, y, frac, color, n=10, w=12, h=8, gap=2):
    out = []
    lit = round(max(0.0, min(1.0, frac)) * n)
    for k in range(n):
        out.append(f'<rect x="{x + k * (w + gap)}" y="{y}" width="{w}" height="{h}" fill="{color if k < lit else "#1E2150"}"/>')
    return "".join(out)


def log_frac(v, cap):
    return math.log10(v + 1) / math.log10(cap + 1) if v else 0.0


def render(s, lang):
    t = TXT[lang]
    W, H = 854, 300
    font = base64.b64encode(open(FONT, "rb").read()).decode()
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" shape-rendering="crispEdges" role="img" aria-label="{escape(t["aria"])}">',
           f'<title>PLAYER 1 · {LOGIN}</title>',
           '<style>@font-face { font-family: "PS2P"; src: url(data:font/woff2;base64,' + font + ') format("woff2"); }'
           ' text { font-family: "PS2P", ui-monospace, monospace; }'
           '.blink { animation: bl 1.1s steps(1, end) infinite; } @keyframes bl { 0%, 55% { opacity: 1; } 56%, 100% { opacity: 0; } }'
           '.xp { animation: xp 2.2s steps(1, end) infinite; } @keyframes xp { 0%, 50% { fill: #00D4FF; } 51%, 100% { fill: #B9F3FF; } }'
           '@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }</style>']
    out.append(f'<rect x="6" y="0" width="{W - 12}" height="{H}" fill="#7F5AF0"/><rect x="0" y="6" width="{W}" height="{H - 12}" fill="#7F5AF0"/>'
               f'<rect x="6" y="6" width="{W - 12}" height="{H - 12}" fill="#0F1328"/>'
               f'<rect x="10" y="10" width="{W - 20}" height="{H - 20}" fill="none" stroke="#3E2F86" stroke-width="2"/>'
               f'<rect x="12" y="12" width="{W - 24}" height="36" fill="#1B1F3B"/>'
               f'<text x="28" y="38" font-size="14" fill="#FFE45C">PLAYER 1</text>'
               f'<text x="{W - 28}" y="38" font-size="12" fill="#00D4FF" text-anchor="end">@{escape(LOGIN.upper())}</text>')
    # avatar y clase
    out.append('<rect x="28" y="62" width="200" height="164" fill="#161B3A"/><rect x="28" y="62" width="200" height="164" fill="none" stroke="#3E2F86" stroke-width="2"/>')
    out.append(avatar(64, 72, 4))
    out.append(f'<text x="128" y="250" font-size="10" fill="#F4F1FF" text-anchor="middle">{escape(LOGIN.upper())}</text>'
               f'<text x="128" y="270" font-size="8" fill="#7F8CC4" text-anchor="middle">{escape(t["class"])}</text>')
    # nivel y XP
    xp = s["xp"] if s["xp"] is not None else 0
    lvl = int(math.sqrt(xp / 5)) + 1
    lo, hi = 5 * (lvl - 1) ** 2, 5 * lvl ** 2
    out.append(f'<text x="252" y="84" font-size="20" fill="#FFE45C">LVL {lvl}</text>')
    out.append(f'<rect x="252" y="96" width="290" height="16" fill="#7F5AF0"/><rect x="255" y="99" width="284" height="10" fill="#1E2150"/>'
               f'<rect class="xp" x="255" y="99" width="{int(284 * (xp - lo) / max(1, hi - lo))}" height="10"/>'
               f'<text x="252" y="130" font-size="8" fill="#B9F3FF">XP {xp} / {hi}</text>')
    # estadísticas
    out.append(f'<text x="252" y="156" font-size="9" fill="#8B949E">{escape(t["stats"])}</text>')
    for k, (label, key, cap) in enumerate(t["rows"]):
        y = 176 + k * 18
        v = s.get(key)
        out.append(f'<text x="252" y="{y}" font-size="8" fill="#E6EDF3">{escape(label)}</text>'
                   f'<text x="440" y="{y}" font-size="8" fill="#FFE45C" text-anchor="end">{"--" if v is None else v}</text>'
                   + seg_bar(452, y - 8, log_frac(v or 0, cap), "#3CCB6E" if key in ("streak", "best") else "#7F5AF0", n=6, w=12, h=8))
    # habilidades = lenguajes más usados en sus repos públicos
    out.append(f'<text x="584" y="84" font-size="9" fill="#8B949E">{escape(t["skills"])}</text>')
    for k, (name, color, frac) in enumerate(s["langs"]):
        y = 112 + k * 40
        out.append(f'<rect x="584" y="{y - 10}" width="10" height="10" fill="{color}"/>'
                   f'<text x="602" y="{y}" font-size="9" fill="#E6EDF3">{escape(name)}</text>'
                   f'<text x="826" y="{y}" font-size="8" fill="#B9F3FF" text-anchor="end">{round(frac * 100)}%</text>'
                   + seg_bar(584, y + 8, frac, color, n=12, w=16, h=8, gap=4))
    today = dt.date.today().isoformat()
    foot = f'{t["updated"]} {today} · {t["daily"]}'
    out.append(f'<text x="826" y="{H - 24}" font-size="7" fill="#5A6382" text-anchor="end">{escape(foot)}</text>'
               f'<rect class="blink" x="{826 - len(foot) * 7 - 16}" y="{H - 32}" width="8" height="8" fill="#3CCB6E"/>')
    out.append('</svg>')
    return "".join(out)


stats = collect()
for lang, name in (("es", "player-card.svg"), ("en", "player-card-en.svg")):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
        fh.write(render(stats, lang))
print(json.dumps({k: v for k, v in stats.items() if k != "langs"}), [l[0] for l in stats["langs"]])
