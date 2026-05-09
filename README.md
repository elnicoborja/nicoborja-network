# nicoborja-network

**Live**: [network.nicoborja.com](https://network.nicoborja.com)
**Source**: this repo
**License**: MIT, fork freely

A read of my own LinkedIn network as data. 1,342 connections, 17 years, seven professional eras, scored against an ICP filter, ordered as the cola de outreach for the next 14 days.

This repo holds two things:

1. **The deployed site** at `index.html` + `leads.csv` (root). What renders on `network.nicoborja.com`.
2. **The toolkit** at `toolkit/` (parser + template + config + SKILL.md). What anyone else can use to generate their own version from their own LinkedIn export, locally, no server, no shared data.

The site is the example. The toolkit is the actual tool.

## Deploy

Auto-deploys to Vercel on every push to `main`. Production URL is `network.nicoborja.com`.

If you fork: connect Vercel to your fork, branch `main`, no build step needed. The site is static HTML + CSV.

---

## Why this exists

April 10, 2026: I left Thomson Reuters. Thirteen years in marketing, an architecture degree from Universidad de los Andes, a Specialty in Data Visualization from Centro (Mexico City, May 2024). No retainer, no infra, no team.

Thirty days later, this exists. Built with Python stdlib, D3, vanilla HTML, and the official LinkedIn data export. No SaaS, no third-party data routing, no marketing tone.

The point is not that I built it. The point is what gets built when the goal is the named outcome and not the recurring invoice.

---

## How the site works

The eight panels on the live site are eight readings of the same dataset:

01. Densidad por año (timeline of connections per year)
02. Composición de roles (role treemap, contrast-aware text)
03. Filtro del agente (score funnel showing 27 priorizados out of 1,342)
04. Puertas ya abiertas (warmth signals × ICP alignment heat table)
05. Capítulos (eras as horizontal bar)
06. Vista de constelación (top 30 as zoomable, draggable, mobile-responsive force graph)
07. Endorsements como espejo (skill bubbles with certification cross-reference)
08. Cola de outreach (top 30 leads table with score heat band, sortable headers, era color)

All scoring is local. Source data is my own LinkedIn export ZIP, processed by `toolkit/parser.py` against `toolkit/config.example.json`.

---

## How the toolkit works

If you want your own version:

1. Export your LinkedIn data (Settings → Data Privacy → Get a copy of your data). You get a ZIP with `Connections.csv`, `Skills.csv`, `Endorsements.csv` among others.
2. Copy `toolkit/config.example.json` to `config.json` and edit. Fill in your own ICP keywords, era boundaries, brand colors.
3. Run `python3 toolkit/parser.py --connections /path/to/Connections.csv --config ./config.json --out ./my-network.html`.
4. Open `my-network.html` in a browser. That is your own version.

The data never leaves your machine. The toolkit is Python stdlib only, no dependencies.

For LLM-driven workflows, `toolkit/SKILL.md` is the agent-ready instruction set.

---

## What is in this repo

```
.
├── index.html          # The deployed site (network.nicoborja.com)
├── leads.csv           # Public lead CSV (top 30, the cola de outreach)
├── vercel.json         # Vercel deploy config
├── README.md           # This file
├── LICENSE             # MIT
├── .gitignore
├── docs/               # Screenshots, longer-form notes
└── toolkit/
    ├── README.md       # How to use the toolkit
    ├── SKILL.md        # Agent-ready instructions
    ├── parser.py       # The scorer + insights generator
    ├── template.html   # The HTML template the parser fills
    ├── config.example.json
    └── example/
        └── insights.example.json
```

---

## Method, in two lines

Cobrar por el resultado nombrado. Entregar sólo eso. No tomar nada más.

Net results, sin ruido.

---

## License

MIT. Use it, fork it, build your own. Attribution appreciated, not required.
