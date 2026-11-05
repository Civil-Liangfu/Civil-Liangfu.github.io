# How to update my website

My site is live at **https://civil-liangfu.github.io** and is built automatically by
GitHub. **I never need to install anything.** I just edit text files on github.com, and
the site rebuilds itself in 1–2 minutes.

Everything below is done in the browser at
**github.com/Civil-Liangfu/Civil-Liangfu.github.io**.

## Where to edit

| I want to…                        | Edit this file                 | How                                                                                      |
| --------------------------------- | ------------------------------ | ---------------------------------------------------------------------------------------- |
| Change my bio                     | `_pages/about.md`              | Edit the text                                                                            |
| Change my photo                   | `assets/img/prof_pic.jpg`      | Upload a new image with that exact name                                                  |
| Change my affiliation/address     | `_pages/about.md`              | Edit the `more_info` lines near the top                                                  |
| Change my links (email, Scholar…) | `_data/socials.yml`            | Follow the notes at the top of the file                                                  |
| Add a publication                 | `_bibliography/papers.bib`     | Paste the paper's BibTeX entry at the top (see below)                                    |
| Feature a paper on the home page  | `_bibliography/papers.bib`     | Add `selected={true}` to its entry                                                       |
| Edit a research topic             | `_projects/`                   | Edit `1_…md` to `4_…md`; the note at the top of `1_traffic_load_identification.md` helps |
| Add a research topic              | `_projects/`                   | Copy one of the files, rename it (e.g. `5_my_topic.md`), edit it                         |
| Show my teaching                  | `_pages/teaching.md`           | Follow the notes in the file (the page is hidden until I do)                             |
| Add a news item                   | `_news/`                       | Add a new file; copy the format of `announcement_1.md`                                   |
| Edit my CV                        | `_data/cv.yml`                 | Edit the entries; templates for Education/Experience are at the bottom                   |
| Use my own PDF CV                 | `assets/pdf/` + `_pages/cv.md` | Upload the PDF to `assets/pdf/`, then set `cv_pdf: /assets/pdf/yourfile.pdf`             |

## The editing loop

1. Open the file on GitHub and click the ✏️ pencil ("Edit this file").
2. Make your changes.
3. Scroll down and click **Commit changes**.
4. Wait about 1–2 minutes, then refresh the live site.

## Adding a brand-new file (e.g. a research topic or news item)

1. Go into the folder (e.g. `_projects/`), click **Add file → Create new file**.
2. Name it (e.g. `5_my_topic.md`), paste content copied from an existing file, and edit.
3. Click **Commit changes**.

## Adding a publication

Paste the BibTeX entry at the top of `_bibliography/papers.bib`. Useful extra lines
(each one goes inside the `{ … }` of the entry, with a comma at the end):

- `abbr={JBE},` short journal name shown as a coloured label
- `selected={true},` also show the paper on the home page
- `doi={10.xxxx/xxxxx},` adds a DOI button and citation badges (copy the DOI from
  the paper's web page)
- `pdf={my_paper.pdf},` adds a PDF button (upload the file to `assets/pdf/` first)
- `html={https://…},` adds a link button to any web page

To refer to a paper on a research page, write `{% cite key %}`, where
`key` is the first word of its entry (e.g. `ge2020accurate`).

## Avoid these common mistakes (they stop the whole site from updating)

In `.yml` files (`_config.yml`, `_data/socials.yml`, `_data/cv.yml`):

- Put **one space after every colon**: `orcid_id: 0000-…` (not `orcid_id:0000-…`).
- Put **a space before a `#` note** at the end of a line: `name: Ge # note`.
- **Keep the indentation** (the spaces at the start of lines) the same as nearby lines.
- In `_data/socials.yml`, give only the ID or username, **not** the full web address.

## If something looks broken

Open the repo's **Actions** tab and look at the latest **"Deploy site"** run:

- Green ✓ means the change is live.
- Red ✗ means the build failed. Click it to read the error. It is usually one of the
  mistakes above, in the file you just edited. Fix it, commit again, and it rebuilds.

Other workflows you may see in the Actions tab:

- **Render a CV** runs when `_data/cv.yml` changes and makes a PDF of the CV
  (`assets/rendercv/rendercv_output/Liangfu_Ge_CV.pdf`). If it fails, the CV file has an
  entry type it does not understand; compare it with the templates at the bottom of
  `_data/cv.yml`.
- **Update Google Scholar Citations** runs three times a week. It sometimes fails because
  Google blocks it. That is harmless.
- **Integration tests**, **Visual regression checks** and **Prettier code formatter** are
  the theme developers' own checks. They test demo pages that are not part of my site,
  so a red ✗ on them does **not** mean my website is broken.

## Important: don't touch these

- In `_config.yml`, leave `url` and `baseurl` as they are. Changing them breaks the site.
