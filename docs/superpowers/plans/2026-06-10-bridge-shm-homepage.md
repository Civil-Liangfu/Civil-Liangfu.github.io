# Bridge SHM Research Homepage — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deploy a customized [al-folio](https://github.com/alshedivat/al-folio) personal homepage for bridge structural health monitoring (SHM), live at `https://civil-liangfu.github.io`, editable entirely through the GitHub web UI.

**Architecture:** Clone al-folio into this folder (already a git repo holding the design docs), strip demo content, customize config + pages with bridge-SHM placeholders, then push to the GitHub user-site repo `Civil-Liangfu.github.io`. al-folio's bundled GitHub Actions workflow builds the Jekyll site on GitHub's servers and publishes to GitHub Pages — no local Ruby/Docker/Node needed.

**Tech Stack:** Jekyll (al-folio theme), GitHub Pages, GitHub Actions, BibTeX (jekyll-scholar), git.

---

## Conventions for this plan

- **OWNER ACTION** marks a step only the site owner (Liangfu) can perform (browser login, repo creation, authorizing a push). Claude pauses and waits at these.
- No local build verification is possible (no Ruby/Docker/Node). Local checks are limited to "file exists / contains expected text." True build verification happens via the GitHub Actions run; final verification is the live URL.
- Commit after each task. Author: `Liangfu Ge <geliangfu@gmail.com>`.
- All commands run from `C:/001LiangfuGe/001Research/Research_Page`.

## File structure (what this plan touches)

- Create (via clone): the full al-folio tree — key files `_config.yml`, `.github/workflows/deploy.yml`, `_pages/*.md`, `_bibliography/papers.bib`, `_projects/`, `_news/`, `_data/`, `assets/`.
- Modify: `_config.yml` (site identity, URL, social).
- Modify: `_pages/about.md` (bio), `_pages/teaching.md` (courses).
- Replace: `_bibliography/papers.bib` (one placeholder paper).
- Replace contents: `_projects/` (one placeholder project), `_news/` (one placeholder item).
- Remove demo: `_posts/` samples, `_data/` sample files, extra demo projects.
- Create: `HOW-TO-UPDATE.md`, `CLAUDE.md`.
- Keep: `docs/superpowers/**` (design + plan), already committed.

---

### Task 1: Scaffold al-folio into the project folder

**Files:**
- Create: entire al-folio tree under `C:/001LiangfuGe/001Research/Research_Page/`
- Keep: existing `docs/` and `.git/`

- [ ] **Step 1: Clone al-folio to a temp directory (shallow)**

```bash
cd "C:/001LiangfuGe/001Research/Research_Page"
git clone --depth 1 https://github.com/alshedivat/al-folio.git /tmp/al-folio
```
Expected: clone completes, `/tmp/al-folio` populated.

- [ ] **Step 2: Delete the upstream `.git`, then copy al-folio files into the project**

```bash
# Remove al-folio's own git history FIRST so it can never overwrite our .git
rm -rf /tmp/al-folio/.git
# Now copy everything (including dotfiles like .github) into our repo
cp -r /tmp/al-folio/. "C:/001LiangfuGe/001Research/Research_Page/"
```
This preserves the existing `C:/001LiangfuGe/001Research/Research_Page/.git` (our spec/plan history) and our `docs/` folder. `cp` only adds al-folio's files alongside them.

- [ ] **Step 3: Inspect the actual structure (confirms exact filenames for later tasks)**

```bash
cd "C:/001LiangfuGe/001Research/Research_Page"
ls -1 _pages/ _projects/ _news/ _data/ _posts/ _bibliography/ 2>/dev/null
echo "--- workflow ---"; ls -1 .github/workflows/
```
Record: confirm `_pages/about.md`, `_pages/teaching.md`, `_pages/cv.md`, `_pages/publications.md`, `_pages/projects.md` exist; note the deploy workflow filename (e.g. `deploy.yml`) and which branch it triggers on, and whether it uses `actions/deploy-pages` (→ Pages Source = GitHub Actions) or pushes a `gh-pages` branch.

- [ ] **Step 4: Verify key files are present**

```bash
test -f _config.yml && echo "config OK"
test -f .github/workflows/deploy.yml && echo "workflow OK"
test -f _pages/about.md && echo "about OK"
test -f _pages/teaching.md && echo "teaching OK"
```
Expected: four "OK" lines (if the workflow filename differs, use the name found in Step 3).

