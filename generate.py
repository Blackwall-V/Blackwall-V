#!/usr/bin/env python3
"""Generate two RETRO animated SVGs (dark.svg, light.svg) for the Blackwall-V
GitHub profile. Pure SVG + SMIL only — no CSS, HTML, or script.

Layout: a large block "V" logo on the left, terminal content on the right.
Canvas stays at 940px wide. ASCII art is the "V" character rendered large.

NOTE on the fix: the previous version broke because the V-logo <text>
elements had letter-spacing="2". Box-drawing glyphs (╗ ╔ ╚ ╝ ║ ═) are drawn
to tile edge-to-edge with the full-block glyph (█) — zero gap. Adding
letter-spacing pushes every character apart, so the corner/hook strokes
detach visually from the blocks next to them. That's the "extra lines
sticking out" artifact. Removing letter-spacing (and using real monospace
metrics for layout) fixes it while keeping the ASCII art itself.
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ROOT, "assets")
os.makedirs(ASSETS, exist_ok=True)

# Large block "V" logo (6 lines, rendered at large font-size)
ASCII_V = [
    "    ██╗   ██╗",
    "    ██║   ██║",
    "    ██║   ██║",
    "    ╚██╗ ██╔╝",
    "     ╚████╔╝",
    "      ╚══╝",
]

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
    W, H = 960, 480

    # ---- left side: large V logo ----
<<<<<<< HEAD
    # Real monospace metrics: char width ≈ 0.6 * font-size, line-height ≈ 1.25 * font-size.
    # These are only used for LAYOUT (divider / right-column position) — the
    # actual glyph rendering is untouched (no letter-spacing).
    logo_font = 30
    logo_cw = round(logo_font * 0.6)     # ≈ 18
    logo_ch = round(logo_font * 1.25)    # ≈ 38
    logo_w = max(len(l) for l in ASCII_V) * logo_cw
    logo_h = len(ASCII_V) * logo_ch
=======
    # 6 lines, max 13 chars, at font-size 44, ch≈52, cw≈26
    logo_font = 30
    logo_ch = 52
    logo_cw = 26
    logo_w = max(len(l) for l in ASCII_V) * logo_cw  # ~338
    logo_h = len(ASCII_V) * logo_ch                  # ~312
>>>>>>> e01b0d0b2cbc6415d907318b7163d5dd7bef6023

    # ---- panel & layout ----
    panel_x, panel_y = 22, 50
    panel_w = W - 44
    panel_h = H - panel_y - 18

    logo_ax = 60          # left padding from panel
    content_top = panel_y + 34       # below title bar
    content_bottom = H - 40 - 14      # above status bar
    logo_ay = content_top + (content_bottom - content_top - logo_h) / 2

    # ---- right side: terminal content ----
    script = [
        (True,  "whoami",                                   p["accent"]),
        (False, "blackwall-v — data/ML engineer",            p["fg"]),
        (True,  "cat stack.txt",                            p["accent"]),
        (False, "python · pandas · sklearn · pycaret",      p["fg"]),
        (False, "rust · lua · linux",                       p["fg"]),
        (True,  "echo $STATUS",                             p["accent"]),
        (False, "open to collaboration",                    p["accent3"]),
    ]

    right_x = logo_ax + logo_w + 40   # gap between logo and script (base calc)
    left_block_start = panel_x + 20
    left_block_end = right_x - 20
    logo_ax = left_block_start + (left_block_end - left_block_start - logo_w) / 2
    script_x = right_x
    script_first_y = logo_ay + 12
    line_step = 22
    begin = 0.4
    step = 1.0
    nodes = []
    for i, (is_cmd, text, color) in enumerate(script):
        y = script_first_y + i * line_step
        b = begin + i * step
        if is_cmd:
            nodes.append(
                f'  <g opacity="0">'
                f'<text x="{script_x}" y="{y}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
                f'font-size="14" font-weight="700" fill="{p["amber"]}">$</text>'
                f'<text x="{script_x+18}" y="{y}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
                f'font-size="14" font-weight="700" fill="{color}">{esc(text)}</text>'
                f'<animate attributeName="opacity" from="0" to="1" begin="{b:.2f}s" dur="0.35s" fill="freeze"/>'
                f'</g>'
            )
        else:
            nodes.append(
                f'  <g opacity="0">'
                f'<text x="{script_x+18}" y="{y}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
                f'font-size="14" font-weight="500" fill="{color}">{esc(text)}</text>'
                f'<animate attributeName="opacity" from="0" to="1" begin="{b:.2f}s" dur="0.35s" fill="freeze"/>'
                f'</g>'
            )
    script_block = "\n".join(nodes)

    # ---- V logo lines with reveal + persistent pulse ----
    # xml:space="preserve" keeps leading spaces; NO letter-spacing (see note above).
    v_nodes = []
    for i, l in enumerate(ASCII_V):
        y = logo_ay + i * logo_ch + logo_ch * 0.82
        b = 0.2 + i * 0.18
        glow_dur = 3.6 + i * 0.4
        v_nodes.append(
            f'      <text x="{logo_ax}" y="{y:.1f}" xml:space="preserve" '
            f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
            f'font-size="{logo_font}" font-weight="700" '
            f'fill="{p["fg"]}" opacity="0">{esc(l)}'
            f'<animate attributeName="opacity" from="0" to="1" begin="{b:.2f}s" dur="0.5s" fill="freeze"/>'
            f'<animate attributeName="opacity" values="1;0.55;1" begin="3s" '
            f'dur="{glow_dur:.1f}s" repeatCount="indefinite"/>'
            f'</text>'
        )
    v_block = "\n".join(v_nodes)

    # ---- scanlines ----
    scanlines = [f'<rect x="0" y="{y}" width="{W}" height="1" fill="{p["scan"]}"/>' for y in range(0, H, 3)]
    scan_block = "\n".join(scanlines)

    # ---- $ ls prompt label + stack tags (below the script) ----
    ls_y = script_first_y + len(script) * line_step + 22
    tag_y = ls_y + 20
    tags = ["python", "pandas", "sklearn", "pycaret", "rust", "lua", "linux"]
    tag_nodes = []
    cx = script_x
    for i, t in enumerate(tags):
        label = f"[{t}]"
        w = len(label) * 8.4 + 6
        tag_nodes.append(
            f'      <g opacity="0">'
            f'<text x="{cx}" y="{tag_y}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
            f'font-size="13" font-weight="700" fill="{p["amber"]}">{label}</text>'
            f'<animate attributeName="opacity" from="0" to="1" begin="{2.4+i*0.12:.2f}s" dur="0.4s" fill="freeze"/>'
            f'</g>'
        )
        cx += w + 10
    tags_block = "\n".join(tag_nodes)

    status_y = H - 40

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"
     role="img" aria-label="Blackwall-V retro terminal ({tag})">
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
    <circle cx="160" cy="240" r="110" fill="{p["accent"]}">
      <animate attributeName="cx" values="160;220;160" dur="18s" repeatCount="indefinite"/>
    </circle>
    <circle cx="780" cy="180" r="90" fill="{p["amber"]}" opacity="0.7">
      <animate attributeName="cx" values="780;700;780" dur="22s" repeatCount="indefinite"/>
    </circle>
    <circle cx="600" cy="360" r="80" fill="{p["accent3"]}" opacity="0.5">
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

  <!-- large V logo on the left -->
  <g filter="url(#bloom)">
{v_block}
  </g>

  <!-- vertical divider between logo and script -->
  <line x1="{right_x-20}" y1="{logo_ay-10}" x2="{right_x-20}" y2="{logo_ay+logo_h+10}"
        stroke="{p["accent"]}" stroke-width="1" opacity="0.4">
    <animate attributeName="opacity" values="0.2;0.6;0.2" dur="4s" repeatCount="indefinite"/>
  </line>

  <!-- typed script on the right -->
{script_block}

  <!-- $ ls ./stack label -->
  <text x="{script_x}" y="{ls_y}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
        font-size="13" font-weight="700" fill="{p["muted"]}">$ ls ./stack</text>
{tags_block}

  <!-- status bar -->
  <rect x="{panel_x}" y="{status_y}" width="{panel_w}" height="26" fill="#000000" opacity="0.5"/>
  <rect x="{panel_x}" y="{status_y}" width="{panel_w}" height="26" fill="none" stroke="{p["panel_edge"]}" stroke-width="1"/>
  <circle cx="{panel_x+18}" cy="{status_y+13}" r="4" fill="#28c840">
    <animate attributeName="opacity" values="1;0.3;1" dur="1.6s" repeatCount="indefinite"/>
  </circle>
  <text x="{panel_x+32}" y="{status_y+17}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
        font-size="11" fill="{p["accent"]}">online</text>
  <text x="{panel_x+90}" y="{status_y+17}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
        font-size="11" fill="{p["muted"]}">| branch: main | utf-8 | RETRO-OS v1.0</text>
  <text x="{panel_x+panel_w-18}" y="{status_y+17}" text-anchor="end"
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
