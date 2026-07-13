#!/usr/bin/env python3
"""Generate two RETRO animated SVGs (dark.svg, light.svg) for the Blackwall-V
GitHub profile. Pure SVG + SMIL only — no CSS, HTML, or script.

Centerpiece: animated CRT terminal with:
  - BLOCK ASCII art logo (BLACKWALL-V) at the top, with generous padding.
  - Typed shell-command script (whoami / cat stack / echo $STATUS).
  - Stack tags row.
  - Bottom status bar.
  - CRT background: drifting phosphor glow blobs, scanlines, scan beam, vignette.

All layout is computed so vertical positions are separated by positive gaps.
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ROOT, "assets")
os.makedirs(ASSETS, exist_ok=True)

# ASCII art hard-coded so the output is deterministic.
ASCII = [
    "*@@@***@@m *@@@                   *@@@                                   *@@@   *@@@          *@@@@*   *@@@*  *@",
    "  @@    @@   @@                     @@                                     @@     @@            *@@     m@    m@",
    "  @@    @@   @@   m@*@@m   m@@*@@   @@  m@@* *@@*    m@    *@@* m@*@@m     @@     @@             @@m   m@     *@",
    "  @@***@mm   !@  @@   @@  @@*  @@   @@ m@      @@   m@@@   m@  @@   @@     !@     !@              @@m  @*     m@",
    "  @!    *@   !@   m@@@!@  @!        !@m@@       @@ m@  @@ m@    m@@@!@     !@     !@    @@@@@     *!@ !*      *@",
    "  !!    m@   !@  @!   !@  @!m    m  !@ *@@m      @@@    @!!    @!   !@     !@     !@               !@@m      m@",
    "  !:    *!   !!   !!!!:!  !!        !!!!!        !@!!   !:!     !!!!:!     !!     !!               !! !*      *@",
    "  !:    !!   :!  !!   :!  !:!    !  :! *!!!      !!!    !:!    !!   :!     :!     :!               !!::     :@",
    ": !: : : : : : :!: : !:  : : :  : : :  : :      :      :     :!: : !:  : : :  : : :               :       ::",
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
    W, H = 940, 600

    # ---- compute ASCII dimensions ----
    # at font-size 12 monospace, advance ~7.2px
    cw, ch = 7.2, 17
    ascii_w = max(len(l) for l in ASCII) * cw
    ascii_h = len(ASCII) * ch

    # ---- panel & ASCII placement (padding around the figlet) ----
    panel_x, panel_y = 22, 50
    panel_w = ascii_w + 84
    panel_h = H - panel_y - 18

    ax = 60
    ay = 108

    # ---- typed script (compact, 5 lines) ----
    script = [
        (True,  "whoami",                                   p["accent"]),
        (False, "blackwall-v — data/ML engineer",            p["fg"]),
        (True,  "cat stack.txt",                            p["accent"]),
        (False, "python · pandas · sklearn · pycaret",      p["fg"]),
        (False, "rust · lua · linux",                       p["fg"]),
        (True,  "echo $STATUS",                             p["accent"]),
        (False, "open to collaboration",                    p["accent3"]),
    ]

    # ---- typed script positioning (clear of ASCII + divider) ----
    div_y = ay + ascii_h + 14
    ty = div_y + 36
    line_step = 22
    begin = 0.4
    step = 1.0
    nodes = []
    for i, (is_cmd, text, color) in enumerate(script):
        y = ty + i * line_step
        b = begin + i * step
        if is_cmd:
            nodes.append(
                f'  <g opacity="0">'
                f'<text x="{ax}" y="{y}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
                f'font-size="14" font-weight="700" fill="{p["amber"]}">$</text>'
                f'<text x="{ax+18}" y="{y}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
                f'font-size="14" font-weight="700" fill="{color}">{esc(text)}</text>'
                f'<animate attributeName="opacity" from="0" to="1" begin="{b:.2f}s" dur="0.35s" fill="freeze"/>'
                f'</g>'
            )
        else:
            nodes.append(
                f'  <g opacity="0">'
                f'<text x="{ax+18}" y="{y}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
                f'font-size="14" font-weight="500" fill="{color}">{esc(text)}</text>'
                f'<animate attributeName="opacity" from="0" to="1" begin="{b:.2f}s" dur="0.35s" fill="freeze"/>'
                f'</g>'
            )
    script_block = "\n".join(nodes)

    # ---- ASCII art lines with reveal + persistent pulse ----
    ascii_nodes = []
    for i, l in enumerate(ASCII):
        y = ay + i * ch + ch * 0.82
        b = 0.2 + i * 0.12
        glow_dur = 3.6 + i * 0.4
        ascii_nodes.append(
            f'      <text x="{ax}" y="{y:.1f}" '
            f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
            f'font-size="12" font-weight="700" letter-spacing="0.5" '
            f'fill="{p["fg"]}" opacity="0">{esc(l)}'
            f'<animate attributeName="opacity" from="0" to="1" begin="{b:.2f}s" dur="0.45s" fill="freeze"/>'
            f'<animate attributeName="opacity" values="1;0.55;1" begin="3s" '
            f'dur="{glow_dur:.1f}s" repeatCount="indefinite"/>'
            f'</text>'
        )
    ascii_block = "\n".join(ascii_nodes)

    # ---- scanlines ----
    scanlines = [f'<rect x="0" y="{y}" width="{W}" height="1" fill="{p["scan"]}"/>' for y in range(0, H, 3)]
    scan_block = "\n".join(scanlines)

    # ---- prompt above ASCII ----
    prompt_y = ay - 14

    # ---- ls prompt label + stack tags ----
    ls_y = ty + len(script) * line_step + 28
    tag_y = ls_y + 20
    tags = ["python", "pandas", "sklearn", "pycaret", "rust", "lua", "linux"]
    tag_nodes = []
    cx = ax
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
      <feGaussianBlur stdDeviation="4" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="soft" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="36"/>
    </filter>
  </defs>

  <rect width="{W}" height="{H}" fill="url(#bg)"/>

  <g filter="url(#soft)" opacity="0.40">
    <circle cx="160" cy="300" r="120" fill="{p["accent"]}">
      <animate attributeName="cx" values="160;240;160" dur="18s" repeatCount="indefinite"/>
    </circle>
    <circle cx="780" cy="220" r="100" fill="{p["amber"]}" opacity="0.7">
      <animate attributeName="cx" values="780;700;780" dur="22s" repeatCount="indefinite"/>
    </circle>
    <circle cx="600" cy="480" r="90" fill="{p["accent3"]}" opacity="0.5">
      <animate attributeName="cy" values="480;450;480" dur="12s" repeatCount="indefinite"/>
    </circle>
  </g>

  <rect x="{panel_x}" y="{panel_y}" width="{panel_w:.0f}" height="{panel_h:.0f}" rx="12"
        fill="{p["panel"]}" stroke="{p["panel_edge"]}" stroke-width="1.5"/>
  <rect x="{panel_x}" y="{panel_y}" width="{panel_w:.0f}" height="28" rx="12" fill="#000000" opacity="0.55"/>
  <rect x="{panel_x}" y="{panel_y+22}" width="{panel_w:.0f}" height="6" fill="#000000" opacity="0.55"/>
  <circle cx="{panel_x+18}" cy="{panel_y+15}" r="5" fill="#ff5f57"/>
  <circle cx="{panel_x+36}" cy="{panel_y+15}" r="5" fill="#febc2e"/>
  <circle cx="{panel_x+54}" cy="{panel_y+15}" r="5" fill="#28c840"/>
  <text x="{panel_x+78}" y="{panel_y+20}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
        font-size="11" fill="{p["muted"]}">blackwall@localhost: ~</text>
  <circle cx="{panel_x+panel_w-22:.0f}" cy="{panel_y+15}" r="4" fill="#ff3b30">
    <animate attributeName="opacity" values="1;0.2;1" dur="1.2s" repeatCount="indefinite"/>
  </circle>

  <!-- prompt above ASCII -->
  <text x="{ax}" y="{prompt_y}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
        font-size="13" font-weight="700" fill="{p["amber"]}">$ figlet Blackwall-V</text>
  <rect x="{ax+170}" y="{prompt_y-12}" width="9" height="14" fill="{p["amber"]}">
    <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.49;0.5;1" dur="1s" repeatCount="indefinite"/>
  </rect>

  <!-- ASCII art with bloom -->
  <g filter="url(#bloom)">
{ascii_block}
  </g>

  <!-- divider under ASCII -->
  <line x1="{ax}" y1="{div_y}" x2="{panel_x+panel_w-20:.0f}" y2="{div_y}"
        stroke="{p["accent"]}" stroke-width="1" opacity="0.5">
    <animate attributeName="opacity" values="0.2;0.7;0.2" dur="4s" repeatCount="indefinite"/>
  </line>

  <!-- typed script -->
{script_block}

  <!-- $ ls ./stack label -->
  <text x="{ax}" y="{ls_y}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
        font-size="13" font-weight="700" fill="{p["muted"]}">$ ls ./stack</text>
{tags_block}

  <!-- status bar -->
  <rect x="{panel_x}" y="{status_y}" width="{panel_w:.0f}" height="26" fill="#000000" opacity="0.5"/>
  <rect x="{panel_x}" y="{status_y}" width="{panel_w:.0f}" height="26" fill="none" stroke="{p["panel_edge"]}" stroke-width="1"/>
  <circle cx="{panel_x+18}" cy="{status_y+13}" r="4" fill="#28c840">
    <animate attributeName="opacity" values="1;0.3;1" dur="1.6s" repeatCount="indefinite"/>
  </circle>
  <text x="{panel_x+32}" y="{status_y+17}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
        font-size="11" fill="{p["accent"]}">online</text>
  <text x="{panel_x+90}" y="{status_y+17}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
        font-size="11" fill="{p["muted"]}">| branch: main | utf-8 | RETRO-OS v1.0</text>
  <text x="{panel_x+panel_w-18:.0f}" y="{status_y+17}" text-anchor="end"
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