- [ ] **Step 5: Commit the scaffold**

```bash
git add -A
git -c user.name="Liangfu Ge" -c user.email="geliangfu@gmail.com" commit -m "chore: scaffold al-folio template"
```

---

### Task 2: Configure site identity (`_config.yml`)

**Files:**
- Modify: `_config.yml`

- [ ] **Step 1: Set the site/owner fields**

Find each key in `_config.yml` and set these exact values (keys exist in al-folio; replace the value after the colon):

```yaml
title: blank                       # leave navbar brand blank; name shows via first/last
first_name: Liangfu
middle_name:
last_name: Ge
email: geliangfu@gmail.com
description: Personal homepage of Liangfu Ge — research in bridge structural health monitoring (SHM).
keywords: bridge, structural health monitoring, SHM, damage detection, sensors, civil engineering
```

- [ ] **Step 2: Set the deployment URL fields (user site)**

```yaml
url: https://civil-liangfu.github.io
baseurl: ""
```
(`baseurl` MUST be empty string for a `*.github.io` user site, otherwise CSS/links break.)

- [ ] **Step 3: Set social/profile links (placeholders the owner edits later)**

In the social section set:
```yaml
github_username: Civil-Liangfu
```
Leave `scholar_userid`, `orcid_id`, `researchgate`, etc. blank (empty value) so no broken icons appear until the owner fills them.

- [ ] **Step 4: Disable analytics/comments for v1**

Set any of these that exist to false/blank:
```yaml
enable_google_analytics: false
enable_google_analytics_gtag: false
disqus_shortname:
giscus:                            # leave subkeys blank if present
```

- [ ] **Step 5: Verify the edits**

```bash
grep -E "^(url|baseurl|first_name|last_name|email|github_username):" _config.yml
```
Expected: shows `url: https://civil-liangfu.github.io`, `baseurl: ""`, `first_name: Liangfu`, `last_name: Ge`, `email: geliangfu@gmail.com`, `github_username: Civil-Liangfu`.

- [ ] **Step 6: Commit**

```bash
git add _config.yml
git -c user.name="Liangfu Ge" -c user.email="geliangfu@gmail.com" commit -m "feat: configure site identity and deployment URL"
```

---

### Task 3: Customize the About / Home page

**Files:**
- Modify: `_pages/about.md`

- [ ] **Step 1: Replace `_pages/about.md` with bridge-SHM placeholder content**

```markdown
---
layout: about
title: about
permalink: /
subtitle: Researcher in Bridge Structural Health Monitoring

profile:
  align: right
  image: prof_pic.jpg
  image_circular: false
  more_info: >
    <p>Department of Civil Engineering</p>
    <p>Your University</p>
    <p>City, Country</p>

news: true
selected_papers: true
social: true
---

I am a researcher working on **bridge structural health monitoring (SHM)** — using
sensor networks, data-driven methods, and digital twins to detect damage and assess
the condition of bridges throughout their service life.

*(This is placeholder text. Edit `_pages/about.md` on GitHub to add your real bio,
photo (`assets/img/prof_pic.jpg`), and contact details.)*

My research interests include:

- Vibration- and strain-based damage detection
- Wireless sensor networks for civil infrastructure
- Data-driven and physics-informed condition assessment
- Digital twins of bridge structures
```

- [ ] **Step 2: Verify**

```bash
grep -E "permalink: /|Bridge Structural Health Monitoring" _pages/about.md
```
Expected: both lines present.

- [ ] **Step 3: Commit**

```bash
git add _pages/about.md
git -c user.name="Liangfu Ge" -c user.email="geliangfu@gmail.com" commit -m "feat: about page placeholder for bridge SHM"
```

---

### Task 4: Customize the Teaching page

**Files:**
- Modify: `_pages/teaching.md`

- [ ] **Step 1: Replace `_pages/teaching.md` with placeholder content (keep it in the navbar)**

