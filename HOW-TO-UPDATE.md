# How to update my website

My site is live at **https://civil-liangfu.github.io** and is built automatically by
GitHub. **I never need to install anything** — I just edit text files on github.com and
the site rebuilds itself in 1–2 minutes.

Everything below is done in the browser at
**github.com/Civil-Liangfu/Civil-Liangfu.github.io**.

## Where to edit

| I want to… | Edit this file | How |
|------------|----------------|-----|
| Change my bio | `_pages/about.md` | Edit the text |
| Change my photo | `assets/img/prof_pic.jpg` | Upload a new image with that exact name |
| Change my affiliation/address | `_pages/about.md` | Edit the `more_info` lines near the top |
| Add my links (email, GitHub, Scholar, ORCID) | `_data/socials.yml` | Uncomment a line and fill it in |
| Add a publication | `_bibliography/papers.bib` | Paste the paper's BibTeX entry near the top |
| Feature a paper on the home page | `_bibliography/papers.bib` | Add `selected = {true}` to its entry |
| Add a research project | `_projects/` | Copy `1_bridge_shm.md`, rename it, edit; image → `assets/img/` |
| Edit teaching | `_pages/teaching.md` | Edit the text |
| Add a news item | `_news/` | Click "Add file" → copy the format of `announcement_1.md` |
| Edit my CV | `_data/cv.yml` | Edit the entries (keep the indentation) |
| Add a downloadable CV PDF | upload to `assets/pdf/`, then `_pages/cv.md` | Set `cv_pdf:` to `/assets/pdf/yourfile.pdf` |

## The editing loop
1. Open the file on GitHub and click the ✏️ pencil ("Edit this file").
2. Make your changes.
3. Scroll down and click **Commit changes**.
4. Wait ~1–2 minutes, then refresh the live site.

## Adding a brand-new file (e.g. a project or news item)
1. Go into the folder (e.g. `_projects/`), click **Add file → Create new file**.
2. Name it (e.g. `2_my_project.md`), paste content copied from an existing file, edit.
3. **Commit changes.**

## If something looks broken
Open the repo's **Actions** tab. A red ✗ on the latest run means the build failed —
click it to read the error (usually a typo in `_config.yml`, `_data/*.yml`, or a `.bib`
entry — watch your indentation in YAML files). Fix the file, commit again, and it
rebuilds. A green ✓ means your change is live.

## Important: don't touch these
- In `_config.yml`, leave `url` and `baseurl` as they are — changing them breaks the site.
