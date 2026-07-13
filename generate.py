#!/usr/bin/env python3
"""Generate two premium animated SVGs (dark.svg, light.svg) for the Blackwall-V
GitHub profile. Pure SVG + SMIL only — no CSS, no HTML, no script."""
import os
import pyfiglet

ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ROOT, "assets")
os.makedirs(ASSETS, exist_ok=True)

DARK = dict(
    bg0="#0a0e1a", bg1="#121833",
    glass="rgba(20,28,48,0.55)", glass_hi="rgba(35,46,80,0.65)",
    edge="rgba(120,140,220,0.35)",
    grid="rgba(90,120,210,0.07)",
    fg="#e6ecff", muted="#8b97c4",
    accent="#7aa2ff", accent2="#b07cff", accent3="#39e6c9",
    orb1="#b07cff", orb2="#39e6c9", orb3="#7aa2ff",
)
LIGHT = dict(
    bg0="#eef2fb", bg1="#ffffff",
    glass="rgba(255,255,255,0.70)", glass_hi="rgba(255,255,255,0.90)",
    edge="rgba(90,120,210,0.30)",
    grid="rgba(80,110,200,0.08)",
    fg="#0e1530", muted="#5b6a93",
    accent="#3a64d8", accent2="#8a3df0", accent3="#0aa590",
    orb1="#8a3df0", orb2="#0aa590", orb3="#3a64d8",
)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def ascii_lines(text, font="slant"):
    raw = pyfiglet.figlet_format(text, font=font)
    lines = [ln.rstrip() for ln in raw.split("\n")]
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    return lines


def build(p, tag):
    W, H = 840, 460
    lines = ascii_lines("BLACKWALL-V", "slant")
    cw, ch = 8.4, 17
    ay = 78
    ax = 44
    panel_w = max(len(l) for l in lines) * cw + 48
    panel_h = len(lines) * ch + 60

    # ---- ASCII lines: per-line SMIL reveal + soft glow pulse (opacity) ----
    ascii_nodes = []
    for i, l in enumerate(lines):
        y = ay + i * ch + ch * 0.78
        content = esc(l) or " "
        begin = 0.15 + i * 0.10
        ascii_nodes.append(
            f'      <text x="{ax}" y="{y:.1f}" '
            f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
            f'font-size="15" font-weight="700" letter-spacing="0.6" '
            f'fill="{p["fg"]}" opacity="0">{content}'
            f'<animate attributeName="opacity" from="0" to="1" begin="{begin:.2f}s" '
            f'dur="0.45s" fill="freeze"/>'
            f'<animate attributeName="opacity" values="1;0.65;1" begin="2s" '
            f'dur="{4+i*0.4:.1f}s" repeatCount="indefinite"/>'
            f'</text>'
        )
    ascii_block = "\n".join(ascii_nodes)

    # ---- Typing effect: cycle through words with SMIL opacity on each ----
    words = ["Data Miner.", "ML Engineer.", "Linux Ricer.", "Rust Enjoyer."]
    tw, th = 510, 64
    ty = 232
    tx = 498
    # Each word visible for a window; build keyTimes across total duration
    per = 2.4
    total = per * len(words)
    word_nodes = []
    for i, w in enumerate(words):
        start = i * per
        a = start / total
        b = (start + 0.1) / total
        c = (start + per - 0.15) / total
        d = (start + per - 0.02) / total
        e = (start + per) / total
        word_nodes.append(
            f'        <text x="{tx}" y="{ty}" '
            f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
            f'font-size="17" font-weight="700" fill="{p["accent"]}" opacity="0">{esc(w)}'
            f'<animate attributeName="opacity" '
            f'values="0;1;1;0;0" keyTimes="0;{a+0.0001:.4f};{c:.4f};{d:.4f};1" '
            f'dur="{total}s" repeatCount="indefinite"/></text>'
        )
    typing_block = "\n".join(word_nodes)

    # ---- Tech pills ----
    pills = ["Python", "Data Science", "ML", "Rust", "Linux", "Hyprland"]
    px = 44
    py = 312
    pill_nodes = []
    for i, it in enumerate(pills):
        w = len(it) * 7.2 + 24
        pill_nodes.append(
            f'      <g opacity="0">'
            f'<rect x="{px}" y="{py}" width="{w:.0f}" height="28" rx="14" '
            f'fill="{p["glass"]}" stroke="{p["edge"]}" stroke-width="1"/>'
            f'<text x="{px+12}" y="{py+19}" font-family="ui-sans-serif,system-ui,Segoe UI,Roboto,sans-serif" '
            f'font-size="12" font-weight="600" fill="{p["fg"]}">{it}</text>'
            f'<animate attributeName="opacity" from="0" to="1" begin="{1.4+i*0.12:.2f}s" dur="0.4s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" '
            f'values="0 6;0 0" keyTimes="0;1" begin="{1.4+i*0.12:.2f}s" dur="0.4s" fill="freeze"/>'
            f'</g>'
        )
        px += w + 10
    pills_block = "\n".join(pill_nodes)

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"
     role="img" aria-label="Blackwall-V animated banner ({tag} mode)">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{p["bg0"]}"/>
      <stop offset="0.5" stop-color="{p["bg1"]}"/>
      <stop offset="1" stop-color="{p["bg0"]}"/>
    </linearGradient>
    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{p["accent"]}"/>
      <stop offset="0.5" stop-color="{p["accent2"]}"/>
      <stop offset="1" stop-color="{p["accent3"]}"/>
    </linearGradient>
    <linearGradient id="glass" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{p["glass_hi"]}"/>
      <stop offset="1" stop-color="{p["glass"]}"/>
    </linearGradient>
    <radialGradient id="glow1" cx="0.18" cy="0.25" r="0.55">
      <stop offset="0" stop-color="{p["orb1"]}" stop-opacity="0.40"/>
      <stop offset="1" stop-color="{p["orb1"]}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glow2" cx="0.85" cy="0.80" r="0.50">
      <stop offset="0" stop-color="{p["orb2"]}" stop-opacity="0.35"/>
      <stop offset="1" stop-color="{p["orb2"]}" stop-opacity="0"/>
    </radialGradient>
    <filter id="blur" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="22"/>
    </filter>
    <pattern id="grid" width="34" height="34" patternUnits="userSpaceOnUse">
      <path d="M34 0H0V34" fill="none" stroke="{p["grid"]}" stroke-width="1"/>
    </pattern>
  </defs>

  <!-- background + grid -->
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect width="{W}" height="{H}" fill="url(#grid)"/>

  <!-- drifting glow fields -->
  <rect x="-60" y="-40" width="500" height="500" fill="url(#glow1)">
    <animate attributeName="x" values="-60;30;-60" dur="16s" repeatCount="indefinite"/>
    <animate attributeName="y" values="-40;20;-40" dur="16s" repeatCount="indefinite"/>
  </rect>
  <rect x="320" y="-30" width="520" height="520" fill="url(#glow2)">
    <animate attributeName="x" values="320;220;320" dur="20s" repeatCount="indefinite"/>
    <animate attributeName="y" values="-30;30;-30" dur="20s" repeatCount="indefinite"/>
  </rect>

  <!-- floating blurred orbs -->
  <g filter="url(#blur)" opacity="0.55">
    <circle cx="120" cy="395" r="62" fill="{p["orb1"]}">
      <animate attributeName="cy" values="395;370;395" dur="9s" repeatCount="indefinite"/>
    </circle>
    <circle cx="720" cy="70" r="52" fill="{p["orb2"]}">
      <animate attributeName="cy" values="70;95;70" dur="11s" repeatCount="indefinite"/>
    </circle>
    <circle cx="660" cy="410" r="42" fill="{p["orb3"]}">
      <animate attributeName="cy" values="410;388;410" dur="8s" repeatCount="indefinite"/>
    </circle>
  </g>

  <!-- top accent bar -->
  <rect x="0" y="0" width="{W}" height="3" fill="url(#accent)">
    <animate attributeName="opacity" values="0.45;1;0.45" dur="3.2s" repeatCount="indefinite"/>
  </rect>

  <!-- ASCII glass panel -->
  <rect x="24" y="42" width="{panel_w:.0f}" height="{panel_h:.0f}" rx="18"
        fill="url(#glass)" stroke="{p["edge"]}" stroke-width="1"/>
  <rect x="24" y="42" width="{panel_w:.0f}" height="28" rx="18" fill="{p["glass_hi"]}" opacity="0.5"/>
  <circle cx="44" cy="56" r="5" fill="#ff5f57"/>
  <circle cx="62" cy="56" r="5" fill="#febc2e"/>
  <circle cx="80" cy="56" r="5" fill="#28c840"/>

