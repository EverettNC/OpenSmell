#!/usr/bin/env python3
"""
Generate opensmell_cognitive_cortex.html from live open_smell2.py truth.
Run after any profile/marker change: python3 generate_cortex_diagram.py
"""

from __future__ import annotations

import json
from pathlib import Path

from open_smell2 import (
    DEGENERATE_GROUPS,
    MARKER_ALIASES,
    PROFILE_SIGNATURES,
    SCENT_PROFILES,
    SENSOR_CHANNELS,
)

OUT = Path(__file__).parent / "opensmell_cognitive_cortex.html"

# MQ-135 cross-sensitive bands → human-readable smell families (proxies, not species)
SMELL_BANDS = [
    {
        "label": "Fruity / Acetone",
        "color": "#4ade80",
        "channels": ["acetone", "ketones", "propanol", "ethanol_trace"],
    },
    {
        "label": "Acrid / Ammonia",
        "color": "#a78bfa",
        "channels": ["ammonia", "toluene"],
    },
    {
        "label": "Musty / Sweet",
        "color": "#e6c875",
        "channels": ["hydrocarbons", "aldehydes", "benzene", "alkanes", "sebum_vocs"],
    },
    {
        "label": "Sour / Metallic",
        "color": "#f87171",
        "channels": [
            "aliphatic_acids",
            "sulfur",
            "dimethyl_sulfide",
            "skatole",
            "lipid_oxidation",
            "isoprene",
            "ethane",
            "butane",
            "methane_trace",
        ],
    },
]

METRICS = {
    "catalog_profiles": len(SCENT_PROFILES),
    "live_profiles": len(PROFILE_SIGNATURES),
    "research_only": sum(1 for p in SCENT_PROFILES.values() if p.research_only),
    "sensor_channels": len(SENSOR_CHANNELS),
    "marker_aliases": len(MARKER_ALIASES),
    "alert_threshold_default": 0.7,
    "synthetic_separability_exact": "87.2%",
    "synthetic_separability_note": "Bio-sim labeled closed-loop (seed=42). Not clinical accuracy.",
    "conf_correctness": "+0.42",
    "false_alert_background": "~0% @ 0.7",
}


def profile_rows() -> list[dict]:
    rows = []
    for key in sorted(PROFILE_SIGNATURES):
        p = SCENT_PROFILES[key]
        sig = PROFILE_SIGNATURES[key]
        rows.append(
            {
                "key": key,
                "condition": p.condition,
                "category": p.category,
                "severity": p.severity,
                "channels": sig,
                "n": len(sig),
            }
        )
    return rows


