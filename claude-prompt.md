# Self-contained Claude Code prompt (paste this into Claude Code on your machine)

You are taking over a deploy task from the Cowork session. The repo is fully
prepped; your job is to push it to GitHub and rewire Vercel.

## Working directory

`C:\Users\nicob\OneDrive\Documentos\Claude\Projects\SOUND OS\05_LAB10\network-viz-repo\`

## Context

- This is a brand new git repo for `network.nicoborja.com`.
- All files are already in place: `index.html`, `leads.csv`, `vercel.json`,
  `README.md`, `LICENSE`, `.gitignore`, `CHANGELOG.md`, `DEPLOY.md`,
  and the `toolkit/` subfolder.
- A previous sandbox attempt left a broken `.git/` folder. **Delete it first.**
- The site is already live on Vercel via direct upload. We are migrating to
  GitHub auto-deploy from this repo.

## Steps

1. Delete the broken `.git/` folder (`Remove-Item -Recurse -Force .git`).
   If permissions block, ask user to run PowerShell as Administrator.
2. `git init -b main` and configure user.email + user.name.
3. `git add -A && git status` to verify staged file list looks right.
4. Single commit with the message in `DEPLOY.md` step 2.
5. Create the GitHub repo. Prefer `gh repo create nicoborja-network --public
   --source=. --remote=origin --push` if `gh` is installed and authenticated.
   Otherwise prompt user to create the repo manually on github.com and provide
   the URL, then `git remote add origin <url>` + `git push -u origin main`.
6. Tell user to open Vercel → project for network.nicoborja.com → Settings →
   Git → Connect to the new GitHub repo → branch `main`. Wait for first
   auto-deploy.
7. Walk user through the 9-checkpoint production verification list in
   `DEPLOY.md` step 5.

## Constraints

- Do not modify `index.html`, `leads.csv`, or any toolkit file. They are the
  shipping content; only commit them as-is.
- Do not create new branches; first commit goes straight to `main`.
- If anything fails (permissions, push rejected, Vercel disconnect refuses),
  surface the exact error to user and stop. Do not retry blindly.
- Brand voice: no em-dashes, no banned terms (impactar, leverage,
  game-changer, disrupting, potenciar, sinergia, "Retainer" capital R).
- Report concisely. No filler.

## When done

Report back:
- GitHub repo URL
- First Vercel deploy status (Ready / Building / Failed)
- Production URL test result (200 / 404 / 5xx)
- Any of the 9 verification checkpoints that did not pass

Net results, sin ruido.
