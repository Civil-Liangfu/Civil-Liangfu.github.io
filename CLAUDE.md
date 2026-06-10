# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is
A personal academic homepage for **Liangfu Ge** (bridge structural health
monitoring), built on the **al-folio** Jekyll theme (gem-based, `theme: al_folio_core`,
Tailwind style engine) and hosted on **GitHub Pages** at
https://civil-liangfu.github.io. Repo: `Civil-Liangfu/Civil-Liangfu.github.io`
(a GitHub *user site*). The owner edits content primarily through the GitHub web UI.

## Build & deploy
- **No local build is configured** (the owner has git but no Ruby/Docker/Node).
- Pushing to the `main` branch triggers `.github/workflows/deploy.yml`, which builds
  the Jekyll site on GitHub's servers and publishes the built `_site/` to the
  **`gh-pages` branch** via `JamesIves/github-pages-deploy-action`.
- GitHub Pages must therefore serve from **branch `gh-pages` / root** (Settings →
  Pages → Deploy from a branch). This is NOT the "GitHub Actions" Pages source.
- Live site updates ~1–2 min after the Action finishes. To preview locally one would
  need Jekyll/Docker (see al-folio's `docs/INSTALL.md`) — intentionally not set up here.

## Where content lives (edit these, not the theme internals)
- Site identity & URL: `_config.yml`. **Do not change** `url: https://civil-liangfu.github.io`
  or `baseurl: ""` — a non-empty baseurl breaks all asset paths on a user site.
- Home / bio: `_pages/about.md`; profile photo `assets/img/prof_pic.jpg`.
- Social links (email, GitHub, Scholar, ORCID…): `_data/socials.yml` (jekyll-socials).
- Publications: `_bibliography/papers.bib` (BibTeX; jekyll-scholar renders it; mark
  `selected={true}` to feature a paper on the home page).
- Research projects: `_projects/*.md`; images in `assets/img/`.
- Teaching: `_pages/teaching.md` (plain markdown — the demo calendar/collection
  includes were intentionally removed for easy editing).
- CV: data in `_data/cv.yml` (rendercv format); page settings in `_pages/cv.md`.
- News: `_news/*.md` (shown on the home page and the News page).
- Navbar membership/order: the `nav:` / `nav_order:` front matter on each `_pages/*`
  file. Current navbar: about (home) · publications(1) · research(2) · teaching(3) ·
  news(4) · CV(5). Blog, repositories, people, and submenus are set `nav: false`.

## Conventions
- Keep edits simple and well-commented; the owner is not a web developer.
- Demo content (sample projects/news/posts/books/teachings/people, Einstein CV/bib,
  external blog feeds, Disqus) has been removed — don't reintroduce it.
- Design/plan docs live in `docs/superpowers/` and are excluded from the built site.
- Avoid editing theme internals (the `al_folio_core` gem provides layouts/includes).