```markdown
---
layout: page
permalink: /teaching/
title: teaching
description: Courses, materials, and student supervision.
nav: true
nav_order: 5
---

*(Placeholder. Edit `_pages/teaching.md` on GitHub to list your real courses.)*

## Courses

- **Structural Health Monitoring** — graduate course. Sensors, signal processing,
  damage detection, and case studies on bridges.
- **Structural Dynamics** — undergraduate/graduate. Vibration theory and applications
  to civil structures.

## Supervision

I supervise students working on bridge SHM topics. Prospective students are welcome
to get in touch.
```

- [ ] **Step 2: Verify it is set to appear in the navbar**

```bash
grep -E "nav: true|title: teaching" _pages/teaching.md
```
Expected: both lines present.

- [ ] **Step 3: Commit**

```bash
git add _pages/teaching.md
git -c user.name="Liangfu Ge" -c user.email="geliangfu@gmail.com" commit -m "feat: teaching page placeholder"
```

---

### Task 5: Seed Publications with a placeholder

**Files:**
- Replace: `_bibliography/papers.bib`

- [ ] **Step 1: Overwrite `_bibliography/papers.bib` with one placeholder entry**

```bibtex
---
---

@article{ge2026shm,
  title    = {Placeholder: A Data-Driven Approach to Bridge Structural Health Monitoring},
  author   = {Ge, Liangfu},
  journal  = {Journal of Bridge Engineering (placeholder)},
  year     = {2026},
  note     = {Replace this entry by pasting your own BibTeX into _bibliography/papers.bib},
  selected = {true}
}
```
(The leading `---`/`---` block is required by jekyll-scholar — keep it.)

- [ ] **Step 2: Verify**

```bash
grep -E "ge2026shm|selected = \{true\}" _bibliography/papers.bib
```
Expected: both present.

- [ ] **Step 3: Commit**

```bash
git add _bibliography/papers.bib
git -c user.name="Liangfu Ge" -c user.email="geliangfu@gmail.com" commit -m "feat: placeholder publication entry"
```

---

### Task 6: Seed Research / Projects and remove demo projects

**Files:**
- Remove: existing demo files in `_projects/`
- Create: `_projects/1_bridge_shm.md`

- [ ] **Step 1: Remove al-folio's demo projects**

```bash
rm -f _projects/*.md
```

- [ ] **Step 2: Create `_projects/1_bridge_shm.md`**

```markdown
---
layout: page
title: Bridge SHM Sensor Network
description: Placeholder project — wireless monitoring of a highway bridge.
img: assets/img/12.jpg
importance: 1
category: research
---

*(Placeholder project. Copy this file in `_projects/` on GitHub to add more, and put
images in `assets/img/`.)*

A wireless sensor network continuously measures acceleration and strain on a highway
bridge. Data are streamed to a server where damage-detection algorithms flag anomalies
in near real time.

Replace this text with a description of your real project, methods, and results.
```
(`img:` reuses an image al-folio already ships in `assets/img/`. Confirm `assets/img/12.jpg` exists from Task 1 Step 3; if not, point `img:` at any file that does.)

- [ ] **Step 3: Verify**

```bash
ls _projects/ && grep "Bridge SHM Sensor Network" _projects/1_bridge_shm.md
```
Expected: only `1_bridge_shm.md` listed; title line present.

- [ ] **Step 4: Commit**

```bash
git add _projects/
git -c user.name="Liangfu Ge" -c user.email="geliangfu@gmail.com" commit -m "feat: placeholder research project; remove demo projects"
```

---

### Task 7: Clean remaining demo content and hide the blog

**Files:**
- Remove: `_posts/` demo posts; sample files in `_data/`
- Replace: `_news/` with one placeholder
- Modify: blog nav visibility

- [ ] **Step 1: Replace demo news with one placeholder**

```bash
rm -f _news/*.md
```
Create `_news/announcement_1.md`:
```markdown
---
layout: post
date: 2026-06-10 09:00:00-0400
inline: true
related_posts: false
---

New personal homepage is live. *(Placeholder — add news items in `_news/`.)*
```

- [ ] **Step 2: Remove demo blog posts (blog is a non-goal for v1)**

```bash
rm -f _posts/*.md _posts/*.markdown 2>/dev/null; true
```

- [ ] **Step 3: Hide the blog tab from the navbar**

In `_config.yml`, find the blog navbar setting. al-folio shows blog via the `_pages/blog/index.html` front matter `nav: true`. Set it to `nav: false`:
```bash
grep -rn "nav:" _pages/blog/ 2>/dev/null
```
Edit the blog index page's front matter to `nav: false` (file path from the grep above, typically `_pages/blog/index.html`). If no blog index exists, skip.

