# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A personal academic homepage for **Liangfu Ge** (bridge structural health
monitoring), built on the **al-folio** Jekyll theme (gem-based, `theme: al_folio_core`,
Tailwind style engine) and hosted on **GitHub Pages** at
https://civil-liangfu.github.io. Repo: `Civil-Liangfu/Civil-Liangfu.github.io`
(a GitHub _user site_). The owner edits content primarily through the GitHub web UI.

## Build & deploy

- The owner has no local build (git only, no Ruby/Docker/Node).
- Pushing to the `main` branch triggers `.github/workflows/deploy.yml`, which builds
  the Jekyll site on GitHub's servers and publishes the built `_site/` to the
  **`gh-pages` branch** via `JamesIves/github-pages-deploy-action`.
- GitHub Pages must therefore serve from **branch `gh-pages` / root** (Settings →
  Pages → Deploy from a branch). This is NOT the "GitHub Actions" Pages source.
- Live site updates ~1–2 min after the Action finishes.
- **Verifying a change in a cloud container** (Ruby is usually available there):
  `bundle config set --local path vendor/bundle && bundle install`, then
  `pip3 install nbconvert` and
  `LANG=C.UTF-8 LC_ALL=C.UTF-8 JEKYLL_ENV=production bundle exec jekyll build -d <tmpdir>`.
  Without the UTF-8 locale the build crashes with "invalid byte sequence in US-ASCII".
  `vendor/`, `.bundle`, `.jekyll-cache`, `node_modules/` are git-ignored.

## Where content lives (edit these, not the theme internals)

- Site identity & URL: `_config.yml`. **Do not change** `url: https://civil-liangfu.github.io`
  or `baseurl: ""` — a non-empty baseurl breaks all asset paths on a user site.
  The owner deliberately set `first_name: Liangfu GE` with an empty `last_name`; keep it.
  `scholar.last_name/first_name` (`[Ge]`, `[Liangfu, L.]`) control bolding of the owner
  in author lists.
- Home / bio: `_pages/about.md` (the owner's own text); profile photo `assets/img/prof_pic.jpg`.
  The four research interests link to the four `_projects/` pages.
- Social links: `_data/socials.yml` (jekyll-socials). Values are IDs/usernames, not URLs
  (the plugin prepends the URL). A YAML error here breaks the build AND the
  Scholar-citations workflow (which reads `scholar_userid` from this file).
- Publications: `_bibliography/papers.bib` (jekyll-scholar; `selected={true}` features a
  paper on the home page). Entries currently have no `doi` fields.
- Research: `_projects/1_traffic_load_identification.md`, `2_damage_detection.md`,
  `3_robotics_inspection.md`, `4_digital_twins.md` — one page per research theme,
  written only from the paper titles in `papers.bib`; each uses `{% cite key %}` +
  `related_publications: true` to list its papers. No images yet (the al-folio stock
  photos were unrelated and have been deleted) — use real figures from the owner if added.
- Teaching: `_pages/teaching.md` is hidden (`nav: false`, `sitemap: false`) because the
  owner's real teaching is unknown; examples sit in an HTML comment.
- CV: `_data/cv.yml`; page settings in `_pages/cv.md`. **This file must stay valid for
  RenderCV** (`render-cv.yml` renders it to a PDF on every change on `main`) **and** render
  on the al-folio CV page. Rules learned by testing with RenderCV v2.8:
  no `label`/`summary`/`address`/`image` under `cv:` (RenderCV rejects them); extra fields on
  entries are allowed only as strings (a list-valued extra field crashes the renderer);
  use `- bullet:` or `- label:/details:` entries in sections whose titles are NOT
  `Skills`, `Awards`, `Interests`, … (those titles switch the website to templates
  that expect other fields). Publications carry both `journal` (PDF) and `publisher` (web).
  Education/Experience details are unknown — templates are at the bottom of the file.
- News: `_news/*.md` (shown on the home page and the News page).
- Navbar membership/order: the `nav:` / `nav_order:` front matter on each `_pages/*`
  file. Current navbar: about (home) · publications(1) · research(2) · news(4) · CV(5).
  Teaching(3), blog and repositories are `nav: false`.

## Workflows (GitHub Actions)

- Matter for the site: **Deploy site**, **Check for broken links on site** (runs after a
  successful deploy), **Update Google Scholar Citations** (writes `_data/citations.yml`),
  **Render a CV**.
- **Integration tests** (`unit-tests.yml`), **Visual regression checks** and **Prettier**
  are al-folio's developer checks. The first two test demo blog posts/pages that were
  removed, so they fail on this site regardless of content. Turning their automatic
  triggers off is the owner's decision (it was proposed but not done).
- Prettier passes if changed files are formatted: run `npx prettier --write <files>`
  (after `npm ci`) before committing.

## Conventions

- Keep edits simple and well-commented; the owner is not a web developer. Owner-facing
  guide: `HOW-TO-UPDATE.md` (keep it in sync with changes).
- Demo content has been removed — don't reintroduce it: sample projects/news/posts/
  books/teachings, the people/books/plugins/submenus pages, Einstein CV/bib/citations/
  photo/resume.json, stock photos, demo audio/video/plotly/jupyter files, external blog
  feeds, Disqus.
- Don't invent facts about the owner (positions, dates, degrees, courses, awards); ask.
- Design/plan docs live in `docs/superpowers/` and are excluded from the built site.
- Avoid editing theme internals (the `al_folio_core` gem provides layouts/includes).
