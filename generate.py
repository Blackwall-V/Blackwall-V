#!/usr/bin/env python3
"""Generate two premium RETRO animated SVGs (dark.svg, light.svg) for the
Blackwall-V GitHub profile. Pure SVG + SMIL only — no CSS, no HTML, no script.
Aesthetic: CRT terminal, block ASCII, scanlines, amber/green phosphor glow."""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ROOT, "assets")
os.makedirs(ASSETS, exist_ok=True)

ASCII = [
    "██████╗ ██╗      █████╗  ██████╗██╗  ██╗██╗    ██╗ █████╗ ██╗     ██╗         ██╗   ██╗",
    "██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝██║    ██║██╔══██╗██║     ██║         ██║   ██║",
    "██████╔╝██║     ███████║██║     █████╔╝ ██║ █╗ ██║███████║██║     ██║         ██║   ██║",
    "██╔══██╗██║     ██╔══██║██║     ██╔═██╗ ██║███╗██║██╔══██║██║     ██║         ╚██╗ ██╔╝",
    "██████╔╝███████╗██║  ██║╚██████╗██║  ██╗╚███╔███╔╝██║  ██║███████╗███████╗     ╚████╔╝",
    "╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ ╚██╝╚██╝ ╚═╝  ╚═╝╚══════╝╚══════╝      ╚═══╝",
]

