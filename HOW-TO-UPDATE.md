# How to update my website

My site is live at **https://civil-liangfu.github.io** and is built automatically by
GitHub. **I never need to install anything.** After I save a change, the site rebuilds
itself in 1–2 minutes.

There are two ways to make changes:

1. **The editing panel** (easiest): simple forms at
   **https://civil-liangfu.github.io/admin/**.
2. **Editing files on github.com** (for anything the panel doesn't cover).

---

## 1. The editing panel

### One-time setup: create a sign-in key (token)

The panel signs in to GitHub with a personal "access token". I only need to do this
once (and again when the token expires).

1. On github.com, click my profile picture (top right) → **Settings**.
2. In the left menu, at the very bottom: **Developer settings** →
   **Personal access tokens** → **Fine-grained tokens** → **Generate new token**.
3. Fill in:
   - **Token name:** `Website editing panel`
   - **Expiration:** pick a date, for example 1 year from now.
   - **Repository access:** _Only select repositories_ → choose
     `Civil-Liangfu/Civil-Liangfu.github.io`.
   - **Permissions → Repository permissions → Contents:** _Read and write_.
4. Click **Generate token** and copy the token (it starts with `github_pat_`).
5. Open **https://civil-liangfu.github.io/admin/**, click
   **Sign In Using Access Token**, and paste the token.

The browser remembers the token, so next time the panel opens straight away. Treat the
token like a password: don't share it or paste it anywhere else. If it ever leaks, delete
it on the same GitHub page and create a new one.

### What I can edit in the panel

| Panel section       | What it changes                                                                            |
| ------------------- | ------------------------------------------------------------------------------------------ |
| **Home page**       | Name line, role, photo, affiliation, short bio, selected papers, section switches, contact |
| **Contact links**   | Email, Google Scholar, ORCID, ResearchGate, LinkedIn, GitHub (buttons on the home page)    |
| **Research topics** | The research cards and pages. **New** adds a topic; “Position” sets the order              |
| **Collaborations**  | The world map of my collaborations on the home page (see “Collaboration map” below)        |
| **News**            | News items, with optional photos, a video and a LinkedIn post (see “News” below)           |
| **Publications**    | The BibTeX list (see “Adding a publication” below), and where I am corresponding author    |
| **CV**              | Experience, education, awards, grants, papers, talks, teaching, mentoring                  |
| **Teaching**        | The Teaching page, and the switches that show it in the menu                               |

Each **Save** is one change on GitHub. Wait 1–2 minutes, then refresh the live site.
Pictures I upload in the panel are stored in `assets/img/`.

Good to know:

- Empty boxes are simply left out, so I can leave optional boxes blank.
- When the panel saves a file, it removes the `#` notes inside that file. That is
  normal and does not affect the website.
- Every paper has a **key**: the word right after `@article{` or `@inproceedings{` in
  its BibTeX entry (e.g. `ge2025deep`). Keys are how the site refers to papers:
  - **Selected publications** on the home page: in **Home page → Selected
    publications**, add one item per paper key. They are shown in that order (drag
    items to reorder). A key that is not in the Publications list is simply skipped.
  - **Corresponding author**: in **Publications → Corresponding author**, add one item
    per paper where I am a corresponding author, and choose **Sole corresponding author**
    or **Co-corresponding author**.
  - On research pages, cite a paper by writing `{% cite key %}` in the page text. The
    cited papers are listed at the bottom of the page automatically.
- In every author list, all authors are shown and my name is bold:
  - **green** when I am the first author (worked out automatically from the order),
  - **orange with a \*** when I am a corresponding author (green with an orange \* if I am
    both). Pointing at my name shows “Corresponding author” or “Co-corresponding
    author”.
- Two home page sections fill themselves in. Each has an on/off switch under **Home
  page** in the panel:
  - **Numbers at a glance** (under my introduction): how many publications, journal
    papers, conference papers and first-author papers I have. They are counted from the
    Publications list, so they update when I paste a new list.
  - **Fellowships & awards**: taken from **Grants and fellowships** and **Awards and
    honours** in the **CV** section. The text before the first comma is shown in bold.
- The **CV** page has a **Download PDF** button. The PDF is made automatically from my
  CV a few minutes after I save a CV change (the “Render a CV” step on GitHub).

### Collaboration map

The home page shows a world map with my institution (orange) and my collaborations (blue),
joined by curved lines. Visitors click a marker, or a name in the list under the map, to
see that collaboration's card. To edit it, open **Collaborations → Collaboration map**:

- **Add Collaboration** adds a marker. Only the **Institution** is needed (e.g. “University
  of Sydney”). A few minutes after saving, GitHub finds where it is (the “Place
  collaborations on the map” step), fills in the city, country and coordinates, and the
  marker appears. Until then the new collaboration is already in the list under the map.
- If the marker lands in the wrong place (two universities with the same name, say), add
  the **City and country**, or set the **Coordinates** myself: on Google Maps, right-click
  the building, click the two numbers at the top of the menu to copy them, and paste them.
  Coordinates I enter are never changed.
- Optional: **People**, **Period**, **Short description**, **Web page**, and **Their names
  in the Publications list** (e.g. “Dan, Danhui”). With the names, the card lists our joint
  papers automatically, and keeps doing so when I paste a new Publications list. Papers
  that shorten the name (“Dan, D”) are found too.
- Drag items to change the order of the list. **My institution** (at the top of the
  form) is where the lines start.
- The section can be switched off under **Home page → Show the collaboration map**.

### News: photos, videos and LinkedIn posts

In **News → New News item**, the text is required; everything else is optional:

- **Photos:** click **Add Photo**, then **Browse** to upload. Big photos are made
  smaller automatically. Visitors can click a photo on the News page to enlarge it.
- **Video link:** a YouTube, Bilibili or Vimeo link. The video plays on the News page.
- **Or upload a short video:** an MP4 file of at most 20 MB. Put longer videos on
  YouTube or Bilibili and use the link instead.
- **LinkedIn post:** LinkedIn does not let other websites read my posts automatically,
  but every public post can be shown on my site:
  1. On LinkedIn, open the post and click the **•••** at its top right.
  2. Choose **Embed this post**, then **Copy code**.
  3. Paste the code into the **LinkedIn post** box.

  A plain link to the post also works; it then shows as a “View on LinkedIn” button.

The home page lists the latest news with a small photo and labels such as “Video” or
“LinkedIn post” that lead to the full item on the News page. Once my LinkedIn address
is filled in under **Contact links → LinkedIn**, the News page also shows a **Follow me
on LinkedIn** button.

### Citation counts (automatic)

Every Monday, and right after I change the Publications list, GitHub fetches my
citation counts from **Google Scholar**. If Google blocks
the request, it uses **OpenAlex**, an open citation database, instead. Each paper then
shows **Cited by N** next to its DOI, and the home page shows my total citations and
h-index with the source and date. Nothing to do on my side.

- To update now: on GitHub, **Actions → Update citation counts → Run workflow**.
- A paper shows no count when it has no citations yet, or when its title in the
  Publications list differs from the title on Google Scholar.

---

## 2. Editing files on github.com

Everything below is done in the browser at
**github.com/Civil-Liangfu/Civil-Liangfu.github.io**.

### Where things live

| I want to…                        | Edit this file                 | Notes                                                                        |
| --------------------------------- | ------------------------------ | ---------------------------------------------------------------------------- |
| Change the home page text         | `_pages/about.md`              | Also in the panel                                                            |
| Change my photo                   | `assets/img/prof_pic.jpg`      | Upload a new image with that exact name (or use the panel)                   |
| Change my links (email, Scholar…) | `_data/socials.yml`            | Also in the panel                                                            |
| Add a publication                 | `_bibliography/papers.bib`     | Also in the panel; see below                                                 |
| Choose the home page's papers     | `_pages/about.md`              | `selected_publications` list of paper keys; also in the panel (Home page)    |
| Edit or add a research topic      | `_projects/`                   | Also in the panel                                                            |
| Add a news item                   | `_news/`                       | Also in the panel                                                            |
| Edit my CV                        | `_data/cv.yml`                 | Also in the panel; templates for new sections are at the bottom              |
| Show my teaching                  | `_pages/teaching.md`           | Also in the panel                                                            |
| Use my own PDF CV instead         | `assets/pdf/` + `_pages/cv.md` | Upload the PDF to `assets/pdf/`, then set `cv_pdf: /assets/pdf/yourfile.pdf` |
| Change colours or fonts           | `_sass/_design.scss`           | All colours and fonts are listed at the top of the file                      |
| Change my name or the footer text | `_config.yml`                  | `first_name` and `footer_text`                                               |
| Change the browser-tab icon       | `_config.yml`                  | `icon:` (now `favicon.png`, a bridge; an emoji such as 🌉 also works)        |
| Start a blog                      | `_pages/blog.md` + `_posts/`   | Add posts to `_posts/`, then set `published: true` and `nav: true`           |

### The editing loop

1. Open the file on GitHub and click the ✏️ pencil ("Edit this file").
2. Make your changes.
3. Scroll down and click **Commit changes**.
4. Wait about 1–2 minutes, then refresh the live site.

### Adding a publication

Paste the BibTeX entry at the top of the list (in the panel: **Publications**; as a file:
`_bibliography/papers.bib`). Google Scholar gives it under **Cite → BibTeX**. Useful extra
lines (each one goes inside the `{ … }` of the entry, with a comma at the end):

- `type_label={Book Chapter},` a different label in front of the paper. Without it, the
  label comes from the entry type: `@article` → **Journal Paper**, `@inproceedings` →
  **Conference Paper**, `@incollection` → **Book Chapter**, `@book` → **Book**,
  `@phdthesis` → **Thesis**, `@misc` → **Preprint**. (This changes only the label,
  not the list the paper is in; see below.)
- `abbr={JBE},` short journal name, shown in small letters under the label
- `doi={10.xxxx/xxxxx},` adds a DOI button (copy the DOI from the paper's web page)
- `pdf={my_paper.pdf},` adds a PDF button (upload the file to `assets/pdf/` first)
- `html={https://…},` adds a link button to any web page

The Publications page has one list per kind of paper, each grouped by year, newest
first. The word after `@` decides the list:

| Entry type                                                | List on the Publications page                   |
| --------------------------------------------------------- | ----------------------------------------------- |
| `@article`                                                | **Journal Papers**                              |
| `@inproceedings` (or `@conference`)                       | **Conference Papers**                           |
| anything else (`@phdthesis`, `@incollection`, `@misc`, …) | **Other Publications** (only shown when needed) |

The buttons at the top of the page jump to each list and show how many papers it has.

To show a new paper on the home page, also add its key under **Home page → Selected
publications** in the panel.

### Avoid these common mistakes (they stop the whole site from updating)

In `.yml` files (`_config.yml`, `_data/socials.yml`, `_data/cv.yml`):

- Put **one space after every colon**: `orcid_id: 0000-…` (not `orcid_id:0000-…`).
- Put **a space before a `#` note** at the end of a line: `name: Ge # note`.
- **Keep the indentation** (the spaces at the start of lines) the same as nearby lines.
- In `_data/socials.yml`, give only the ID or username, **not** the full web address.

The panel avoids all of these mistakes for me.

---

## If something looks broken

Open the repo's **Actions** tab and look at the latest **"Deploy site"** run:

- Green ✓ means the change is live.
- Red ✗ means the build failed. Click it to read the error. It is usually one of the
  mistakes above, in the file I just edited. Fix it, save again, and it rebuilds.

Other workflows I may see in the Actions tab:

- **Render a CV** runs when the CV changes and makes a PDF of it
  (`assets/rendercv/rendercv_output/Liangfu_Ge_CV.pdf`). If it fails, the CV has an entry
  it does not understand; compare it with the templates at the bottom of `_data/cv.yml`.
- **Place collaborations on the map** runs after I save the Collaborations page and
  fills in the position of new entries. A yellow warning in its log means a place was not
  found; add the city and country, or the coordinates.
- **Update citation counts** runs every Monday (see “Citation counts” above). A red ✗
  means neither Google Scholar nor OpenAlex answered that week; the old counts stay on
  the site and the next run tries again.
- **Integration tests** and **Visual regression checks** are the theme developers' own
  checks. They test demo pages that are not part of my site, so a red ✗ on them does
  **not** mean my website is broken.

## Important: don't touch these

- In `_config.yml`, leave `url` and `baseurl` as they are. Changing them breaks the site.
- `admin/config.yml` controls the editing panel. Only change it if I know what I'm doing
  (a mistake there shows an error message in the panel, but does not affect the website).
