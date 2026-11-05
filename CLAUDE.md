# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A personal academic homepage for **Liangfu Ge** (bridge structural health
monitoring), built on the **al-folio** Jekyll theme (gem-based, `theme: al_folio_core`,
Tailwind style engine) and hosted on **GitHub Pages** at
https://civil-liangfu.github.io. Repo: `Civil-Liangfu/Civil-Liangfu.github.io`
(a GitHub _user site_). The owner is not a web developer and edits content through the
**editing panel** at `/admin/` (Sveltia CMS) or the GitHub web UI. Owner-facing guide:
`HOW-TO-UPDATE.md` — keep it in sync with any change.

## Build & deploy

- The owner has no local build (git only, no Ruby/Docker/Node).
- Pushing to `main` triggers `.github/workflows/deploy.yml`: `jekyll build`, then
  **PurgeCSS** (`purgecss.config.js`, removes CSS selectors not found in the built
  HTML/JS), then publishes `_site/` to the **`gh-pages` branch**. Pages serves from
  branch `gh-pages` / root (not the "GitHub Actions" source). Live ~1–2 min later.
- **Verifying in a cloud container** (Ruby is usually available):
  `bundle config set --local path vendor/bundle && bundle install`, `pip3 install nbconvert`,
  then `LANG=C.UTF-8 LC_ALL=C.UTF-8 JEKYLL_ENV=production bundle exec jekyll build -d <tmp>`
  (without the UTF-8 locale it crashes with "invalid byte sequence in US-ASCII"), then
  run PurgeCSS (`npx purgecss@8`) on the output to see what CI ships. Google Fonts and
  cdn.jsdelivr.net are usually blocked in the container; for faithful screenshots serve
  the same packages from npm through Playwright request routing.
  `vendor/`, `.bundle`, `.jekyll-cache`, `node_modules/` are git-ignored.

## Design layer (local overrides of theme files)

The look is this site's own; theme files are overridden locally, never edited in the gem.
After upgrading `al_folio_core` / `al_folio_cv`, diff these against the gem versions:

- `assets/css/main.scss` — copy of the theme's file plus `@use "design";` at the end.
- `_sass/_design.scss` — the whole design: tokens at the top (`--c-*` colours for light
  and `html[data-theme="dark"]`, `--font-*` IBM Plex Sans/Serif/Mono), mapped onto the
  theme's `--global-*` variables. Theme rules are often very specific or `!important`
  (e.g. `.publications ol.bibliography li …`, `.cv .card .list-group-item .badge`) —
  match their selectors rather than adding more `!important`.
- `_layouts/about.liquid` — home page (hero, research cards from `site.projects`,
  selected papers, news, contact band). Reads plain front-matter fields in
  `_pages/about.md`: `eyebrow`, `subtitle`, `profile.{image,image_alt,department,institution,location}`,
  `research_heading`, `selected_papers`, `announcements.{enabled,limit}`, `social`,
  `contact_heading`, `contact_note`. Contact buttons are built from `_data/socials.yml`.
- `_layouts/page.liquid` — adds "Research · Theme 0N", `.prose` width and prev/next
  links for `_projects/` pages.
- `_includes/footer.liquid` — cleaner footer (no stray space when `last_name` is empty).
- `_includes/cv/render.liquid`, `_includes/cv/publications.liquid` — local copies of the
  `al_folio_cv` templates (site `_includes` win over the plugin's include path): show
  snake_case section keys as "Title Case" (same rule as RenderCV), and read `journal`.
- Fonts URL: `third_party_libraries.google_fonts.url.fonts` in `_config.yml`.
  `max_width: 1080px`, `footer_fixed: false`.

## Editing panel (`admin/`, Sveltia CMS)

- `admin/index.html` loads Sveltia CMS **pinned** to `@sveltia/cms@0.250.2` from unpkg;
  `admin/config.yml` defines the forms. Backend `github`, `branch: main`,
  `auth_methods: [token]` (fine-grained PAT, Contents read/write; no OAuth server).
  `output.omit_empty_optional_fields: true`.
- Validate config against `schema/sveltia-cms.json` from the npm package, **and** load it
  in a browser: the runtime is stricter than the schema. Learned rules: field `name`s
  must not contain spaces (so CV section keys are snake_case); a required DateTime needs
  `default: "{{now}}"` or new entries can't be saved.
- The panel rewrites files it saves: YAML/front-matter comments are dropped and key order
  follows the config; markdown bodies, `{% cite %}` tags and HTML comments are kept;
  `papers.bib` is a `format: raw` file (saved byte-for-byte). This was round-trip tested
  by running the panel in Playwright with `showDirectoryPicker` stubbed to an OPFS folder
  ("Work with Local Repository"), then building the site from the saved files.
- `/admin/` is excluded from the sitemap (`defaults` in `_config.yml`) and `robots.txt`.

## Where content lives

- Site identity & URL: `_config.yml`. **Do not change** `url: https://civil-liangfu.github.io`
  or `baseurl: ""`. The owner deliberately set `first_name: Liangfu GE` with an empty
  `last_name`; keep it. `scholar.last_name/first_name` (`[Ge]`, `[Liangfu, L.]`) bold the
  owner in author lists. `_config.yml` is NOT in the panel (it would lose its comments).
- Social links: `_data/socials.yml` (jekyll-socials keys; values are IDs, not URLs; the
  ResearchGate key is `research_gate_profile`). The Scholar-citations workflow reads
  `scholar_userid` from here.
- Publications: `_bibliography/papers.bib` (`selected={true}` → home page). No `doi`s yet.
- Research: `_projects/*.md`, one per research theme, written only from paper titles;
  `{% cite key %}` + `related_publications: true`. No images yet (`img:` is optional).
- News: `_news/*.md` (`inline: true`; panel adds a `title` used only for the file name).
- Teaching: `_pages/teaching.md`, hidden (`nav: false`, `sitemap: false`) until the owner
  adds real teaching.
- CV: `_data/cv.yml`, must stay valid for **RenderCV** (`render-cv.yml` makes a PDF on
  every change on `main`) and render on `/cv/`. Rules: no `label/summary/address/image`
  under `cv:`; entry extra fields only as strings; multi-word section keys in snake_case
  (`current_position`, `research_interests`, `methods_and_tools`, `awards_and_honours`);
  sections titled `Skills`, `Awards`, `Interests`, … switch the website to other
  templates, so avoid those exact titles. Education/Experience details are unknown.
- Navbar: `nav:` / `nav_order:` front matter in `_pages/*`. Current: about · publications(1)
  · research(2) · news(4) · CV(5). Teaching(3), blog and repositories are `nav: false`.

## Workflows (GitHub Actions)

- Matter for the site: **Deploy site**, **Check for broken links on site** (after a
  successful deploy), **Update Google Scholar Citations**, **Render a CV**, **Prettier**
  (passes if files are formatted: `npm ci && npx prettier --write <files>`).
- **Integration tests** (`unit-tests.yml`) and **Visual regression checks** are al-folio's
  developer checks against removed demo pages; they fail regardless of content. Turning
  their automatic triggers off is the owner's decision (proposed, not done).

## Conventions

- Keep edits simple and well-commented. Don't invent facts about the owner (positions,
  dates, degrees, courses, awards); ask.
- Demo content has been removed — don't reintroduce it (sample projects/news/posts/books,
  people/books/plugins/submenus pages, Einstein data, stock photos, demo media, Disqus).
- Design/plan docs live in `docs/superpowers/` and are excluded from the built site.
