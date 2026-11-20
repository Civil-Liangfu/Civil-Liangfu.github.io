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
- `_layouts/about.liquid` — home page (hero, numbers at a glance, research cards,
  selected papers, fellowships & awards, news, contact band). Reads plain front-matter
  fields in `_pages/about.md`: `eyebrow`, `subtitle`, `profile.{image,image_alt,department,institution,location}`,
  `highlights`, `research_heading`, `selected_papers`, `selected_publications`, `recognition`,
  `announcements.{enabled,limit}`, `social`, `contact_heading`, `contact_note` (`highlights` and
  `recognition` are on unless `false`). Contact buttons are built from `_data/socials.yml`.
  Numbers at a glance: `bibliography_count` (all / `@article` / conference types / first
  author via `@*[author~=^{{ owner_last }}\W+{{ owner_initial }}]`, which assumes Scholar's
  "Last, First" author format). Fellowships & awards: `site.data.cv.cv.sections`
  `grants_and_fellowships` + `awards_and_honours` (text before the first ", " in bold).
  Research cards: `_includes/theme_cards.liquid`, shared with `_pages/projects.md`.
  Selected papers: `selected_publications` is an ordered list of BibTeX keys, rendered with
  `{% nocite paper_key %}` in a loop (output captured, so a missing key's "(missing
  reference)" text never shows) + `{% bibliography --group_by none --cited_in_order %}`.
  If the list is empty it falls back to `selected={true}` entries; the section is hidden
  when nothing renders. Section numbers (01, 02, …) are counted, not hard-coded.
- `_layouts/bib.liquid` — local copy of the theme's publication entry template. Adds
  (1) a type label at the top of the left column ("Journal Paper" for `@article`,
  "Conference Paper" for `@inproceedings`/`@conference`, "Book Chapter", "Book",
  "Thesis", "Report", "Preprint"), overridable per entry with `type_label={…}` (listed in
  `filtered_bibtex_keywords`); classes `.pub-type--journal|conference|other`; and
  (2) owner-name roles: the owner's `<em>` gets `author-self--first` (green, first in
  the author list) or `author-self--corresponding` (orange) plus a `<sup class="author-corr">*</sup>`
  and a hidden `.sr-only` "(corresponding author)" / "(co-corresponding author)" for screen
  readers, the same text as a hover tooltip on the name (the visible `.pub-role` line under
  the type label was removed at the owner's request, Nov 2026), when the
  entry's key is in `_data/corresponding.yml` (`papers: [{key, role: sole|co}]`, edited
  in the panel under Publications → Corresponding author; kept out of the .bib so a
  Google Scholar re-paste can't wipe it). First author wins the colour when both apply.
  `max_author_limit` is blank, so every author is shown. `_includes/author_legend.liquid`
  is the colour key above the Publications page and the home page's selected papers (its
  "corresponding" item appears only when the list is non-empty). `--c-green` token:
  #15803d light / #5fd18b dark.