- [ ] **Step 4: Remove sample data and clean the CV so no demo person renders**

```bash
# Coauthors sample would render fake names on publications — remove it.
rm -f _data/coauthors.yml 2>/dev/null; true
ls _data/                       # see what CV/data files actually exist (cv.yml / cv.json / repositories.yml)
```
Then handle the CV page so it shows a clean placeholder instead of al-folio's demo CV:
- If `_data/cv.yml` exists, open it and **keep its key structure** (so the schema stays valid) but replace the sample values with placeholders — e.g. set the name to `Liangfu Ge`, basics to "Bridge Structural Health Monitoring researcher", and delete all but one example entry per section. (Exact keys come from the file inspected above; do not invent new keys.)
- Also remove demo `_data/repositories.yml` GitHub-user/repo samples if present: `rm -f _data/repositories.yml 2>/dev/null; true`.
- Leave `_pages/cv.md` in the navbar; it will now render the trimmed placeholder CV.

- [ ] **Step 5: Verify**

```bash
ls _news/; echo "--- posts ---"; ls _posts/ 2>/dev/null | head
```
Expected: `_news/` has only `announcement_1.md`; `_posts/` is empty or absent.

- [ ] **Step 6: Commit**

```bash
git add -A
git -c user.name="Liangfu Ge" -c user.email="geliangfu@gmail.com" commit -m "chore: remove demo content; hide blog tab"
```

---

### Task 8: Write the owner guide and CLAUDE.md

**Files:**
- Create: `HOW-TO-UPDATE.md`
- Create: `CLAUDE.md`

- [ ] **Step 1: Create `HOW-TO-UPDATE.md`**

```markdown
# How to update my website

My site is live at **https://civil-liangfu.github.io** and is built automatically
by GitHub. **I never need to install anything** — I just edit text files on
github.com and the site rebuilds itself in 1–2 minutes.

## Where to edit (all at github.com/Civil-Liangfu/Civil-Liangfu.github.io)

| I want to… | Edit this file | How |
|------------|----------------|-----|
| Change my bio / photo info | `_pages/about.md` | Edit text; replace photo at `assets/img/prof_pic.jpg` |
| Add a publication | `_bibliography/papers.bib` | Paste the paper's BibTeX entry at the top |
| Add a news item | `_news/` | Click "Add file" → copy the format of `announcement_1.md` |
| Add a project | `_projects/` | Copy `1_bridge_shm.md`, rename, edit; image → `assets/img/` |
| Edit teaching | `_pages/teaching.md` | Edit text |
| Edit my name / links | `_config.yml` | Edit values (e.g. `scholar_userid`, `orcid_id`) |

## The editing loop
1. Open the file on GitHub and click the ✏️ pencil ("Edit this file").
2. Make changes.
3. Scroll down, click **Commit changes**.
4. Wait ~1–2 minutes, then refresh the live site.

## If something looks broken
Go to the repo's **Actions** tab. A red ✗ means the last build failed — click it to
see the error (usually a typo in `_config.yml` or a `.bib` entry). Fix the file and
commit again.
```

- [ ] **Step 2: Create `CLAUDE.md`**

```markdown
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is
A personal academic homepage for Liangfu Ge (bridge structural health monitoring),
built on the **al-folio** Jekyll theme and hosted on **GitHub Pages** at
https://civil-liangfu.github.io (repo: `Civil-Liangfu.github.io`, a GitHub user site).

## Build & deploy
- **No local build is configured** (no Ruby/Docker/Node on the owner's machine).
- Pushing to the default branch triggers `.github/workflows/deploy.yml`, which builds
  the Jekyll site on GitHub's servers and deploys to GitHub Pages.
- To preview locally one would need Jekyll/Docker (see al-folio README) — not set up here.

## Where content lives (edit these, not the theme internals)
- Site identity & links: `_config.yml` (`url` must stay `https://civil-liangfu.github.io`, `baseurl` must stay `""`).
- Home/bio: `_pages/about.md`; profile photo `assets/img/prof_pic.jpg`.
- Publications: `_bibliography/papers.bib` (BibTeX; jekyll-scholar renders it).
- Projects: `_projects/*.md`; images in `assets/img/`.
- Teaching: `_pages/teaching.md`. CV: `_pages/cv.md` (+ `_data/cv.*`). News: `_news/*.md`.
- Navbar visibility is the `nav:`/`nav_order:` front matter on each `_pages/*` file.

