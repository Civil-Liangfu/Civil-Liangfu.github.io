# Bridge SHM Research Homepage — Design Spec

**Date:** 2026-06-10
**Owner:** Liangfu Ge (geliangfu@gmail.com)
**Status:** Approved

## Inputs (provided)

- **GitHub username:** `Civil-Liangfu`
- **Repository / live URL:** `Civil-Liangfu.github.io` → `https://civil-liangfu.github.io`
- **Initial content:** placeholders, to be edited later via the GitHub web UI

## Goal

A high-tech-looking personal research homepage focused on **bridge structural
health monitoring (SHM)**, hosted on the public internet for free, that the
owner can update easily **entirely through the GitHub website** (no local
software required).

## Decisions (locked)

- **Template:** [al-folio](https://github.com/alshedivat/al-folio) — modern,
  clean, responsive Jekyll theme for academics (~14.7k stars). Chosen over
  academicpages for its more contemporary "high-tech" aesthetic, dark mode,
  math/code rendering, and BibTeX-driven publications.
- **Host:** GitHub Pages, free, HTTPS.
- **Primary edit method:** the GitHub web editor (browser only). Local editing
  is not required; the owner has git but no Ruby/Docker/Node.
- **Build:** al-folio's bundled GitHub Actions workflow builds the Jekyll site
  on GitHub's servers and deploys it. No local build toolchain needed.

## Architecture

```
Owner edits text files in the GitHub web UI
        │  (commit)
        ▼
GitHub repo  <username>.github.io
        │  (push triggers Actions)
        ▼
GitHub Actions: build Jekyll (al-folio)
        │  (deploy)
        ▼
GitHub Pages  →  https://<username>.github.io   (live in ~1–2 min)
```

- Repository name: `Civil-Liangfu.github.io` (a GitHub *user site*).
- Live URL: `https://civil-liangfu.github.io` (GitHub serves the host in lower
  case; the repo name keeps the original casing).
- Initial content: **placeholders** the owner edits later via the web UI.
- GitHub Pages "Source" must be set to **GitHub Actions** (not "Deploy from a
  branch"), which is how al-folio's workflow publishes.

## Site structure (pages)

| Page | Source file(s) | Purpose |
|------|----------------|---------|
| Home / About | `_pages/about.md`, `_config.yml` | Photo, short bio, research focus (bridge SHM), affiliation, profile links (Google Scholar, ORCID, GitHub, email). |
| Publications | `_bibliography/papers.bib` | Auto-generated list; add a paper by pasting its BibTeX entry. |
| Research / Projects | `_projects/*.md` + images in `assets/img/` | Cards for SHM projects (e.g. sensor networks, damage detection, digital twins). |
| Teaching | `_pages/teaching.md` | Courses taught, materials, supervision. |
| News | `_news/*.md` | Short dated updates (new paper, award, talk). |
| CV | `_pages/cv.md` + `assets/pdf/` | PDF link and/or structured entries. |

Demo content shipped with al-folio (sample posts, unrelated projects, example
people/profile) will be removed so the site starts clean and on-topic.

## Update workflow (the "easy to update" requirement)

All actions are performed in the browser at `github.com/<username>/<username>.github.io`:

- **Add a publication:** open `_bibliography/papers.bib`, paste the BibTeX
  entry, commit.
- **Add a news item:** create a small file in `_news/` (copy an existing one).
- **Add a project:** copy an existing file in `_projects/`, edit text, drop an
  image into `assets/img/`.
- **Edit bio / site title / links:** edit `_pages/about.md` and `_config.yml`.

After each commit, GitHub Actions rebuilds and the live site updates in
~1–2 minutes. A plain-English `HOW-TO-UPDATE.md` guide will be written for the
owner, plus a `CLAUDE.md` documenting build/deploy and content locations.

## Division of labor

- **Claude (this project):** clone al-folio, customize `_config.yml`, pages,
  and theme settings for bridge SHM; remove demo content; add the Teaching
  page; confirm the GitHub Actions deploy workflow is present and correct; write
  `HOW-TO-UPDATE.md` and `CLAUDE.md`.
- **Owner:** provide GitHub username; create the empty `<username>.github.io`
  repo (or install GitHub CLI so Claude can create it); authorize the first
  `git push` (Git Credential Manager browser prompt); enable Pages → Source =
  GitHub Actions; supply basics (name, affiliation, photo, a few papers) — or
  accept placeholders to edit later via the web UI.

## Non-goals (YAGNI)

- No custom domain in v1 (can be added later via repo Settings → Pages).
- No local Jekyll/Ruby/Docker setup; no local preview server.
- No blog/posts section, no analytics, no comments in v1.

## Success criteria

1. `https://<username>.github.io` loads a clean, on-topic al-folio site (no
   leftover demo content).
2. About, Publications, Research, Teaching, News, and CV pages render.
3. Owner can add a publication and a news item via the GitHub web editor and see
   the live site update without touching a local machine.
4. `HOW-TO-UPDATE.md` and `CLAUDE.md` are present in the repo.
```