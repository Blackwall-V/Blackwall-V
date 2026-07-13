#!/usr/bin/env python3
"""Generate two RETRO animated SVGs (dark.svg, light.svg) for the Blackwall-V
GitHub profile. Pure SVG + SMIL only — no CSS, HTML, or script.

Centerpiece: an animated CRT terminal that types shell commands + output
(whoami, cat stack.txt, echo $STATUS), then cycles a role tagline.
No ASCII art, no logos. Single-file, deterministic, GitHub-compatible.
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ROOT, "assets")
os.makedirs(ASSETS, exist_ok=True)

DARK = dict(
    bg0="#0a0f08", bg1="#0d160c",
    panel="#08120a", panel_edge="rgba(60,200,90,0.30)",
    scan="rgba(80,255,120,0.05)",
    fg="#7dffb0", amber="#ffb454",
    muted="#5a8f72",
    accent="#39ff14", accent3="#5fd0ff",
)
LIGHT = dict(
    bg0="#f4f1e6", bg1="#fbf8ee",
    panel="#1a2418", panel_edge="rgba(20,40,24,0.45)",
    scan="rgba(0,0,0,0.04)",
    fg="#0a3d1f", amber="#7a4d00",
    muted="#4a6b58",
    accent="#0a7d28", accent3="#1a5a8a",
)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build(p, tag):
    W, H = 820, 420
    panel_x, panel_y = 24, 40
    panel_w = W - 48
    panel_h = H - panel_y - 18

    # (is_command, text, color)
    script = [
        (True,  "whoami",                                   p["accent"]),
        (False, "blackwall-v  —  data scientist / ml engineer", p["fg"]),
        (True,  "cat stack.txt",                            p["accent"]),
        (False, "python · pandas · scikit-learn · pycaret", p["fg"]),
        (False, "rust · lua · linux",                       p["fg"]),
        (True,  "echo $STATUS",                             p["accent"]),
        (False, "open to collaboration",                    p["accent3"]),
    ]

    line_h = 28
    first_y = 92
    begin = 0.4
    step = 1.1
    nodes = []
    cursor_y = first_y + len(script) * line_h + 4

    for i, (is_cmd, text, color) in enumerate(script):
        y = first_y + i * line_h
        b = begin + i * step
        if is_cmd:
            nodes.append(
                f'  <g opacity="0">'
                f'<text x="56" y="{y}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
                f'font-size="15" font-weight="700" fill="{p["amber"]}">$</text>'
                f'<text x="76" y="{y}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
                f'font-size="15" font-weight="700" fill="{color}">{esc(text)}</text>'
                f'<animate attributeName="opacity" from="0" to="1" begin="{b:.2f}s" dur="0.35s" fill="freeze"/>'
                f'</g>'
            )
        else:
            nodes.append(
                f'  <g opacity="0">'
                f'<text x="76" y="{y}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
                f'font-size="15" font-weight="500" fill="{color}">{esc(text)}</text>'
                f'<animate attributeName="opacity" from="0" to="1" begin="{b:.2f}s" dur="0.35s" fill="freeze"/>'
                f'</g>'
            )
    script_block = "\n".join(nodes)

    # cycling role tagline
    roles = ["data_scientist", "ml_engineer", "python_dev", "open_source"]
    per = 2.6
    total = per * len(roles)
    ty = cursor_y + 8
    role_nodes = []
    for i, w in enumerate(roles):
        start = i * per
        c = (start + per - 0.2) / total
        d = (start + per - 0.04) / total
        role_nodes.append(
            f'  <text x="76" y="{ty}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
            f'font-size="15" font-weight="700" fill="{p["accent3"]}" opacity="0">{esc(w)}'
            f'<animate attributeName="opacity" values="0;1;1;0;0" '
            f'keyTimes="0;{start/total+0.0001:.4f};{c:.4f};{d:.4f};1" dur="{total}s" repeatCount="indefinite"/></text>'
        )
    roles_block = "\n".join(role_nodes)

    # scanlines
    scanlines = [f'<rect x="0" y="{y}" width="{W}" height="1" fill="{p["scan"]}"/>' for y in range(0, H, 3)]
    scan_block = "\n".join(scanlines)

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"
     role="img" aria-label="Blackwall-V terminal ({tag})">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{p["bg1"]}"/>
      <stop offset="0.5" stop-color="{p["bg0"]}"/>
      <stop offset="1" stop-color="{p["bg1"]}"/>
    </linearGradient>
    <radialGradient id="vignette" cx="0.5" cy="0.5" r="0.75">
      <stop offset="0.55" stop-color="#000000" stop-opacity="0"/>
      <stop offset="1" stop-color="#000000" stop-opacity="{0.55 if tag=='dark' else 0.10}"/>
    </radialGradient>
    <filter id="bloom" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="soft" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="36"/>
    </filter>
  </defs>

  <rect width="{W}" height="{H}" fill="url(#bg)"/>

  <g filter="url(#soft)" opacity="0.40">
    <circle cx="160" cy="220" r="110" fill="{p["accent"]}">
      <animate attributeName="cx" values="160;220;160" dur="18s" repeatCount="indefinite"/>
    </circle>
    <circle cx="660" cy="180" r="90" fill="{p["amber"]}" opacity="0.7">
      <animate attributeName="cx" values="660;600;660" dur="22s" repeatCount="indefinite"/>
    </circle>
    <circle cx="540" cy="360" r="80" fill="{p["accent3"]}" opacity="0.5">
      <animate attributeName="cy" values="360;330;360" dur="12s" repeatCount="indefinite"/>
    </circle>
  </g>

  <rect x="{panel_x}" y="{panel_y}" width="{panel_w}" height="{panel_h}" rx="12"
        fill="{p["panel"]}" stroke="{p["panel_edge"]}" stroke-width="1.5"/>
  <rect x="{panel_x}" y="{panel_y}" width="{panel_w}" height="28" rx="12" fill="#000000" opacity="0.55"/>
  <rect x="{panel_x}" y="{panel_y+22}" width="{panel_w}" height="6" fill="#000000" opacity="0.55"/>
  <circle cx="{panel_x+18}" cy="{panel_y+15}" r="5" fill="#ff5f57"/>
  <circle cx="{panel_x+36}" cy="{panel_y+15}" r="5" fill="#febc2e"/>
  <circle cx="{panel_x+54}" cy="{panel_y+15}" r="5" fill="#28c840"/>
  <text x="{panel_x+78}" y="{panel_y+20}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
        font-size="11" fill="{p["muted"]}">blackwall@localhost: ~</text>
  <circle cx="{panel_x+panel_w-22}" cy="{panel_y+15}" r="4" fill="#ff3b30">
    <animate attributeName="opacity" values="1;0.2;1" dur="1.2s" repeatCount="indefinite"/>
  </circle>

  <text x="{panel_x+24}" y="64" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
        font-size="18" font-weight="700" fill="{p["accent"]}" filter="url(#bloom)">blackwall-v</text>
  <rect x="{panel_x+24}" y="72" width="120" height="2" fill="{p["accent"]}" opacity="0.6">
    <animate attributeName="opacity" values="0.2;0.8;0.2" dur="3s" repeatCount="indefinite"/>
  </rect>

{script_block}

  <text x="56" y="{ty}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
        font-size="15" font-weight="700" fill="{p["amber"]}">$</text>
  <rect x="66" y="{ty-14}" width="9" height="17" fill="{p["accent"]}" opacity="0">
    <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.05;0.95;1" dur="1.05s" repeatCount="indefinite"/>
  </rect>
{roles_block}

  <rect x="{panel_x}" y="{H-44}" width="{panel_w}" height="26" fill="#000000" opacity="0.5"/>
  <rect x="{panel_x}" y="{H-44}" width="{panel_w}" height="26" fill="none" stroke="{p["panel_edge"]}" stroke-width="1"/>
  <circle cx="{panel_x+18}" cy="{H-31}" r="4" fill="#28c840">
    <animate attributeName="opacity" values="1;0.3;1" dur="1.6s" repeatCount="indefinite"/>
  </circle>
  <text x="{panel_x+32}" y="{H-27}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
        font-size="11" fill="{p["accent"]}">online</text>
  <text x="{panel_x+90}" y="{H-27}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
        font-size="11" fill="{p["muted"]}">| branch: main | utf-8 | RETRO-OS v1.0</text>
  <text x="{panel_x+panel_w-18}" y="{H-27}" text-anchor="end"
        font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
        font-size="11" fill="{p["amber"]}">github.com/Blackwall-V</text>

  <g opacity="0.9">
{scan_block}
  </g>

  <rect x="0" y="0" width="{W}" height="3" fill="{p["accent"]}" opacity="0.08">
    <animate attributeName="y" values="0;{H};0" dur="9s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0;0.18;0" dur="9s" repeatCount="indefinite"/>
  </rect>

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