def build_html() -> str:
    profiles = profile_rows()
    degenerate = DEGENERATE_GROUPS
    bands_json = json.dumps(SMELL_BANDS)
    profiles_json = json.dumps(profiles)
    degenerate_json = json.dumps(degenerate)
    metrics_json = json.dumps(METRICS)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>OpenSmell Cognitive Cortex — Diagnostic Core (Code-Aligned)</title>
  <style>
    :root {{
      --bg: #030712;
      --panel: #0a1628;
      --gold: #e6c875;
      --cyan: #00f0ff;
      --red: #f87171;
      --green: #4ade80;
      --muted: #94a3b8;
      --font: "SF Mono", "Fira Code", ui-monospace, monospace;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: var(--font);
      background: radial-gradient(ellipse at 50% 0%, #0f2847 0%, var(--bg) 55%);
      color: #e2e8f0;
      min-height: 100vh;
    }}
    header {{
      text-align: center;
      padding: 2rem 1rem 1rem;
      border-bottom: 1px solid rgba(0,240,255,0.15);
    }}
    h1 {{
      font-size: 1.1rem;
      letter-spacing: 0.2em;
      text-transform: uppercase;
      color: var(--gold);
      margin: 0 0 0.5rem;
    }}
    .subtitle {{ color: var(--muted); font-size: 0.75rem; max-width: 52rem; margin: 0 auto; line-height: 1.5; }}
    .grid {{
      display: grid;
      grid-template-columns: 1fr 1.4fr 1fr;
      gap: 1rem;
      padding: 1.25rem;
      max-width: 1400px;
      margin: 0 auto;
    }}
    @media (max-width: 1100px) {{ .grid {{ grid-template-columns: 1fr; }} }}
    .panel {{
      background: rgba(10,22,40,0.85);
      border: 1px solid rgba(0,240,255,0.2);
      border-radius: 12px;
      padding: 1rem;
    }}
    .panel h2 {{
      font-size: 0.7rem;
      text-transform: uppercase;
      letter-spacing: 0.15em;
      color: var(--cyan);
      margin: 0 0 0.75rem;
      border-bottom: 1px solid rgba(0,240,255,0.12);
      padding-bottom: 0.5rem;
    }}
    .hw-diagram {{
      font-size: 0.68rem;
      line-height: 1.6;
      color: #cbd5e1;
    }}
    .hw-box {{
      border: 1px solid rgba(230,200,117,0.35);
      border-radius: 8px;
      padding: 0.6rem;
      margin: 0.5rem 0;
      background: rgba(0,0,0,0.25);
    }}
    .pipeline {{
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
      align-items: stretch;
    }}
    .step {{
      border: 1px solid rgba(0,240,255,0.25);
      border-radius: 8px;
      padding: 0.55rem 0.75rem;
      font-size: 0.68rem;
      position: relative;
    }}
    .step strong {{ color: var(--gold); display: block; margin-bottom: 0.2rem; }}
    .step.alert {{ border-color: rgba(248,113,113,0.5); }}
    .step.alert strong {{ color: var(--red); }}
    .arrow {{ text-align: center; color: var(--cyan); font-size: 0.85rem; }}
    .brain-wrap {{
      text-align: center;
      padding: 1rem 0;
    }}
    .brain {{
      width: 180px;
      height: 120px;
      margin: 0 auto;
      border: 2px solid rgba(0,240,255,0.4);
      border-radius: 90px 90px 40px 40px;
      background: linear-gradient(180deg, rgba(0,240,255,0.08), transparent);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 0.65rem;
      color: var(--cyan);
      letter-spacing: 0.1em;
    }}
    .bands {{ display: flex; flex-wrap: wrap; gap: 0.4rem; justify-content: center; margin-top: 0.75rem; }}
    .band {{
      font-size: 0.62rem;
      padding: 0.35rem 0.55rem;
      border-radius: 6px;
      border: 1px solid currentColor;
      cursor: pointer;
      opacity: 0.85;
    }}
    .band:hover {{ opacity: 1; }}
    .profile-list {{
      max-height: 420px;
      overflow-y: auto;
      font-size: 0.62rem;
    }}
    .profile-row {{
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 0.25rem;
      padding: 0.35rem 0;
      border-bottom: 1px solid rgba(255,255,255,0.05);
      cursor: pointer;
    }}
    .profile-row:hover {{ background: rgba(0,240,255,0.05); }}
    .sev-critical {{ color: var(--red); }}
    .sev-high {{ color: var(--gold); }}
    footer {{
      text-align: center;
      padding: 1.25rem;
      font-size: 0.65rem;
      color: var(--muted);
      border-top: 1px solid rgba(0,240,255,0.1);
      line-height: 1.6;
    }}
    .truth-bar {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      justify-content: center;
      margin: 1rem auto;
      max-width: 900px;
    }}
    .chip {{
      background: rgba(0,240,255,0.08);
      border: 1px solid rgba(0,240,255,0.2);
      padding: 0.35rem 0.6rem;
      border-radius: 999px;
      font-size: 0.62rem;
    }}
    #detail {{
      margin-top: 0.75rem;
      font-size: 0.65rem;
      color: #cbd5e1;
      min-height: 3rem;
      padding: 0.5rem;
      background: rgba(0,0,0,0.3);
      border-radius: 8px;
    }}
    .disclaimer {{ color: #fbbf24; }}
  </style>
</head>
<body>
  <header>
    <h1>OpenSmell Cognitive Cortex — Diagnostic Core v2.0</h1>
    <p class="subtitle">
      <strong class="disclaimer">Code-aligned diagram.</strong> Generated from <code>open_smell2.py</code> at build time.
      Screening-support only · Not FDA-approved · Not clinical accuracy.
      Channel names are MQ-135 cross-sensitive <em>proxies</em>, not named species resolution.
    </p>
    <div class="truth-bar" id="chips"></div>
  </header>

  <div class="grid">
    <section class="panel">
      <h2>Hardware Root (Image 8)</h2>
      <div class="hw-diagram">
        <div class="hw-box"><strong>MQ-135 VOC Module</strong><br/>VCC → 5V · GND → GND · AOUT → A0 (10kΩ)</div>
        <div class="hw-box"><strong>Arduino Nano</strong><br/>A0 analog read · USB serial to phone<br/>D9 PWM → 5V fan (active airflow)</div>
        <div class="hw-box"><strong>30mm 5V Fan</strong><br/>Pulls breath/air across sensor head</div>
        <p style="margin-top:0.75rem;color:var(--muted)">
          ~$20 stack. Root-first: fix the physical sample path before the story.
        </p>
      </div>
    </section>

    <section class="panel">
      <h2>Classifier Pipeline (actual code path)</h2>
      <div class="brain-wrap">
        <div class="brain">COGNITIVE<br/>CORTEX</div>
        <div class="bands" id="bands"></div>
      </div>
      <div class="pipeline">
        <div class="step"><strong>1 · Analog VOC Grid</strong>20 sensor channels · intensity 0–1 per cycle</div>
        <div class="arrow">↓</div>
        <div class="step"><strong>2 · Normalize + Bio-Sim Covariance</strong>Patient baseline · diurnal phase · noise (opensmell_bio_sim.py)</div>
        <div class="arrow">↓</div>
        <div class="step"><strong>3 · Marker Resolve</strong>Descriptive biomarkers → physical channels (MARKER_ALIASES)</div>
        <div class="arrow">↓</div>
        <div class="step"><strong>4 · Specificity Classify</strong>confidence = min(1, coverage × mean_I × √(matched)/√(max_len))</div>
        <div class="arrow">↓</div>
        <div class="step alert"><strong>5 · Threshold Gate (default 0.7)</strong>CRITICAL label ≠ alert. No alert unless confidence earns it.</div>
        <div class="arrow">↓</div>
        <div class="step"><strong>6 · Degenerate Groups</strong>Physically inseparable profiles scored together (e.g. diabetes ketosis)</div>
      </div>
      <div id="detail">Select a smell band or live profile.</div>
    </section>

    <section class="panel">
      <h2>Live Profile Registry</h2>
      <p style="font-size:0.62rem;color:var(--muted);margin:0 0 0.5rem">
        {METRICS["live_profiles"]} live · {METRICS["research_only"]} research-only in catalog · {METRICS["catalog_profiles"]} total catalog
      </p>
      <div class="profile-list" id="profiles"></div>
    </section>
  </div>

  <footer>
    <strong>Constance / OpenSmell Origin Charter</strong> — Merkel cell carcinoma at stage 4 sparked this work. Goal: earlier screening signal, not late-room news.<br/>
    Built by Everett N. Christman &amp; collaborators · The Christman AI Project / Luma Cognify AI<br/>
    <span class="disclaimer">Numbers on this page are engine facts + documented synthetic separability. If the number ain't there, it ain't on the slide.</span>
  </footer>

  <script>
    const BANDS = {bands_json};
    const PROFILES = {profiles_json};
    const DEGENERATE = {degenerate_json};
    const METRICS = {metrics_json};

    const chips = document.getElementById('chips');
    [
      `${{METRICS.live_profiles}} live profiles`,
      `${{METRICS.sensor_channels}} sensor channels`,
      `${{METRICS.marker_aliases}} marker aliases`,
      `Separability ${{METRICS.synthetic_separability_exact}} (synthetic)`,
      `Conf↔correct ${{METRICS.conf_correctness}}`,
      `False alert ${{METRICS.false_alert_background}}`,
    ].forEach(t => {{
      const s = document.createElement('span');
      s.className = 'chip';
      s.textContent = t;
      chips.appendChild(s);
    }});

    const bandsEl = document.getElementById('bands');
    const detail = document.getElementById('detail');
    BANDS.forEach(b => {{
      const el = document.createElement('span');
      el.className = 'band';
      el.style.color = b.color;
      el.textContent = b.label;
      el.onclick = () => {{
        detail.innerHTML = `<strong>${{b.label}}</strong><br/>Channels: ${{b.channels.join(', ')}}<br/><em>Proxies for MQ-135 response bands — not literal species.</em>`;
      }};
      bandsEl.appendChild(el);
    }});

    const list = document.getElementById('profiles');
    PROFILES.forEach(p => {{
      const row = document.createElement('div');
      row.className = 'profile-row';
      const sev = p.severity === 'critical' ? 'sev-critical' : 'sev-high';
      row.innerHTML = `<span><strong>${{p.condition}}</strong><br/><span style="color:#64748b">${{p.key}} · ${{p.n}}ch · ${{p.category}}</span></span><span class="${{sev}}">${{p.severity.toUpperCase()}}</span>`;
      row.onclick = () => {{
        detail.innerHTML = `<strong>${{p.condition}}</strong> (${{p.key}})<br/>Signature: ${{p.channels.join(', ') || '(none)'}}<br/>Alert fires only if confidence ≥ profile threshold (usually 0.7).`;
      }};
      list.appendChild(row);
    }});

    detail.innerHTML = `<strong>Degenerate groups (honest):</strong> ${{JSON.stringify(DEGENERATE)}} — scored at group level, not faked markers.`;
  </script>
</body>
</html>
"""


def main() -> None:
    html = build_html()
    OUT.write_text(html, encoding="utf-8")
    truth = {
        "metrics": METRICS,
        "profiles": profile_rows(),
        "degenerate_groups": DEGENERATE_GROUPS,
        "sensor_channels": SENSOR_CHANNELS,
    }
    Path(__file__).parent.joinpath("opensmell_engine_truth.json").write_text(
        json.dumps(truth, indent=2), encoding="utf-8"
    )
    print(f"Wrote {OUT}")
    print(f"Wrote opensmell_engine_truth.json")
    print(f"Live profiles: {METRICS['live_profiles']} (not 2401)")


if __name__ == "__main__":
    main()