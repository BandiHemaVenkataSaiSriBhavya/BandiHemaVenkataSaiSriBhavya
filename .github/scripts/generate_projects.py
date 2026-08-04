#!/usr/bin/env python3
"""
Generate an animated, monochromatic pink theme-matched projects and languages panel.
"""
import json, base64, os, sys, math, html
from datetime import datetime, timezone

# ---------------- STRICT PINK/MAGENTA THEMES ----------------
THEMES = {
    "dark": {
        "BG": "#0A0A0A", "PANEL": "#120A16", "PANEL_BAR": "#180A22",
        "PRIMARY": "#EC4899",   # Hot Pink (Replaces Cyan/Green)
        "SECONDARY": "#D946EF", # Fuchsia
        "TERTIARY": "#BE185D",  # Dark Magenta
        "TEXT": "#FDF2F8", "MUTED": "#F472B6",
        "DIM": "#9D174D",
        "STROKE": "rgba(236,72,153,0.3)", "STROKE_HI": "rgba(236,72,153,0.6)",
        "STROKE_LO": "rgba(236,72,153,0.15)", "BARLINE": "rgba(236,72,153,0.15)",
        "RING_BG": "rgba(236,72,153,0.15)", "PILL_BG": "rgba(217,70,239,0.15)",
        "PILL_STROKE": "rgba(217,70,239,0.4)", "MONO_TX": "#FFFFFF",
    },
    "light": {
        "BG": "#FFFFFF", "PANEL": "#FFFFFF", "PANEL_BAR": "#FDF2F8",
        "PRIMARY": "#BE185D",   # Dark Magenta
        "SECONDARY": "#9D174D", # Deep Pink
        "TERTIARY": "#831843",  # Burgundy
        "TEXT": "#4A0023", "MUTED": "#9D174D",
        "DIM": "#F472B6",
        "STROKE": "rgba(157,23,77,0.3)", "STROKE_HI": "rgba(157,23,77,0.6)",
        "STROKE_LO": "rgba(157,23,77,0.15)", "BARLINE": "rgba(157,23,77,0.15)",
        "RING_BG": "rgba(157,23,77,0.1)", "PILL_BG": "rgba(157,23,77,0.05)",
        "PILL_STROKE": "rgba(157,23,77,0.3)", "MONO_TX": "#FFFFFF",
    },
}

BG = PANEL = PANEL_BAR = PRIMARY = SECONDARY = TERTIARY = TEXT = MUTED = DIM = None
STROKE = STROKE_HI = STROKE_LO = BARLINE = RING_BG = PILL_BG = PILL_STROKE = MONO_TX = None
DONUT_COLORS = []

def set_theme(name):
    t = THEMES[name]
    g = globals()
    for k, v in t.items():
        g[k] = v
    # Strict monochromatic pink scale for donuts
    g["DONUT_COLORS"] = [t["PRIMARY"], t["SECONDARY"], t["TERTIARY"], "#F472B6", "#9D174D"]

set_theme("dark")

W        = 1180
CARD_W   = 578
CARD_H   = 168
GAP      = 14
MARGIN   = 5
FONT     = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

def esc(s): return html.escape(str(s), quote=True)

def rel_time(iso):
    if not iso: return "n/a"
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        d = (datetime.now(timezone.utc) - dt)
        if d.days > 365: return f"{d.days//365}y ago"
        if d.days > 30:  return f"{d.days//30}mo ago"
        if d.days > 0:   return f"{d.days}d ago"
        h = d.seconds // 3600
        return f"{h}h ago" if h else "just now"
    except Exception:
        return "n/a"

def load_logo_b64(path):
    if not path: return None
    for base in ("logos", "."):
        p = os.path.join(base, path)
        if os.path.exists(p):
            ext = os.path.splitext(p)[1].lower()
            mime = {"png":"image/png","svg":"image/svg+xml","jpg":"image/jpeg",
                    "jpeg":"image/jpeg","webp":"image/webp"}.get(ext[1:], "image/png")
            with open(p, "rb") as f:
                return f"data:{mime};base64," + base64.b64encode(f.read()).decode()
    return None

def wrap_text(s, max_chars, max_lines=2):
    words = s.split()
    lines, cur = [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= max_chars:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur); cur = w
            if len(lines) == max_lines: break
    if cur and len(lines) < max_lines: lines.append(cur)
    if len(lines) == max_lines and words and " ".join(lines).count(" ") + 1 < len(words):
        lines[-1] = lines[-1][:max_chars-1].rstrip() + "…"
    return lines