## Conventions
- Owner edits primarily via the GitHub web UI; keep changes simple and well-commented.
- Don't set `baseurl` to a non-empty value — it breaks asset paths on a user site.
- Theme upgrades follow al-folio's upstream; avoid editing `_layouts`/`_includes` unless necessary.
```

- [ ] **Step 3: Verify**

```bash
test -f HOW-TO-UPDATE.md && test -f CLAUDE.md && echo "guides OK"
```
Expected: `guides OK`.

- [ ] **Step 4: Commit**

```bash
git add HOW-TO-UPDATE.md CLAUDE.md
git -c user.name="Liangfu Ge" -c user.email="geliangfu@gmail.com" commit -m "docs: add owner update guide and CLAUDE.md"
```

---

### Task 9: Create the GitHub repo and push

**Files:** none (git remote + push)

- [ ] **Step 1: OWNER ACTION — create the empty repo on GitHub**

Owner: at https://github.com/new create a repository named exactly **`Civil-Liangfu.github.io`**, **Public**, and do **NOT** add a README, .gitignore, or license (must be empty so the push isn't rejected). Confirm when done.

- [ ] **Step 2: Set the default branch to `main` and add the remote**

```bash
cd "C:/001LiangfuGe/001Research/Research_Page"
git branch -M main
git remote add origin https://github.com/Civil-Liangfu/Civil-Liangfu.github.io.git
git remote -v
```
Expected: `origin` shows the fetch/push URLs.
NOTE: the branch name MUST match the branch al-folio's `deploy.yml` triggers on (found in Task 1 Step 3). Modern al-folio uses `main`. If the workflow only triggers on `master`, use `git branch -M master` and push that instead.

- [ ] **Step 3: OWNER ACTION — push (first push triggers a browser login)**

```bash
git push -u origin main
```
Git Credential Manager will open a browser window for the owner to sign in to GitHub the first time. Expected: branch pushed, upstream set.

- [ ] **Step 4: Verify the push**

```bash
git ls-remote --heads origin
```
Expected: lists `refs/heads/main`.

---

### Task 10: Enable GitHub Pages and verify the live site

**Files:** none (GitHub settings + verification)

- [ ] **Step 1: OWNER ACTION — set the Pages source**

Owner: repo **Settings → Pages → Build and deployment → Source = "GitHub Actions"**.
(If Task 1 Step 3 found the workflow pushes a `gh-pages` branch instead of using
`actions/deploy-pages`, set Source = "Deploy from a branch" → `gh-pages` / `root`.)

- [ ] **Step 2: Watch the build**

Owner/Claude: open the repo's **Actions** tab. The deploy workflow should be running
from the push in Task 9. Wait for it to finish with a green ✓ (first build ~2–4 min).
If it fails, open the run log, fix the reported file (commonly `_config.yml` YAML or a
`.bib` typo), commit, and the build reruns.

- [ ] **Step 3: Verify the live site responds**

```bash
curl -sSI https://civil-liangfu.github.io | head -1
```
Expected: `HTTP/2 200` (may take a few minutes after the first successful build while DNS/Pages warm up).

- [ ] **Step 4: Verify on-topic content rendered**

```bash
curl -s https://civil-liangfu.github.io | grep -iE "structural health monitoring|Liangfu" | head -1
```
Expected: a matching line, confirming the customized content (not al-folio demo text) is live.

- [ ] **Step 5: Final confirmation**

Confirm in a browser: About, Publications, Research/Projects, Teaching, News, and CV
appear in the navbar; no leftover al-folio demo content; dark/light toggle works.

---

## Definition of done

1. `https://civil-liangfu.github.io` returns HTTP 200 and shows the customized site.
2. About, Publications, Research, Teaching, News, CV pages render; blog hidden.
3. No leftover al-folio demo content (sample projects/news/posts/people removed).
4. `HOW-TO-UPDATE.md` and `CLAUDE.md` present in the repo.
5. Owner can edit a file in the GitHub web UI and see the live site update — no local tools.