DARK = dict(
    bg0="#0a0f08", bg1="#0d160c",
    panel="#08120a", panel_edge="rgba(60,200,90,0.30)",
    scan="rgba(80,255,120,0.05)",
    fg="#7dffb0", fg_dim="#3fbf7a",
    amber="#ffb454", amber_dim="#a86a1f",
    muted="#5a8f72",
    accent="#39ff14", accent2="#ffb454", accent3="#5fd0ff",
    glow="rgba(57,255,20,0.55)",
)
LIGHT = dict(
    bg0="#f4f1e6", bg1="#fbf8ee",
    panel="#1a2418", panel_edge="rgba(20,40,24,0.45)",
    scan="rgba(0,0,0,0.04)",
    fg="#0a3d1f", fg_dim="#1d6b3a",
    amber="#7a4d00", amber_dim="#a86a1f",
    muted="#4a6b58",
    accent="#0a7d28", accent2="#9a5b00", accent3="#1a5a8a",
    glow="rgba(10,125,40,0.30)",
)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build(p, tag):
    W, H = 940, 560
    cw, ch = 9.6, 22          # block chars are tall/wide
    ascii_w = max(len(l) for l in ASCII) * cw
    ascii_h = len(ASCII) * ch
    ax = 38
    ay = 96
    panel_x = 22
    panel_y = 50
    panel_w = ascii_w + 36
    panel_h = H - panel_y - 18  # tall panel reaching near bottom

    # ---- ASCII lines: per-line reveal + persistent phosphor glow pulse ----
    ascii_nodes = []
    for i, l in enumerate(ASCII):
        y = ay + i * ch + ch * 0.82
        content = esc(l) or " "
        begin = 0.2 + i * 0.13
        dur_glow = 3.6 + i * 0.5
        ascii_nodes.append(
            f'      <text x="{ax}" y="{y:.1f}" '
            f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
            f'font-size="16" font-weight="700" letter-spacing="1" '
            f'fill="{p["fg"]}" opacity="0">{content}'
            f'<animate attributeName="opacity" from="0" to="1" begin="{begin:.2f}s" '
            f'dur="0.5s" fill="freeze"/>'
            f'<animate attributeName="opacity" values="1;0.55;1" begin="3s" '
            f'dur="{dur_glow:.1f}s" repeatCount="indefinite"/>'
            f'</text>'
        )
    ascii_block = "\n".join(ascii_nodes)

    # ---- Typing effect via SMIL opacity cycling ----
    words = ["> data_scientist", "> ml_engineer", "> python_dev", "> open_source"]
    per = 2.6
    total = per * len(words)
    word_nodes = []
    ty = ay + ascii_h + 64
    tx = 56
    for i, w in enumerate(words):
        start = i * per
        a = start / total
        b = (start + 0.1) / total
        c = (start + per - 0.2) / total
        d = (start + per - 0.04) / total
        word_nodes.append(
            f'        <text x="{tx}" y="{ty}" '
            f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
            f'font-size="18" font-weight="700" fill="{p["accent"]}" opacity="0">{esc(w)}'
            f'<animate attributeName="opacity" '
            f'values="0;1;1;0;0" keyTimes="0;{a+0.0001:.4f};{c:.4f};{d:.4f};1" '
            f'dur="{total}s" repeatCount="indefinite"/></text>'
        )
    typing_block = "\n".join(word_nodes)

    # ---- tech tags as bracketed tokens ----
    tags = ["python", "pandas", "scikit-learn", "pycaret", "rust", "linux"]
    tx0 = 56
    ty0 = ty + 52
    tag_nodes = []
    cx = tx0
    for i, t in enumerate(tags):
        label = f"[{t}]"
        w = len(label) * 8.4 + 6
        tag_nodes.append(
            f'      <g opacity="0">'
            f'<text x="{cx}" y="{ty0}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
            f'font-size="13" font-weight="700" fill="{p["amber"]}">{label}</text>'
            f'<animate attributeName="opacity" from="0" to="1" begin="{2.4+i*0.12:.2f}s" dur="0.4s" fill="freeze"/>'
            f'</g>'
        )
        cx += w + 10
    tags_block = "\n".join(tag_nodes)

    # ---- scanlines: many thin rects forming a CRT overlay ----
    scanlines = []
    for y in range(0, H, 3):
        scanlines.append(f'<rect x="0" y="{y}" width="{W}" height="1" fill="{p["scan"]}"/>')
    scan_block = "\n".join(scanlines)

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"
     role="img" aria-label="Blackwall-V retro terminal banner ({tag} mode)">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{p["bg1"]}"/>
      <stop offset="0.5" stop-color="{p["bg0"]}"/>
      <stop offset="1" stop-color="{p["bg1"]}"/>
    </linearGradient>
    <linearGradient id="phosphor" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{p["accent"]}" stop-opacity="0.10"/>
      <stop offset="0.5" stop-color="{p["accent"]}" stop-opacity="0"/>
      <stop offset="1" stop-color="{p["accent"]}" stop-opacity="0.10"/>
    </linearGradient>
    <radialGradient id="vignette" cx="0.5" cy="0.5" r="0.75">
      <stop offset="0.55" stop-color="#000000" stop-opacity="0"/>
      <stop offset="1" stop-color="#000000" stop-opacity="{0.55 if tag=='dark' else 0.10}"/>
    </radialGradient>
    <filter id="bloom" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="6" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="soft" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="40"/>
    </filter>
  </defs>

  <!-- background -->
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect width="{W}" height="{H}" fill="url(#phosphor)"/>

  <!-- drifting phosphor glow blobs -->
  <g filter="url(#soft)" opacity="0.45">
    <circle cx="180" cy="260" r="120" fill="{p["accent"]}">
      <animate attributeName="cx" values="180;240;180" dur="18s" repeatCount="indefinite"/>
      <animate attributeName="cy" values="260;230;260" dur="14s" repeatCount="indefinite"/>
    </circle>
    <circle cx="780" cy="200" r="100" fill="{p["amber"]}" opacity="0.7">
      <animate attributeName="cx" values="780;720;780" dur="22s" repeatCount="indefinite"/>
    </circle>
    <circle cx="600" cy="420" r="90" fill="{p["accent3"]}" opacity="0.5">
      <animate attributeName="cy" values="420;390;420" dur="12s" repeatCount="indefinite"/>
    </circle>
  </g>

  <!-- CRT panel (dark glass terminal) -->
  <rect x="{panel_x}" y="{panel_y}" width="{panel_w:.0f}" height="{panel_h:.0f}" rx="10"
        fill="{p["panel"]}" stroke="{p["panel_edge"]}" stroke-width="1.5"/>
  <!-- terminal title bar -->
  <rect x="{panel_x}" y="{panel_y}" width="{panel_w:.0f}" height="26" rx="10" fill="#000000" opacity="0.55"/>
  <rect x="{panel_x}" y="{panel_y+20}" width="{panel_w:.0f}" height="6" fill="#000000" opacity="0.55"/>
  <circle cx="{panel_x+18}" cy="{panel_y+13}" r="5" fill="#ff5f57"/>
  <circle cx="{panel_x+36}" cy="{panel_y+13}" r="5" fill="#febc2e"/>
  <circle cx="{panel_x+54}" cy="{panel_y+13}" r="5" fill="#28c840"/>
  <text x="{panel_x+78}" y="{panel_y+18}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
        font-size="11" fill="{p["muted"]}">blackwall@localhost: ~</text>
  <!-- blinking REC dot -->
  <circle cx="{panel_x+panel_w-22:.0f}" cy="{panel_y+13}" r="4" fill="#ff3b30">
    <animate attributeName="opacity" values="1;0.2;1" dur="1.2s" repeatCount="indefinite"/>
  </circle>

  <!-- prompt line above ASCII -->
  <text x="{ax}" y="{ay-14}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
        font-size="13" font-weight="700" fill="{p["amber"]}">$ figlet Blackwall-V</text>
  <rect x="{ax+170}" y="{ay-26}" width="9" height="14" fill="{p["amber"]}">
    <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.49;0.5;1" dur="1s" repeatCount="indefinite"/>
  </rect>

  <!-- ASCII art with bloom -->
  <g filter="url(#bloom)">
{ascii_block}
  </g>

  <!-- divider -->
  <line x1="{ax}" y1="{ay+ascii_h+14:.0f}" x2="{panel_x+panel_w-20:.0f}" y2="{ay+ascii_h+14:.0f}"
        stroke="{p["accent"]}" stroke-width="1" opacity="0.5">
    <animate attributeName="opacity" values="0.2;0.7;0.2" dur="4s" repeatCount="indefinite"/>
  </line>

  <!-- prompt + typing -->
  <text x="38" y="{ty}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
        font-size="18" font-weight="700" fill="{p["amber"]}">$</text>
  <!-- typing cursor block -->
  <rect x="{tx-2}" y="{ty-16}" width="11" height="20" fill="{p["accent"]}" opacity="0">
    <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.05;0.95;1" dur="1.1s" repeatCount="indefinite"/>
  </rect>
{typing_block}

  <!-- tags -->
  <text x="38" y="{ty0-18}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
        font-size="13" font-weight="700" fill="{p["muted"]}">$ ls ./stack</text>
{tags_block}

  <!-- status bar -->
  <rect x="{panel_x}" y="{H-40}" width="{panel_w:.0f}" height="26" rx="0" fill="#000000" opacity="0.5"/>
  <rect x="{panel_x}" y="{H-40}" width="{panel_w:.0f}" height="26" fill="none" stroke="{p["panel_edge"]}" stroke-width="1"/>
  <circle cx="{panel_x+18}" cy="{H-27}" r="4" fill="#28c840">
    <animate attributeName="opacity" values="1;0.3;1" dur="1.6s" repeatCount="indefinite"/>
  </circle>
  <text x="{panel_x+32}" y="{H-23}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
        font-size="11" fill="{p["accent"]}">online</text>
  <text x="{panel_x+90}" y="{H-23}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
        font-size="11" fill="{p["muted"]}">| branch: main | utf-8 | RETRO-OS v1.0</text>
  <text x="{panel_x+panel_w-18:.0f}" y="{H-23}" text-anchor="end"
        font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
        font-size="11" fill="{p["amber"]}">github.com/Blackwall-V</text>

  <!-- scanlines overlay -->
  <g opacity="0.9">
{scan_block}
  </g>

  <!-- moving scan beam -->
  <rect x="0" y="0" width="{W}" height="3" fill="{p["accent"]}" opacity="0.08">
    <animate attributeName="y" values="0;{H};0" dur="9s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0;0.18;0" dur="9s" repeatCount="indefinite"/>
  </rect>

  <!-- vignette -->
  <rect width="{W}" height="{H}" fill="url(#vignette)"/>
</svg>
"""


def main():
    for tag, p in (("dark", DARK), ("light", LIGHT)):
        svg = build(p, tag)
        path = os.path.join(ASSETS, f"{tag}.svg")
        with open(path, "w") as f:
            f.write(svg)
        print("wrote", path, len(svg), "bytes")


if __name__ == "__main__":
    main()
