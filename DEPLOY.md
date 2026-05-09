# Deployment runbook

How to push this repo to GitHub and rewire `network.nicoborja.com` on Vercel
to auto-deploy from the new repo. Run from PowerShell on your Windows machine,
not from inside Claude (Claude's sandbox can't write `.git` inside OneDrive).

---

## 0. Cleanup (one-time)

A previous git-init attempt from the sandbox left a broken `.git/` folder
inside this directory. Delete it manually before you start:

```powershell
cd "C:\Users\nicob\OneDrive\Documentos\Claude\Projects\SOUND OS\05_LAB10\network-viz-repo"
Remove-Item -Recurse -Force .git
```

If `Remove-Item` complains about permissions, run PowerShell as Administrator
and retry. Verify the folder is gone with `Test-Path .git` (should print `False`).

---

## 1. Init the repo locally

```powershell
cd "C:\Users\nicob\OneDrive\Documentos\Claude\Projects\SOUND OS\05_LAB10\network-viz-repo"

git init -b main
git config user.email "hola@nicoborja.com"
git config user.name "Nicolas Borja"

git add -A
git status --short
```

Status output should show `A` (added) lines for every file, no `??` (untracked)
and no errors.

---

## 2. First commit

```powershell
git commit -m "feat: initial repo + Day 4 panel refinements

Brings network.nicoborja.com into a versioned, deployable repo.
Six panel refinements shipped:
- Treemap luminance-aware text fill
- Warmth signals 3x3 heat table replaces big-number cards
- Constellation zoom + drag + reset, mobile vertical list
- Skills bubbles full divergent ramp + label tags + cert cross-ref
- Leads table score heat band + sortable headers + era column
- Method copy: asymmetry frame paragraph

Toolkit (parser + template + SKILL.md) ships at toolkit/ for anyone
who wants to generate their own version from a LinkedIn export."
```

---

## 3. Create the GitHub repo

Two paths. Pick one:

### 3a. Via GitHub CLI (fastest, requires `gh` installed and authenticated)

```powershell
gh repo create nicoborja-network --public --source=. --remote=origin --push
```

That single command creates the GitHub repo, sets the remote, and pushes `main`.
You are done with the git side; jump to step 4.

### 3b. Via GitHub web UI (no `gh` required)

1. Open https://github.com/new
2. Repository name: `nicoborja-network`
3. Visibility: Public (recommended — the toolkit is the asset)
4. **Do not** initialize with README, .gitignore, or LICENSE. The local repo
   already has those and a remote init will conflict.
5. Click "Create repository."
6. Copy the URL of the new repo (https://github.com/<your-username>/nicoborja-network.git).
7. Back in PowerShell:

```powershell
git remote add origin https://github.com/<your-username>/nicoborja-network.git
git push -u origin main
```

8. GitHub may prompt for credentials. Use a personal access token (Settings →
   Developer settings → Personal access tokens → Tokens (classic) → Generate
   new token, scopes: `repo`). Paste the token as the password.

---

## 4. Connect Vercel to the new GitHub repo

The site is already live on Vercel (network.nicoborja.com). You are switching
its source from "direct upload" to "auto-deploy from this GitHub repo."

1. Open https://vercel.com/dashboard
2. Find the project that serves `network.nicoborja.com`. Click it.
3. Settings → Git
4. If "Connected Git Repository" shows nothing or shows the wrong repo, click
   "Connect Git Repository" (or "Disconnect" then "Connect").
5. Pick GitHub, authorize Vercel if prompted, select `nicoborja-network`.
6. Branch: `main`. Production branch: `main`.
7. Save.

Vercel will trigger a deploy automatically from the latest `main` commit. Watch
the Deployments tab. First deploy should be green in 30-60 seconds.

---

## 5. Verify production

Open https://network.nicoborja.com in a fresh tab. Check, in this order:

- [ ] Hero, manifesto, timeline render
- [ ] Treemap labels readable on every cell color (panel 02)
- [ ] Warmth signals show as a 3-row heat table, not three big number cards (panel 04)
- [ ] Constellation lets you scroll-to-zoom, drag the background to pan, drag a node to move it (panel 06)
- [ ] RESET VIEW button top-right of constellation panel works
- [ ] Skills bubbles have lime borders on any cert-marked skills (will be empty until parser learns Certifications.csv)
- [ ] Leads table score column is colored (heat band), and SCORE / NOMBRE / ERA headers are clickable to sort (panel 08)
- [ ] "Antes de pedirte algo" copy reads with the new asymmetry-frame paragraph
- [ ] Resize browser to under 720px width: constellation should swap to vertical list

If any of these fail, take a screenshot of the broken panel and the browser
console (F12 → Console tab) and we debug.

---

## 6. Future workflow (after this is set up)

Every time we change `index.html` or anything else in this repo:

```powershell
cd "C:\Users\nicob\OneDrive\Documentos\Claude\Projects\SOUND OS\05_LAB10\network-viz-repo"
git add -A
git commit -m "<short message>"
git push
```

Vercel auto-deploys on push to `main`. No manual upload step ever again.

For risky changes, branch + PR pattern:

```powershell
git checkout -b feat/some-change
# make edits
git add -A && git commit -m "wip"
git push -u origin feat/some-change
# open PR on GitHub, Vercel will create a preview deploy URL automatically
# merge when happy, prod auto-deploys
```

---

## 7. If something is wrong

- Build fails on Vercel: open the deployment, click the failing step, read the
  log. Most common: `vercel.json` syntax error or trying to import a missing
  asset. The repo is static HTML + CSV, so build should be near-instant.
- DNS broke: Vercel "Domains" tab on the project. `network.nicoborja.com`
  should be the primary domain attached. If it disappeared during the
  reconnect, re-add it.
- Site loads but a panel is blank: F12 → Console. Look for `viz <chartName>
  failed:` lines. Each chart is wrapped in a try/catch so a single failure
  does not crash the page.