def donut_segments(languages, cx, cy, r, begin):
    total = sum(languages.values()) or 1
    entries = sorted(languages.items(), key=lambda kv: -kv[1])[:4]
    other = total - sum(v for _, v in entries)
    if other > 0: entries.append(("Other", other))
    C = 2 * math.pi * r
    out, legend = [], []
    offset = 0.0
    t = begin
    for i, (lang, v) in enumerate(entries):
        frac = v / total
        seg = frac * C
        col = DONUT_COLORS[i % len(DONUT_COLORS)]
        out.append(
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-width="9" '
            f'stroke-dasharray="{seg:.2f} {C - seg:.2f}" stroke-dashoffset="{-offset:.2f}" '
            f'transform="rotate(-90 {cx} {cy})" opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" dur="0.01s" begin="{t:.2f}s" fill="freeze"/>'
            f'<animate attributeName="stroke-dasharray" from="0 {C:.2f}" to="{seg:.2f} {C - seg:.2f}" '
            f'dur="0.6s" begin="{t:.2f}s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines="0.3 0 0.2 1"/>'
            f'</circle>')
        legend.append((lang, frac, col))
        offset += seg
        t += 0.18
    return "".join(out), legend

def card(p, x, y, idx):
    b = 0.25 + idx * 0.15
    e = []
    a = e.append
    repo = p.get("repo", "").strip()
    repo = repo.replace("https://github.com/", "").replace("http://github.com/", "")
    repo = repo.rstrip("/")
    href = f"https://github.com/{esc(repo)}"
    a(f'<a href="{href}" target="_blank">')
    a(f'<g opacity="0" transform="translate({x},{y})">')
    a(f'<animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="{b:.2f}s" fill="freeze"/>')

    a(f'<rect width="{CARD_W}" height="{CARD_H}" rx="12" fill="{PANEL}" stroke="{STROKE}">'
      f'<animate attributeName="stroke" values="{STROKE_LO};{STROKE_HI};{STROKE_LO}" '
      f'dur="4.5s" begin="{b+idx*0.7:.2f}s" repeatCount="indefinite"/></rect>')
    a(f'<rect width="{CARD_W}" height="30" rx="12" fill="{PANEL_BAR}"/>')
    a(f'<rect y="18" width="{CARD_W}" height="12" fill="{PANEL_BAR}"/>')
    a(f'<line x1="0" y1="30" x2="{CARD_W}" y2="30" stroke="{BARLINE}"/>')
    a(f'<text x="16" y="19" font-size="10" fill="{MUTED}"><tspan fill="{PRIMARY}">&#8226;</tspan> {esc(repo)}</text>')

    days = 999
    try:
        dt = datetime.fromisoformat(p.get("pushed_at", "").replace("Z", "+00:00"))
        days = (datetime.now(timezone.utc) - dt).days
    except Exception:
        pass
    if days <= 14:
        a(f'<circle cx="{CARD_W-16}" cy="15" r="3.5" fill="{PRIMARY}">'
          f'<animate attributeName="opacity" values="1;0.25;1" dur="1.8s" repeatCount="indefinite"/></circle>')
    else:
        a(f'<circle cx="{CARD_W-16}" cy="15" r="3.5" fill="{DIM}"/>')

    logo = p.get("_logo_b64")
    float_anim = (f'<animateTransform attributeName="transform" type="translate" '
                  f'values="0 0; 0 -2.5; 0 0" dur="5s" begin="{b+idx*0.5:.2f}s" '
                  f'repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" '
                  f'keySplines="0.4 0 0.6 1;0.4 0 0.6 1"/>')
    if logo:
        a(f'<g>{float_anim}<image x="16" y="44" width="40" height="40" href="{logo}" preserveAspectRatio="xMidYMid meet"/></g>')
    else:
        initial = esc((p.get("name") or "?")[0].upper())
        a(f'<g>{float_anim}<rect x="16" y="44" width="40" height="40" rx="20" fill="{SECONDARY}" opacity="0.9"/>'
          f'<text x="36" y="71" text-anchor="middle" font-size="20" font-weight="700" fill="{MONO_TX}">{initial}</text></g>')

    name = esc(p.get("name", "unnamed"))
    a(f'<text x="68" y="61" font-size="17" font-weight="700" fill="{TEXT}">{name}'
      f'<tspan fill="{PRIMARY}">_<animate attributeName="opacity" values="1;0;1" dur="1.2s" '
      f'begin="{b+0.4:.2f}s" repeatCount="indefinite"/></tspan></text>')

    for i, line in enumerate(wrap_text(p.get("description", ""), 52)):
        a(f'<text x="68" y="{80 + i * 16}" font-size="11" fill="{MUTED}">{esc(line)}</text>')

    tx = 68
    for tag in (p.get("tags") or [])[:3]:
        tw = len(tag) * 6.6 + 14
        a(f'<rect x="{tx}" y="118" width="{tw:.0f}" height="17" rx="8.5" fill="{PILL_BG}" stroke="{PILL_STROKE}"/>')
        a(f'<text x="{tx + tw/2:.0f}" y="130" text-anchor="middle" font-size="9.5" fill="{PRIMARY}">{esc(tag)}</text>')
        tx += tw + 7

    stars = p.get("stars", 0)
    a(f'<text x="68" y="155" font-size="11" fill="{MUTED}">'
      f'<tspan fill="{PRIMARY}">&#9733;</tspan> {stars}'
      f'<tspan fill="{DIM}" dx="14">updated {rel_time(p.get("pushed_at"))}</tspan></text>')

    langs = p.get("languages") or {}
    if langs:
        cx, cy, r = CARD_W - 58, CARD_H // 2 + 6, 27
        segs, legend = donut_segments(langs, cx, cy, r, b + 0.3)
        a(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{RING_BG}" stroke-width="9"/>')
        a(segs)
        top = legend[0]
        a(f'<text x="{cx}" y="{cy+4}" text-anchor="middle" font-size="11" font-weight="700" fill="{TEXT}">{top[1]*100:.0f}%</text>')
        dot_x = cx - r - 92
        text_x = dot_x + 9
        ly = cy - 22
        for lang, frac, col in legend[:3]:
            a(f'<circle cx="{dot_x}" cy="{ly}" r="3.5" fill="{col}"/>')
            a(f'<text x="{text_x}" y="{ly+4}" font-size="10" fill="{MUTED}">{esc(lang)} {frac*100:.0f}%</text>')
            ly += 18
    a('</g>')
    a('</a>')
    return "".join(e)

def build_projects(projects, theme="dark"):
    rows = math.ceil(len(projects) / 2)
    H = 56 + rows * (CARD_H + GAP) + MARGIN
    gid = f"acc_{theme}"
    s = []
    a = s.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
      f'font-family="{FONT}" role="img" aria-label="Projects">')
    a(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    a(f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0">'
      f'<stop offset="0" stop-color="{PRIMARY}"><animate attributeName="stop-color" values="{PRIMARY};{SECONDARY};{TERTIARY};{PRIMARY}" dur="10s" repeatCount="indefinite"/></stop>'
      f'<stop offset="1" stop-color="{SECONDARY}"><animate attributeName="stop-color" values="{SECONDARY};{PRIMARY};{TERTIARY};{SECONDARY}" dur="10s" repeatCount="indefinite"/></stop>'
      '</linearGradient></defs>')
    a(f'<text x="{MARGIN+2}" y="18" font-size="11" letter-spacing="2" fill="{PRIMARY}">PROJECTS.LIST</text>')
    a(f'<text x="{MARGIN+130}" y="18" font-size="10" fill="{DIM}">./projects.sh --all</text>')
    a(f'<line x1="{MARGIN}" y1="28" x2="{W-MARGIN}" y2="28" stroke="url(#{gid})" stroke-width="1.5" opacity="0.7"/>')
    for i, p in enumerate(projects):
        x = MARGIN + (i % 2) * (CARD_W + GAP + 4)
        y = 42 + (i // 2) * (CARD_H + GAP)
        a(card(p, x, y, i))
    a('</svg>')
    return "".join(s)

def build_languages(projects, theme="dark"):
    agg = {}
    for p in projects:
        for lang, count in (p.get("languages") or {}).items():
            agg[lang] = agg.get(lang, 0) + count

    total_bytes = sum(agg.values()) or 1
    sorted_langs = sorted(agg.items(), key=lambda x: -x[1])[:8]
    
    num_langs = len(sorted_langs)
    H = 130 + (num_langs * 32)
    gid = f"acc_lang_{theme}"
    
    s = []
    a = s.append

    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
      f'font-family="{FONT}" role="img" aria-label="Most Used Languages">')
    
    a(f'<rect width="{W-10}" x="5" y="5" height="{H-10}" rx="12" fill="{PANEL}" stroke="{STROKE}"/>')
    
    a(f'<defs>'
      f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0">'
      f'<stop offset="0" stop-color="{PRIMARY}"><animate attributeName="stop-color" values="{PRIMARY};{SECONDARY};{TERTIARY};{PRIMARY}" dur="8s" repeatCount="indefinite"/></stop>'
      f'<stop offset="1" stop-color="{SECONDARY}"><animate attributeName="stop-color" values="{SECONDARY};{TERTIARY};{PRIMARY};{SECONDARY}" dur="8s" repeatCount="indefinite"/></stop>'
      f'</linearGradient>'
      f'<filter id="glowPink" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="3" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
      f'</defs>')

    a(f'<rect x="5" y="5" width="{W-10}" height="40" rx="12" fill="{PANEL_BAR}"/>')
    a(f'<rect x="5" y="25" width="{W-10}" height="20" fill="{PANEL_BAR}"/>')
    a(f'<circle cx="25" cy="25" r="5.5" fill="#ff5f56"/>')
    a(f'<circle cx="45" cy="25" r="5.5" fill="#ffbd2e"/>')
    a(f'<circle cx="65" cy="25" r="5.5" fill="#27c93f"/>')
    a(f'<text x="{W/2}" y="30" text-anchor="middle" font-size="12" fill="{MUTED}">./languages.sh</text>')
    a(f'<line x1="5" y1="45" x2="{W-5}" y2="45" stroke="{BARLINE}" stroke-width="1.5"/>')

    a(f'<text x="35" y="85" font-size="14" font-weight="700" fill="{PRIMARY}">❯ ./LANGUAGES.SH</text>')
    
    y_offset = 120
    max_bar_width = 800
    
    for i, (lang, count) in enumerate(sorted_langs):
        pct = (count / total_bytes) * 100
        bar_w = max(8, (pct / 100) * max_bar_width) 
        
        # EVERY language now gets the exact same unified pink dot
        a(f'<circle cx="40" cy="{y_offset + 7}" r="4" fill="{PRIMARY}" filter="url(#glowPink)"/>')
        
        # Language Label
        a(f'<text x="55" y="{y_offset + 11}" font-size="13" font-weight="bold" fill="{TEXT}">{esc(lang)}</text>')
        
        # Background Track
        a(f'<rect x="180" y="{y_offset}" width="{max_bar_width}" height="12" rx="6" fill="{RING_BG}"/>')
        
        # ALL bars use the exact same primary pink/magenta glow
        delay = i * 0.15
        a(f'<rect x="180" y="{y_offset}" width="0" height="12" rx="6" fill="url(#{gid})" filter="url(#glowPink)">')
        a(f'<animate attributeName="width" from="0" to="{bar_w:.1f}" dur="1.2s" begin="{delay}s" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1" keyTimes="0;1"/>')
        a(f'</rect>')
        
        # Percentage
        a(f'<text x="{180 + max_bar_width + 25}" y="{y_offset + 11}" font-size="13" font-weight="bold" fill="{MUTED}">{pct:.1f}%</text>')
        
        y_offset += 32

    a('</svg>')
    return "".join(s)

if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "merged.json"
    outdir = sys.argv[2] if len(sys.argv) > 2 else "."
    with open(src) as f:
        projects = json.load(f)
    for p in projects:
        p["_logo_b64"] = load_logo_b64(p.get("logo"))
    
    targets = (
        ("dark", "projects.svg"),
        ("light", "projects-light.svg"),
        ("dark", "languages.svg"),
        ("light", "languages-light.svg"),
    )

    for theme, fname in targets:
        set_theme(theme)
        if fname.startswith("languages"):
            svg = build_languages(projects, theme)
        else:
            svg = build_projects(projects, theme)
            
        path = os.path.join(outdir, fname)
        with open(path, "w") as f:
            f.write(svg)
        print(f"wrote {path}: {theme}, {len(svg)//1024}KB")
