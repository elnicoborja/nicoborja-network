# Changelog

## 2026-05-09 · Iteration 2 (mobile fixes + horizontal timeline + cert overlay)

Hot iteration after Day 5 mobile QA. Six changes batched into one PR.

- **Mobile constellation blocker fix.** Class-toggle inversion in `applyResponsiveLayout()` was hiding the mobile list on mobile devices instead of showing it. iPhone 15 Pro (and any viewport under 720px) was rendering an empty container. Fixed.
- **Treemap text contrast (panel 02).** Switched from WCAG luminance to HSP perceived-brightness. Pink/magenta/cyan cells now correctly get black text instead of being treated as "dark" by raw luminance. Added responsive font sizing per cell width and label abbreviation when cells are narrow ("Design / Creative" → "Design" on small cells).
- **Year timeline rotated to horizontal (panel 01).** Years now flow top-to-bottom on the Y axis (2009 → 2026), count flows left-to-right. Year labels read cleanly on mobile, no more crowding. Cumulative line dropped (it was redundant with the era panel below). Title updated to "CONEXIONES NUEVAS POR AÑO · 2009 → 2026".
- **Mobile constellation interactive list (panel 06).** New replacement for the simple vertical-list stub. 30 leads as checkbox rows sorted by score. Top 10 pre-active. User can toggle on/off, hard cap at 15 simultaneous active. Mini hub-and-spoke SVG above the list re-renders to show only the active subset. Counter at top ("X / 15 ACTIVOS"), reset button to top-10. Replaces the empty constellation panel mobile users were seeing.
- **Skills cert overlay populated (panel 07).** `DATA.certified_skills` now lists 9 skill names backed by formal certifications: Google Ads (Skillshop, 2023-2024), Strategic Thinking, Strategic Leadership / Leading Strategically, 360-Degree Feedback, Performance Management, Constructive Feedback, Cross-Selling (LinkedIn Learning, 2023 + 2025). Bubbles for these skills get a 2px lime border + ✓ glyph inline with the name. `DATA.certifications_meta` exposes the underlying authority/dates for tooltip context.
- **Skills panel description copy.** Updated to honestly flag what is certified vs endorsement-only. Operator-direct, no marketing.

## 2026-05-08 · Initial release

Initial public release. Six panel refinements shipped before move to git:

- **Treemap (panel 02)**: contrast-aware text fill (luminance threshold 0.5), opacity 1.0 on cells.
- **Warmth signals (panel 04)**: replaced three big-number cards with a 3 × 3 heat table (signal type × ICP alignment), log-scaled color, total column on the right.
- **Constellation (panel 06)**: 820px desktop height, d3.zoom (0.4-4x) with mouse wheel + drag-to-pan, d3.drag on individual nodes, RESET VIEW button.
- **Skills bubbles (panel 07)**: full divergent ramp with the 4 darkest steps skipped, semi-transparent label tag behind every visible name.
- **Leads table (panel 08)**: score heat band on the score cell, sortable headers, era column with color dot, subtle tier-row tint.
- **Method copy (panel "Antes de pedirte algo")**: added the asymmetry frame paragraph upfront, kept the punchy three-line stack, added a closing line.

## Pre-history

Versions before this commit lived as direct Vercel uploads. Repo created 2026-05-08 so the toolkit can ship as a real artifact.
