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
  Once `_data/citations.yml` has `totals.citations` > 0 the band gets two more tiles
  (Citations, h-index; class `home-stats__grid--6`: 6 → 3 → 2 per row) and a source/date
  note. The news list shows each item's first photo as a thumbnail and "N photos / Video /
  LinkedIn post" labels linking to `/news/#news-<slug>`.
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
  (3) a "Cited by N" button (`.pub-cites`) next to DOI from `_data/citations.yml`
  `papers[entry.key]` (hidden when 0/missing; the theme's per-entry Google Scholar badge
  is switched off in `_config.yml`). `max_author_limit` is blank, so every author is shown. `_includes/author_legend.liquid`
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
- Visitor counter (Nov 2026, owner's choice of GoatCounter): `_data/visitor_counter.yml`
  (`goatcounter_code`, `show_on_home_page`, `since`; panel: Home page → Visitor counter;
  the code field also accepts `x.goatcounter.com` or the full URL, normalised by
  `_includes/goatcounter_code.liquid` into `gc_code`). `_includes/footer.liquid` loads
  `https://gc.zgo.at/count.js` with `data-goatcounter="https://<code>.goatcounter.com/count"`
  on every page; `_includes/visitor_counter.liquid` (after the contact band in
  `_layouts/about.liquid`) fetches `https://<code>.goatcounter.com/counter/TOTAL.json`
  (`{"count_unique": "1,234", "count": "1,234"}`, site-wide visitors, CORS `*`, cached ≤ 4 h,
  403 unless the owner's GoatCounter setting "Allow adding visitor counts on your
  website" is on) and only then removes `hidden` (`.visitor-counter[hidden]` keeps it
  hidden, since `.visitor-counter` sets `display: flex`). Empty code → no script, no
  widget. count.js ignores localhost and private networks. goatcounter.com is not
  reachable from the cloud container; its docs and source are at github.com/arp242/goatcounter
  (`tpl/help/visitor-counter.md`, `handlers/vcounter.go`).
- Collaboration map (home page section after Selected publications; switch
  `collaboration_map` in `_pages/about.md`): `_includes/collaboration_map.liquid` + data
  `_data/collaborations.yml` (`home` + `collaborations[]`: `institution`, `place` "City,
  Country", `coordinates` "lat, lon", `people`, `coauthors[]` "Surname, Given" or "Given
  Surname" (no comma → last word is the surname), `period`, `summary`, `link`; panel:
  Collaborations; only `institution` is required; plus top-level
  `show_coauthor_institutions` (default on) and `hidden_institutions[]`). Entries
  without `coordinates` get no marker/line (listed only) until **Place collaborations on
  the map** fills them in. Land = `_includes/world_dots.liquid`, ~3.5k
  dots as one SVG path of `M x y h0` segments with round caps, generated once by
  `bin/make_world_dots.cjs` (Natural Earth 110 m via world-atlas; equirectangular 1000 ×
  391.67, 84°N–57°S; in `.prettierignore`). `_includes/collab_xy.liquid` projects
  coordinates with the same formula (Liquid arithmetic, no JS); markers are absolutely
  positioned `<button>`s in percent (so `.collab-map` must have no padding — it's on
  `.collab-frame`), labels flip side near the edges (`--east/--west`), curved lines are
  quadratic Béziers from home bowing upwards. `_includes/collab_card.liquid` finds joint
  papers with `{% bibliography --query @*[author~=\bSurname\W+G(iven)?\b] --template
collab_paper --group_by year %}` (initial-tolerant regex; `<h2 class="bibliography">`
  years rewritten to `<h4 class="collab-year">`) and links to `/publications/#given
surname` (the bibsearch hash filter). A small inline script shows one card at a time;
  without JS all cards show. Phones: list in 2 columns, smaller markers.
  Automatic layer: `_data/coauthor_network.yml` (bot-written, see workflows) adds
  `institutions[]` (same fields + `openalex`, `papers[]` bib keys) as hollow
  `.collab-pin--auto` markers (z-index 0, no arcs), a `<details>` group "Co-author
  institutions" at the end of the list (spans both columns on phones; the script opens
  it when one of its items is selected) and cards with `auto=true` (joint papers queried
  by `@*[key=…]`, no Publications link). Ids continue after the manual entries
  (`net_first_auto`). An automatic entry is dropped when its name, normalised by
  `_includes/collab_norm.liquid` (lowercase, "&"→"and", no punctuation, no leading "the"),
  equals home's, a manual entry's or one in `hidden_institutions`.