- `_pages/publications.md` + `_includes/publication_section.liquid` — the Publications
  page is split by BibTeX type into **Journal Papers** (`@article`), **Conference Papers**
  (`@inproceedings, @conference, @proceedings`) and **Other Publications** (an explicit
  list of every other type, so a thesis/preprint from a Scholar paste never vanishes;
  bibtex-ruby query conditions can't test the entry type, so no "not article" query).
  Each is `{% bibliography --query {{ types }} %}` (comma = OR; jekyll-scholar
  interpolates `{{ var }}` in queries), still grouped by year, counted with
  `bibliography_count`, and skipped when empty. `type_label` changes the label only, not
  the subsection. A pill row (`.pub-jump`) links to each subsection. Gotchas: the
  theme's `bibsearch.js` reads the URL hash as a search term, so the jump links scroll
  with `scrollIntoView` and `preventDefault` (a plain `#conference-papers` link filters
  everything out); year headings must stay `h2.bibliography` and each subsection must be
  its own `<section>` so the search's sibling walk stays inside it; a CSS `:has()` rule
  hides a subsection whose papers are all `.unloaded`; the theme's `.publications h2 span`
  (1.5rem) is beaten by `.publications h2 .pub-section__count`.
- `_layouts/page.liquid` — adds "Research · Theme 0N", `.prose` width and prev/next
  links for `_projects/` pages; other pages get `<article class="page-text">` (spaced
  `h2`s, ruled list rows; used by Teaching).
- `_includes/footer.liquid` — cleaner footer (no stray space when `last_name` is empty).
- `_includes/cv/render.liquid`, `_includes/cv/publications.liquid` — local copies of the
  `al_folio_cv` templates (site `_includes` win over the plugin's include path): show
  snake_case section keys as "Title Case" (same rule as RenderCV), read `journal`, and
  show `cv_pdf` as a "Download PDF" button. `_pages/cv.md` points `cv_pdf` at the
  RenderCV output `assets/rendercv/rendercv_output/Liangfu_Ge_CV.pdf` (file name comes
  from `cv.name`; update `cv_pdf` if that name changes).
- Fonts URL: `third_party_libraries.google_fonts.url.fonts` in `_config.yml`.
  `max_width: 1080px`, `footer_fixed: false`, `last_updated: true` (build date in the
  footer), `enable_math: false` (no page uses formulas). Favicon: `icon: favicon.png`,
  rendered at 192 px from `assets/img/favicon.svg` (arch bridge in the site colours) with
  Playwright; re-render the PNG after editing the SVG.
- `_pages/404.md` — no auto-redirect; buttons to Home / Publications / Research / CV.

## Editing panel (`admin/`, Sveltia CMS)

- `admin/index.html` loads Sveltia CMS **pinned** to `@sveltia/cms@0.250.2` from unpkg;
  `admin/config.yml` defines the forms. Backend `github`, `branch: main`,
  `auth_methods: [token]` (fine-grained PAT, Contents read/write; no OAuth server).
  `output.omit_empty_optional_fields: true`, `output.yaml.quote: double` (with the default,
  the panel single-quotes strings that need quotes, e.g. ones with a colon, and every such
  save failed the Prettier check).
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
  `last_name`; keep it. `scholar.last_name/first_name` (`[Ge]`, `[Liangfu, L., L]`) mark the
  owner in author lists (Google Scholar exports sometimes write "Ge, L"). `_config.yml` is NOT in the panel (it would lose its comments).
- Social links: `_data/socials.yml` (jekyll-socials keys; values are IDs, not URLs; the
  ResearchGate key is `research_gate_profile`). The Scholar-citations workflow reads
  `scholar_userid` from here.
- Publications: `_bibliography/papers.bib`. The owner replaces it wholesale from Google
  Scholar exports, which carry no `selected`/`abbr` fields, so the home page selection
  lives in `_pages/about.md` (`selected_publications`), not in the .bib. Every journal
  paper has a `doi` (taken from the owner's CV, Nov 2026); conference papers have none.
- Research: `_projects/*.md`, one per research theme, written only from paper titles;
  `{% cite key %}` + `related_publications: true`. No images yet (`img:` is optional).
- News: `_news/*.md` (`inline: true`; panel adds a `title` used only for the file name).
- Teaching: `_pages/teaching.md`, in the menu (`nav: true`, `sitemap: true`): courses and
  student supervision from the owner's CV.
- CV: `_data/cv.yml`, must stay valid for **RenderCV** (`render-cv.yml` makes a PDF on
  every change on `main`) and render on `/cv/`. Rules: no `label/summary/address/image`
  under `cv:`; entry extra fields only as strings; multi-word section keys in snake case
  (`current_position`, `research_interests`, `methods_and_tools`, `awards_and_honours`,
  `grants_and_fellowships`, `conference_presentations`); single-word keys are capitalised
  (`Experience`, `Education`, `Publications`, `Teaching`, `Mentoring`), because the website
  shows a key with no underscore exactly as written. Sections titled `Skills`, `Awards`,
  `Interests`, … switch the website to other templates, so avoid those exact titles. Apart
  from Experience, Education and Publications, `/cv/` only renders `bullet` entries and
  `label`/`details` entries (details as plain text), so new sections must use one of
  those. Section order follows the field order in `admin/config.yml` (the panel rewrites
  it). Content filled in from the owner's CV (Nov 2026); `current_position` was dropped
  because it repeated Experience.
- Navbar: `nav:` / `nav_order:` front matter in `_pages/*`. Current: about · publications(1)
  · research(2) · teaching(3) · news(4) · CV(5). Blog (no posts) and repositories (only
  template text) are `published: false`, so they are not built or in the sitemap.
- Not published: `test/` (theme developer tests) and `requirements.txt` are in `exclude:`.

## Workflows (GitHub Actions)

- Matter for the site: **Deploy site**, **Check for broken links on site** (after a
  successful deploy), **Update Google Scholar Citations** (runs "succeed" but
  `_data/citations.yml` has stayed empty, and the last scheduled run was Aug 2026, so the
  site shows no citation counts), **Render a CV**, **Prettier**
  (passes if files are formatted: `npm ci && npx prettier --write <files>`). The Prettier
  workflow installs the **latest** `prettier` and `@shopify/prettier-plugin-liquid` on every
  run, and versions disagree on some details (3.8.0 and 3.10.1 want different blank lines
  and Liquid indentation), so keep `devDependencies` at the latest versions before checking.
- **Integration tests** (`unit-tests.yml`) and **Visual regression checks** are al-folio's
  developer checks against removed demo pages; they fail regardless of content. Turning
  their automatic triggers off is the owner's decision (proposed, not done).

## Conventions

- Keep edits simple and well-commented. Don't invent facts about the owner (positions,
  dates, degrees, courses, awards); ask.
- Demo content has been removed — don't reintroduce it (sample projects/news/posts/books,
  people/books/plugins/submenus pages, Einstein data, stock photos, demo media, Disqus).
- Design/plan docs live in `docs/superpowers/` and are excluded from the built site.