{ascii_block}

  <!-- right info card -->
  <g>
    <rect x="470" y="60" width="326" height="210" rx="18"
          fill="url(#glass)" stroke="{p["edge"]}" stroke-width="1">
      <animate attributeName="stroke-opacity" values="0.3;0.7;0.3" dur="6s" repeatCount="indefinite"/>
    </rect>
    <text x="490" y="102" font-family="ui-sans-serif,system-ui,Segoe UI,Roboto,sans-serif"
          font-size="13" font-weight="600" fill="{p["muted"]}" letter-spacing="3">PROFILE</text>
    <text x="490" y="142" font-family="ui-sans-serif,system-ui,Segoe UI,Roboto,sans-serif"
          font-size="28" font-weight="800" fill="{p["fg"]}">Blackwall-V</text>
    <rect x="490" y="158" width="150" height="3" rx="1.5" fill="url(#accent)">
      <animate attributeName="width" values="0;150;150" keyTimes="0;0.6;1" dur="1.2s" begin="1s" fill="freeze"/>
    </rect>

    <!-- typing prompt -->
    <text x="486" y="232" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
          font-size="17" font-weight="700" fill="{p["accent"]}">&gt;</text>
    <!-- typing cursor block -->
    <rect x="498" y="218" width="10" height="18" fill="{p["accent3"]}">
      <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.49;0.5;1" dur="1.05s" repeatCount="indefinite"/>
    </rect>
{typing_block}

    <!-- status -->
    <circle cx="492" cy="252" r="5" fill="#28c840">
      <animate attributeName="opacity" values="1;0.25;1" dur="1.6s" repeatCount="indefinite"/>
    </circle>
    <text x="508" y="256" font-family="ui-sans-serif,system-ui,Segoe UI,Roboto,sans-serif"
          font-size="12" font-weight="500" fill="{p["muted"]}">Building things with data &amp; code</text>
  </g>

  <!-- pills -->
  <g font-family="ui-sans-serif,system-ui,Segoe UI,Roboto,sans-serif">
{pills_block}
  </g>

  <!-- shimmer scanline -->
  <rect x="0" y="0" width="{W}" height="2" fill="url(#accent)" opacity="0">
    <animate attributeName="y" values="0;{H};0" dur="8s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0;0.35;0" dur="8s" repeatCount="indefinite"/>
  </rect>

  <!-- footer -->
  <text x="40" y="{H-22}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
        font-size="11" fill="{p["muted"]}">// prefers-color-scheme: {tag}</text>
  <text x="{W-40}" y="{H-22}" text-anchor="end"
        font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
        font-size="11" fill="{p["muted"]}">github.com/Blackwall-V</text>
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