- News: `_includes/news.liquid` (local override of the theme's table; used by
  `_pages/news.md`) lists items newest first with anchors `#news-<slug>`, and
  `_includes/news_media.liquid` renders each item's optional front matter: `images`
  (list of `{src, caption}`, `data-zoomable`), `video_link` (YouTube incl. youtu.be/shorts/
  embed/live → youtube-nocookie; Bilibili BV/av; Vimeo; anything else → "Watch the video"
  button), `video_file` (`<video>`), `linkedin_post` (an "Embed this post" iframe code or
  `/embed/` URL → iframe with the code's height; any other LinkedIn link → "View on
  LinkedIn" button). LinkedIn offers no API for reading a person's posts, so embedding
  per post is the only "link". Liquid variables leak between includes, hence the `nm_`
  resets. "Follow me on LinkedIn" on `/news/` appears when `linkedin_username` is set in
  `_data/socials.yml` (set: liangfu-ge-367697234). Item pages are kept out of the sitemap (`defaults`,
  `type: news`). `_news/*.md` is in `.prettierignore`: the panel saves a pasted embed code
  as `"…\"…"`, which Prettier wants single-quoted.

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
  lives in `_pages/about.md` (`selected_publications`), not in the .bib. The
  "Update publications and citations" workflow also appends papers that are new on the
  Scholar profile (see Workflows); `_data/scholar_sync.yml` remembers handled Scholar ids
  so a paper deleted by hand is not re-added. Every journal
  paper has a `doi` (taken from the owner's CV, Nov 2026); conference papers have none.
- Research: `_projects/*.md`, one per research theme, written only from paper titles;
  `{% cite key %}` + `related_publications: true`. No images yet (`img:` is optional).
- Collaborations: `_data/collaborations.yml`, seeded only from facts in the CV and
  papers.bib (PolyU/Yong Xia, Tongji/Danhui Dan, Western/Ayan Sadhu, Exeter/Brownjohn &
  Koo; Nov 2026). The panel form reuses one field list via a YAML anchor
  (`&collab_fields`); coordinates have a pattern check. Round-trip tested in the panel.
- News: `_news/*.md` (`inline: true`; panel adds a `title` used only for the file name).
  Uploads from the News form go to `assets/news/` (collection `media_folder`); photos are
  converted to WebP ≤ 1800 px on upload (`media_libraries.default.config.transformations`),
  video files are limited to 20 MB (`max_file_size`). Round-trip tested in the panel.
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
  successful deploy), **Update publications and citations**, **Render a CV**, **Prettier**
  (passes if files are formatted: `npm ci && npx prettier --write <files>`). The Prettier
  workflow installs the **latest** `prettier` and `@shopify/prettier-plugin-liquid` on every
  run, and versions disagree on some details (3.8.0 and 3.10.1 want different blank lines
  and Liquid indentation), so keep `devDependencies` at the latest versions before checking.
- **Update publications and citations** (`.github/workflows/citations.yml`; was "Update
  citation counts" until Nov 2026), `bin/update_citations.py` then `bin/update_coauthors.py`:
  Mondays and Thursdays 04:23 UTC, on pushes to main that change `papers.bib`,
  `socials.yml` or either script, manual "Run workflow", and dry runs on PRs that change
  them (`update_citations.py --dry-run --preview-new 2`, `update_coauthors.py --dry-run`;
  print, no commit) (`concurrency` group; `git pull --rebase` before pushing).
  **New papers:** profile papers (`fill(author, sections=[basics, indices, counts,
publications])`) whose title matches no papers.bib entry and whose `author_pub_id` is
  not in `_data/scholar_sync.yml` are filled (`scholarly.fill(pub)`, 60 s SIGALRM limit
  each, ≤ 5 per run), given a DOI/type/full author list from OpenAlex title search when
  it matches, and appended to papers.bib as `@article`/`@inproceedings`/`@incollection`/
  `@misc` with key surname+year+first non-stopword title word (suffix b, c… if taken).
  Every handled id (present or added) goes into scholar_sync.yml, so deleting an entry by
  hand keeps it deleted. `scholarly.fill(pub)` failed on GitHub in Nov 2026
  (`AttributeError: 'NoneType' object has no attribute 'text'`, Scholar's paper page); then
  the entry is built from the OpenAlex title match alone (authors, venue, volume, pages,
  DOI), and a paper neither source knows is retried next run. First live check (24 Nov
  2026): profile 34 papers = papers.bib, 931 citations; OpenAlex 33/34 papers, 18
  co-author institutions (14 shown after removing manual duplicates). **Citations:** First real run
  from GitHub (Nov 2026): Google Scholar answered, 34/34 papers matched. Google Scholar via `scholarly==1.7.11` (needs `httpx<0.28`) for
  profile totals + per-paper counts matched to papers.bib by normalised title (prefix match
  for shortened titles); if Scholar fails or matches nothing, OpenAlex (DOI batches +
  `author.orcid` works; totals computed from matched papers) — except that when Scholar
  fails and citations.yml already holds Google Scholar data ≤ 60 days old
  (`KEEP_SCHOLAR_DAYS`), it is kept and the script exits 0. Writes `_data/citations.yml`
  (`metadata{last_updated,source,source_url}`, `totals{citations,h_index,i10_index}`,
  `papers{<bibkey>: {citations, url}}`, double-quoted, Prettier-clean); if both fail it keeps
  the file and exits 1. It replaces the theme's `update-citations.yml`, which GitHub had
  set to `disabled_inactivity` (a new file name = a new, enabled workflow); the weekly bot
  commit keeps the repo active. Commits pushed with `GITHUB_TOKEN` don't trigger `push`
  workflows, so `deploy.yml` also runs on `workflow_run` of "Render a CV", "Update
  publications and citations" and "Place collaborations on the map" (successful, non-PR
  runs on main) — this also stops the CV PDF lagging one deploy behind.
  **Co-authors** (`bin/update_coauthors.py`, runs even if the first step failed): OpenAlex
  works for papers.bib (DOI batches + `author.orcid` works matched by title) →
  authorships minus the owner (ORCID, or surname in `scholar.last_name` with given name
  equal to a `scholar.first_name` or a single matching initial; "Lei Ge" is not the owner)
  → institutions with their co-authors and paper keys → `geo` via
  `institutions?filter=openalex:I1|I2` (no position → left out) → `_data/coauthor_network.yml`
  (sorted by joint papers; `people` = top 3 + "and N more"; Prettier-clean). OpenAlex
  down → `::warning::`, file kept, exit 0. Not reachable from the cloud container (proxy
  403); test it through the PR dry run.
- **Place collaborations on the map** (`.github/workflows/collaboration-places.yml`,
  `bin/locate_collaborations.py`): on pushes to main that change
  `_data/collaborations.yml`, manually, and as a `--check` test on PRs that change it
  (re-locates every entry and prints the distance to the saved position). For `home` and
  each collaboration without `coordinates` it tries OpenAlex institutions (`geo`; when
  `place` is given, its city, region, country or country code must appear in it —
  `place_matches`: aliases such as USA/UK, typo-tolerant 5-letter word prefixes) then Nominatim
  ("institution, place", then "place"; ≤ 1 request/s, identifying User-Agent), writes
  `coordinates` (and `place` if empty) with ruamel.yaml round-trip (comments, quotes and
  key order kept; `width 4096`, `indent(mapping=2, sequence=4, offset=2)`; output passes
  Prettier), commits "Place collaborations on the map", and `deploy.yml` runs after it via
  `workflow_run`. Never overwrites existing coordinates. Not found → `::warning::` in the
  log, exit 0 (the entry just has no marker).
- **Integration tests** (`unit-tests.yml`) and **Visual regression checks** are al-folio's
  developer checks against removed demo pages; they fail regardless of content. Turning
  their automatic triggers off is the owner's decision (proposed, not done).

## Conventions

- Keep edits simple and well-commented. Don't invent facts about the owner (positions,
  dates, degrees, courses, awards); ask.
- Demo content has been removed — don't reintroduce it (sample projects/news/posts/books,
  people/books/plugins/submenus pages, Einstein data, stock photos, demo media, Disqus).
- Design/plan docs live in `docs/superpowers/` and are excluded from the built site.
