# Changelog

## 2026-05-08

Initial public release. Six panel refinements shipped before move to git:

- **Treemap (panel 02)**: contrast-aware text fill (luminance threshold 0.5), opacity 1.0 on cells, no more washed-out labels on neon yellow.
- **Warmth signals (panel 04)**: replaced three big-number cards with a 3 × 3 heat table (signal type × ICP alignment), log-scaled color, total column on the right preserves the headline figures.
- **Constellation (panel 06)**: 820px desktop height, d3.zoom (0.4-4x) with mouse wheel + drag-to-pan, d3.drag on individual nodes, RESET VIEW button. Below 720px viewport swaps to a vertical sortable list of all 30 leads.
- **Skills bubbles (panel 07)**: full divergent ramp with the 4 darkest steps skipped, semi-transparent label tag behind every visible name so text reads on any fill, certifications cross-reference via `DATA.certified_skills` array (lime border + ✓ glyph).
- **Leads table (panel 08)**: score heat band on the score cell, sortable headers (score, nombre, era), new era column with color dot, subtle tier-row tint.
- **Method copy (panel "Antes de pedirte algo")**: added the asymmetry frame paragraph upfront (agency vs SOUND model), kept the punchy three-line stack, added a closing line ("si el filtro está bien construido…"). No em-dashes.

## Pre-history

Versions before this commit lived as direct Vercel uploads. Repo created today (2026-05-08) so the toolkit can ship as a real artifact rather than a copy-and-paste.
