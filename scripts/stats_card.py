"""Genera la tarjeta de estadísticas de GitHub del perfil, en estilo sobrio.

Uso: python stats_card.py <carpeta_assets> [usuario]
Con GH_TOKEN usa la API GraphQL (contribuciones, commits, racha); sin token usa la API REST pública.
Salida: stats.svg (es) y stats-en.svg (en).
"""
import datetime as dt
import json
import os
import sys
import urllib.request
from html import escape

OUT = sys.argv[1]
LOGIN = sys.argv[2] if len(sys.argv) > 2 else "Jeremysa1"
TOKEN = os.environ.get("GH_TOKEN", "")
BG, PANEL, LINE, INK, MUTED = "#0D1117", "#161B22", "#30363D", "#E6EDF3", "#8B949E"
CYAN = "#00D4FF"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"


def api(url, body=None):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "stats-card"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    data = json.dumps(body).encode() if body is not None else None
    with urllib.request.urlopen(urllib.request.Request(url, data=data, headers=headers), timeout=30) as r:
        return json.load(r)


def graphql(query, variables):
    res = api("https://api.github.com/graphql", {"query": query, "variables": variables})
    if "errors" in res:
        raise RuntimeError(res["errors"])
    return res["data"]


Q_MAIN = """query($login: String!) { user(login: $login) {
  pullRequests { totalCount }
  repositories(ownerAffiliations: OWNER, privacy: PUBLIC, isFork: false, first: 100) {
    totalCount nodes { stargazerCount languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name color } } } } }
  contributionsCollection { contributionYears totalCommitContributions
    contributionCalendar { weeks { contributionDays { contributionCount } } } } } }"""


def collect():
    s = {"commits": None, "streak": None, "total": None}
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
                langs.setdefault(e["node"]["name"], [0, e["node"]["color"] or MUTED])[0] += e["size"]
        days = [d["contributionCount"] for w in cc["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
        streak = 0
        for i, n in enumerate(reversed(days)):
            if n:
                streak += 1
            elif i > 0:  # hoy puede no tener contribuciones todavía
                break
        s["streak"] = streak
        parts = " ".join(
            f'y{y}: contributionsCollection(from: "{y}-01-01T00:00:00Z", to: "{y}-12-31T23:59:59Z") {{ contributionCalendar {{ totalContributions }} }}'
            for y in cc["contributionYears"])
        yu = graphql(f"query($login: String!) {{ user(login: $login) {{ {parts} }} }}", {"login": LOGIN})["user"]
        s["total"] = sum(v["contributionCalendar"]["totalContributions"] for v in yu.values())
    else:
        repos = [r for r in api(f"https://api.github.com/users/{LOGIN}/repos?per_page=100&type=owner") if not r["fork"]]
        s["repos"] = len(repos)
        s["stars"] = sum(r["stargazers_count"] for r in repos)
        s["prs"] = api(f"https://api.github.com/search/issues?q=author:{LOGIN}+type:pr")["total_count"]
        for r in repos:
            for n, b in api(r["languages_url"]).items():
                langs.setdefault(n, [0, MUTED])[0] += b
    total = sum(v[0] for v in langs.values()) or 1
    top = sorted(langs.items(), key=lambda kv: -kv[1][0])[:4]
    s["langs"] = [(n, v[1], v[0] / total) for n, v in top]
    return s


TXT = {
    "es": {"tiles": [("commits", "Commits (12 meses)"), ("total", "Contribuciones"), ("prs", "Pull requests"),
                     ("repos", "Repos públicos"), ("stars", "Estrellas"), ("streak", "Racha actual (días)")],
           "langs": "LENGUAJES", "other": "Otros", "updated": "Actualizado", "aria": "Estadísticas de GitHub de Jeremy"},
    "en": {"tiles": [("commits", "Commits (12 months)"), ("total", "Contributions"), ("prs", "Pull requests"),
                     ("repos", "Public repos"), ("stars", "Stars"), ("streak", "Current streak (days)")],
           "langs": "LANGUAGES", "other": "Other", "updated": "Updated", "aria": "Jeremy's GitHub stats"},
}


def render(s, lang):
    t = TXT[lang]
    W, H = 854, 262
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(t["aria"])}">',
           f'<title>{escape(t["aria"])}</title><style>text {{ font-family: {SANS}; }}</style>',
           f'<rect width="{W}" height="{H}" rx="14" fill="{PANEL}"/><rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="none" stroke="{LINE}"/>',
           f'<text x="28" y="40" font-size="12" font-weight="600" letter-spacing="2" fill="{CYAN}">GITHUB  ·  @{escape(LOGIN.upper())}</text>']
    for i, (key, label) in enumerate(t["tiles"]):
        x, y = 28 + (i % 3) * 172, 60 + (i // 3) * 86
        v = s.get(key)
        out.append(f'<rect x="{x}" y="{y}" width="160" height="74" rx="10" fill="{BG}" stroke="{LINE}"/>'
                   f'<text x="{x + 16}" y="{y + 36}" font-size="24" font-weight="700" fill="{INK}">{"–" if v is None else v}</text>'
                   f'<text x="{x + 16}" y="{y + 58}" font-size="12" fill="{MUTED}">{escape(label)}</text>')
    # lenguajes: barra apilada + leyenda
    lx, lw = 560, 266
    out.append(f'<text x="{lx}" y="78" font-size="12" font-weight="600" letter-spacing="2" fill="{MUTED}">{t["langs"]}</text>'
               f'<clipPath id="bar"><rect x="{lx}" y="92" width="{lw}" height="10" rx="5"/></clipPath>'
               f'<rect x="{lx}" y="92" width="{lw}" height="10" rx="5" fill="{LINE}"/><g clip-path="url(#bar)">')
    x = lx
    for name, color, frac in s["langs"]:
        out.append(f'<rect x="{x:.1f}" y="92" width="{max(frac * lw - 2, 0):.1f}" height="10" fill="{color}"/>')
        x += frac * lw
    out.append('</g>')
    rows = s["langs"]
    rest = 1 - sum(f for _, _, f in rows)
    if rest > 0.005:
        rows = rows + [(t["other"], LINE, rest)]
    for i, (name, color, frac) in enumerate(rows):
        y = 130 + i * 22
        out.append(f'<circle cx="{lx + 5}" cy="{y - 4}" r="5" fill="{color}"/>'
                   f'<text x="{lx + 18}" y="{y}" font-size="13" fill="{INK}">{escape(name)}</text>'
                   f'<text x="{lx + lw}" y="{y}" font-size="13" fill="{MUTED}" text-anchor="end">{frac * 100:.1f}%</text>')
    out.append(f'<text x="{W - 28}" y="{H - 14}" font-size="11" fill="#6E7681" text-anchor="end">{t["updated"]} {dt.date.today().isoformat()}</text></svg>')
    return "".join(out)


stats = collect()
for lang, name in (("es", "stats.svg"), ("en", "stats-en.svg")):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
        fh.write(render(stats, lang))
print({k: v for k, v in stats.items() if k != "langs"}, [l[0] for l in stats["langs"]])
