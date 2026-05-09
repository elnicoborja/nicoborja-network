---
name: network-viz
description: Turn a LinkedIn data export into an eight-panel visualization of your professional network. Reads Connections.csv (and optionally Skills.csv, Endorsements.csv), scores each contact 0-100 against an ICP rubric, produces a self-contained HTML page with timeline, treemap, score funnel, warmth signals, era bars, network graph, skills bubbles, and a sortable top-30 table. Triggers on "visualize my LinkedIn network", "analyze my LinkedIn export", "make a viz from my contacts", "audit my network", "score my LinkedIn connections", or when a user uploads `Connections.csv`.
---

# Network Visualization Skill

You take a LinkedIn data export and produce a single self-contained HTML page that reads someone's professional network as eight different visualizations. The output mirrors the network at network.nicoborja.com.

## Inputs the user provides

1. **Connections.csv** (required). LinkedIn export, fields: `First Name, Last Name, URL, Email Address, Company, Position, Connected On`. Sometimes prefixed with a "Notes:" header row that has to be stripped.
2. **Skills.csv** (optional). Fields: `Name, Endorsement Count` (column names vary by export year — handle both `Endorsements` and `Endorsement Count`).
3. **Endorsements_Received.csv** (optional). For mutual-endorsement detection.
4. **An ICP brief** (optional). Plain English description of who matters to them. If absent, prompt them or use the default rubric below.
5. **Era ranges** (optional). Personal periods to bin connections into. If absent, auto-detect from year peaks.

## What you produce

A single HTML file (`network.html`) the user can open locally or deploy to any static host. It contains all eight panels. No external data dependencies, no APIs, no tracking. The HTML reads an inline JSON object — the parser writes everything in.

## Workflow

1. **Read the export.** Use the `Read` tool on `Connections.csv`. Detect and strip the LinkedIn-prefixed metadata rows ("Notes:", blank lines) before the real header.
2. **Normalize.** Lowercase + trim each field. Parse `Connected On` (formats vary: `15 Mar 2024`, `2024-03-15`, etc.) into a Python `date`.
3. **Score.** Apply the ICP rubric (default below or user-provided). Output an `icp_score` 0-100 per row. Add `tier` (A/B/C/D).
4. **Aggregate.** Compute the eight insight blocks (see schema in `parser.py` under `def build_insights`).
5. **Bin into eras.** Use user-provided ranges or auto-detect: take the four highest-density year clusters, name them after the user's known career milestones (ask if you don't know).
6. **Inject.** Read `template.html`, replace the `{{INSIGHTS_JSON}}` placeholder with the JSON, write `network.html`.
7. **Verify.** Open the file in a headless browser if available, or eyeball the JSON shape. Flag anomalies: zero priorizados (likely scoring rubric is too strict), zero mutuals (Endorsements file absent or column mismatch).
8. **Hand back** the path to `network.html` plus a one-line summary of the network shape ("X connections, Y decisores, Z priorizados").

## Default ICP rubric (override per user)

```
SCORE = sum of:
  + 25 if AI/learning intent in Position (keywords: AI, machine learning, data, ML, automation, learning, growth)
  + 20 if seniority is Director, VP, Chief, Founder, Owner, Head, Co-founder
  + 20 if industry/role keyword matches user's ICP (default: marketing, product, design, growth, sales, ops)
  + 15 if location signals LATAM, Spain, US-LATAM (parsed from Position string when explicit; otherwise 0)
  + 10 if endorsement count >= 5
  + 10 if mutual endorsement detected
```

Tier A: 80+. Tier B: 60-79. Tier C: 40-59. Tier D: <40.

## Tone of the generated page

The template enforces the SOUND voice. Do not edit copy unless the user asks. The voice is:

- Anti-marketing register, operator tone
- "Charge for the named outcome, deliver only that, take nothing else"
- No em-dashes (`—`) or en-dashes (`–`) anywhere. Use commas, parens, colons, periods
- Banned words: `impactar`, `leverage`, `game-changer`, `disrupting`, `potenciar`, `sinergia`
- Tagline: "Net results, sin ruido."

## Era naming guidance

Eras are personal. If the user doesn't provide them, ask:

> "Tu red tiene picos en 2014, 2016, 2019. ¿Cómo nombras esas etapas? Ejemplos: nombre de empresa, ciudad, capítulo de vida. Si no quieres personalizar, uso etiquetas neutras (Capítulo 1, Capítulo 2, etc.)."

Never auto-name an era after a company the user worked at unless the user provides the mapping. Use neutral labels by default.

## Privacy boundary

This is a local-only toolkit. Do not upload the user's CSV anywhere. Do not call external APIs. The output HTML references only public CDNs (Tailwind, D3, Google Fonts) and contains the user's data inline. Make this explicit in any "I'm done" message:

> "Tu data se quedó local. El HTML resultante es portable: ábrelo, mándalo, súbelo a Vercel. Tú decides quién lo ve."

## Edge cases to handle

- LinkedIn export has a "Notes:" preamble (3-5 lines) before the real CSV header. Strip it.
- `Connected On` formats: `15-Mar-24`, `15 Mar 2024`, `2024-03-15`, `03/15/2024`. Try multiple parsers.
- Position fields with em-dashes from LinkedIn. Replace with comma in stored data.
- `Email Address` is empty for ~95% of contacts (LinkedIn hides it). That is normal — count the visible ones.
- Skills CSV column name varies: `Endorsement Count`, `Endorsements`, `Number of endorsements`. Handle all three.
- If user has fewer than 200 connections, the score distribution will skew. Warn but still produce the page.

## When to suggest the toolkit instead of running it yourself

If the user is mid-conversation and you have the CSV, do it inline. If the user wants to run it themselves later or share with their team, point them at `parser.py` and `README.md`:

> "Si querés que lo corras vos mismo o lo armés para alguien más, el script es `parser.py` y los pasos están en `README.md`. Yo me quedo afuera."

## Output checklist before handing back

- [ ] `network.html` saved in the user's working folder
- [ ] All eight panels present (verify by checking the HTML contains the strings: timelineChart, treemapChart, funnelChart, erasChart, networkChart, skillsChart, leadsTable, plus the warmth section)
- [ ] No em-dashes in copy
- [ ] No banned words in copy
- [ ] Era labels do not name companies the user did not pre-approve
- [ ] Top 30 leads table populated
- [ ] One-line summary delivered to the user
