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

| Panel section       | What it changes                                                                         |
| ------------------- | --------------------------------------------------------------------------------------- |
| **Home page**       | Name line, role, photo, department/university/city, short bio, contact text             |
| **Contact links**   | Email, Google Scholar, ORCID, ResearchGate, LinkedIn, GitHub (buttons on the home page) |
| **Research topics** | The research cards and pages. **New** adds a topic; “Position” sets the order           |
| **News**            | News items. **New** adds one (the date is filled in with today)                         |
| **Publications**    | The BibTeX list (see “Adding a publication” below)                                      |
| **CV**              | Position, experience, education, awards, interests, methods, selected papers            |
| **Teaching**        | The Teaching page, and the switches that show it in the menu                            |

Each **Save** is one change on GitHub. Wait 1–2 minutes, then refresh the live site.
Pictures I upload in the panel are stored in `assets/img/`.

Good to know:

- Empty boxes are simply left out, so I can leave optional boxes blank.
- When the panel saves a file, it removes the `#` notes inside that file. That is
  normal and does not affect the website.
- On research pages, cite a paper by writing `{% cite key %}` in the page text, where
  `key` is the first word of the paper's BibTeX entry (e.g. `ge2020accurate`). The cited
  papers are listed at the bottom of the page automatically.

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
| Add or feature a publication      | `_bibliography/papers.bib`     | Also in the panel; see below                                                 |
| Edit or add a research topic      | `_projects/`                   | Also in the panel                                                            |
| Add a news item                   | `_news/`                       | Also in the panel                                                            |
| Edit my CV                        | `_data/cv.yml`                 | Also in the panel; templates for new sections are at the bottom              |
| Show my teaching                  | `_pages/teaching.md`           | Also in the panel                                                            |
| Use my own PDF CV                 | `assets/pdf/` + `_pages/cv.md` | Upload the PDF to `assets/pdf/`, then set `cv_pdf: /assets/pdf/yourfile.pdf` |
| Change colours or fonts           | `_sass/_design.scss`           | All colours and fonts are listed at the top of the file                      |
| Change my name or the footer text | `_config.yml`                  | `first_name` and `footer_text`                                               |

### The editing loop

1. Open the file on GitHub and click the ✏️ pencil ("Edit this file").
2. Make your changes.
3. Scroll down and click **Commit changes**.
4. Wait about 1–2 minutes, then refresh the live site.

### Adding a publication

Paste the BibTeX entry at the top of the list (in the panel: **Publications**; as a file:
`_bibliography/papers.bib`). Google Scholar gives it under **Cite → BibTeX**. Useful extra
lines (each one goes inside the `{ … }` of the entry, with a comma at the end):

- `abbr={JBE},` short journal name shown as a label
- `selected={true},` also show the paper on the home page
- `doi={10.xxxx/xxxxx},` adds a DOI button and citation badges (copy the DOI from
  the paper's web page)
- `pdf={my_paper.pdf},` adds a PDF button (upload the file to `assets/pdf/` first)
- `html={https://…},` adds a link button to any web page

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
- **Update Google Scholar Citations** runs three times a week. It sometimes fails because
  Google blocks it. That is harmless.
- **Integration tests** and **Visual regression checks** are the theme developers' own
  checks. They test demo pages that are not part of my site, so a red ✗ on them does
  **not** mean my website is broken.

## Important: don't touch these

- In `_config.yml`, leave `url` and `baseurl` as they are. Changing them breaks the site.
- `admin/config.yml` controls the editing panel. Only change it if I know what I'm doing
  (a mistake there shows an error message in the panel, but does not affect the website).
