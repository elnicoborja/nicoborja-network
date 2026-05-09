# network-viz-toolkit

Turn your LinkedIn data export into an eight-panel visualization of your professional network. Local. Portable. No API keys, no third-party uploads.

The output is one self-contained HTML file. Open it locally, share it as a link, deploy it to Vercel or any static host. Your data never leaves your computer unless you choose to publish.

Live reference: [network.nicoborja.com](https://network.nicoborja.com)

---

## What you get

A single HTML page with eight ways to read your network:

1. **Density timeline** — connections by year, plus cumulative line.
2. **Roles treemap** — composition by seniority and function.
3. **Score funnel** — proportional view of who passes the ICP filter.
4. **Warmth signals** — mutual endorsements, direct emails, recent invitations.
5. **Eras bar chart** — your career chapters with neutral or personal labels.
6. **Constellation graph** — top 30 priority leads as a force-directed network.
7. **Skills bubbles** — what your network says you do, sized by endorsement count.
8. **Top 30 outreach queue** — sortable table of the highest-scoring connections.

Plus a manifesto block, a method explainer, and a CTA section you can customize.

---

## Step 1 · Export your LinkedIn data

1. Go to [linkedin.com/mypreferences/d/download-my-data](https://www.linkedin.com/mypreferences/d/download-my-data).
2. Pick **"The works: All of the individual files we can provide"** (or the smaller "Connections" subset if that's all you need).
3. Click **Request archive**. LinkedIn emails you a download link in 10 minutes (fast tier) or 24 hours (full tier).
4. Unzip. The files you need:
   - `Connections.csv` (required)
   - `Skills.csv` (optional, enables the skills bubble panel)
   - `Endorsements_Received.csv` (optional, enables mutual-endorsement detection)

---

## Step 2 · Run the parser

Requires Python 3.9+. Stdlib only, no `pip install` needed.

```bash
python parser.py \
  --connections /path/to/Connections.csv \
  --skills      /path/to/Skills.csv \
  --endorsements /path/to/Endorsements_Received.csv \
  --config      ./config.json \
  --out         ./network.html
```

Minimum viable command:

```bash
python parser.py --connections /path/to/Connections.csv --out network.html
```

Open `network.html` in any browser. Done.

---

## Step 3 · Customize via config.json

Optional. If you skip this, defaults are used.

```jsonc
{
  "brand": {
    "USER_NAME":      "Your Name",
    "BRAND":          "YOUR BRAND",
    "USER_DOMAIN":    "you.example.com",
    "DIAGNOSTIC_URL": "https://example.com",
    "SUBSTACK_URL":   "https://example.substack.com",
    "LINKEDIN_URL":   "https://linkedin.com/in/youhandle",
    "TOOLKIT_REPO":   "https://github.com/youhandle/network-viz-toolkit"
  },
  "icp_keywords": ["marketing", "growth", "product", "design"],
  "ai_intent_keywords": ["ai", "machine learning", "data", "automation"],
  "senior_keywords": ["chief", "vp", "head", "director", "founder"],
  "latam_keywords": ["latam", "mexico", "colombia", "spain"],
  "eras": {
    "Early career (2010-2013)":   [2010, 2013],
    "Mid career (2014-2018)":     [2014, 2018],
    "Pivot (2019-2021)":          [2019, 2021],
    "Current chapter (2022-2026)":[2022, 2026]
  }
}
```

Era ranges are personal. If you don't define them, the parser auto-detects four equal-density chunks and labels them `Capítulo 1 (...)` through `Capítulo 4 (...)`. Override per your career story.

---

## Step 4 · Use it with an LLM (optional)

`SKILL.md` in this folder is a description anyone can paste into Claude Code, Cursor, or another agentic LLM. The model reads your CSV, runs the parser, and hands you the HTML. No coding required.

Workflow inside an LLM tool:

1. Paste `SKILL.md` as a system / skill prompt.
2. Attach `Connections.csv` (and optionally Skills + Endorsements).
3. Tell it your ICP in plain English.
4. It returns `network.html`.

---

## Privacy

This is a local-only toolkit. Your CSV does not leave your computer. The output HTML embeds your data inline, so:

- **Local view**: your data, your screen. No network traffic for the data.
- **Public deploy**: if you upload `network.html` to Vercel / Netlify / anywhere, the page contains your inlined contact list, scores, and signals. Treat it as public. Redact names with `--redact` (coming v2) if you want to publish without exposing identities.

External CDN dependencies (Tailwind, D3.js, Google Fonts) are loaded by the browser when someone opens the page. They do not see your data.

---

## Voice and design

The template enforces SOUND voice:

- Anti-marketing register, operator tone.
- No em-dashes (`—`) or en-dashes (`–`).
- Banned words: `impactar`, `leverage`, `game-changer`, `disrupting`, `potenciar`, `sinergia`.
- Tagline: "Net results, sin ruido."

If you want a different voice, fork the template and edit copy. The data injection still works.

---

## File map

```
network-viz-toolkit/
├── README.md                          (this file)
├── SKILL.md                           (LLM-ready instructions)
├── parser.py                          (Python 3.9+, stdlib only)
├── template.html                      (HTML with {{PLACEHOLDERS}})
├── config.example.json                (example config)
└── example/
    └── insights.example.json          (example output of build_insights)
```

---

## Roadmap

- v1 (now): parser + template, brand templating, era binning.
- v1.1: redaction mode (`--redact` flag).
- v1.2: optional company-domain enrichment via free `disposable_email_domains` list.
- v2: Apollo / Clay enrichment hooks (opt-in).

PRs welcome. License: MIT.

---

## Credits

Built during a 14-day public sprint with [Lab10](https://lab10.ai). The first version sits at [network.nicoborja.com](https://network.nicoborja.com). The original architect of the eight-panel format owes a debt to data viz patterns from a Spotify thesis project (top-10 artists 2021-2023), where each insight got its own dedicated chart type.

Net results, sin ruido.
