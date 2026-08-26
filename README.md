A Github Pages template for academic websites. This was forked (then detached) by [Stuart Geiger](https://github.com/staeiou) from the [Minimal Mistakes Jekyll Theme](https://mmistakes.github.io/minimal-mistakes/), which is © 2016 Michael Rose and released under the MIT License. See LICENSE.md.

I think I've got things running smoothly and fixed some major bugs, but feel free to file issues or make pull requests if you want to improve the generic template / theme.

### Note: if you are using this repo and now get a notification about a security vulnerability, delete the Gemfile.lock file. 

# Instructions

1. Register a GitHub account if you don't have one and confirm your e-mail (required!)
1. Fork [this repository](https://github.com/academicpages/academicpages.github.io) by clicking the "fork" button in the top right. 
1. Go to the repository's settings (rightmost item in the tabs that start with "Code", should be below "Unwatch"). Rename the repository "[your GitHub username].github.io", which will also be your website's URL.
1. Set site-wide configuration and create content & metadata (see below -- also see [this set of diffs](http://archive.is/3TPas) showing what files were changed to set up [an example site](https://getorg-testacct.github.io) for a user with the username "getorg-testacct")
1. Upload any files (like PDFs, .zip files, etc.) to the files/ directory. They will appear at https://[your GitHub username].github.io/files/example.pdf.  
1. Check status by going to the repository settings, in the "GitHub pages" section
1. (Optional) Use the Jupyter notebooks or python scripts in the `markdown_generator` folder to generate markdown files for publications and talks from a TSV file.

See more info at https://academicpages.github.io/

## To run locally (not on GitHub Pages, to serve on your own computer)

1. Clone the repository and made updates as detailed above
1. Make sure you have ruby-dev, bundler, and nodejs installed: `sudo apt install ruby-dev ruby-bundler nodejs`
1. Run `bundle clean` to clean up the directory (no need to run `--force`)
1. Run `bundle install` to install ruby dependencies. If you get errors, delete Gemfile.lock and try again.
1. Install the dependencies with `bundle install`.
1. Run `bin/serve` to generate the HTML and serve it at
   `http://localhost:4000`. The local server automatically rebuilds the site
   and refreshes the browser when files change.

The local server loads both `_config.yml` and `_config.dev.yml`, which disables
analytics, uses the localhost URL, and emits expanded CSS for easier debugging.
It uses polling for file changes so it also works when the Linux inotify limit
has already been reached by other applications.

## Updating the CV

The website CV and printable PDF share the same source data. Do not enter the
same CV item directly in `_pages/cv.md` or `scripts/build_cv.py`; those files are
renderers and normally do not need to be edited when the CV content changes.

CV information is stored in these locations:

- `_data/cv.yaml`: contact details, appointments, research experience,
  education, honors and awards, fellowships, and service.
- `_publications/`: one Markdown file per publication.
- `_talks/`: one Markdown file per talk or presentation.
- `_teaching/`: one Markdown file per teaching entry.

### Core information

Edit `_data/cv.yaml` to update an appointment, award, fellowship, service role,
degree, advisor, email address, homepage, or Google Scholar link. Preserve the
existing YAML indentation and use `YYYY-MM` for month-level dates. For example:

```yaml
appointments:
  - title: Leinweber Postdoctoral Fellow
    institution: Stanford University
    start: 2026-09
    end: present

honors_and_awards:
  - name: Example Award
    year: 2026
    awarded_by: Example Department, Example University
```

Update `pdf.updated` in the same file whenever the CV is revised:

```yaml
pdf:
  filename: Yugo_Onishi_CV.pdf
  updated: 2026-08
```

### Publications

Add a Markdown file under `_publications/` using an existing publication file
as a template. Its front matter should provide at least `title`, `collection`,
`date`, `venue`, and `citation`:

```yaml
---
title: "Paper title"
collection: publications
date: 2026-01-01
venue: "Journal name"
citation: 'Author list, "Paper title." Journal name, 2026.'
---
```

The publication date controls its position in the PDF. The scripts in
`markdown_generator/` may also be used when importing publications from the
BibTeX bibliography instead of creating files manually.

### Talks and teaching

Add a Markdown file under `_talks/` for each presentation. Use an existing talk
as a template and provide `title`, `collection: talks`, `type`, `venue`, `date`,
and `location`. Similarly, add teaching records under `_teaching/` with
`collection: teaching`. Dates control reverse-chronological ordering.

```yaml
---
title: "Talk title"
collection: talks
type: "Invited talk"
venue: "Conference or institution"
date: 2026-05-01
location: "City, Country"
---
```

### Generate and publish

After changing any CV source file, rebuild the PDF from the repository root:

```powershell
.\.venv\Scripts\python.exe scripts\build_cv.py
```

This writes `output/pdf/Yugo_Onishi_CV.pdf`. Open the generated PDF and check
the page breaks before committing it. The website CV is rendered by Jekyll from
the same data and collections when GitHub Pages builds the site.

Commit the source changes and generated PDF together:

```powershell
git add _data/cv.yaml _publications _talks _teaching output/pdf/Yugo_Onishi_CV.pdf
git commit -m "Update CV"
git push
```

# Changelog -- bugfixes and enhancements

There is one logistical issue with a ready-to-fork template theme like academic pages that makes it a little tricky to get bug fixes and updates to the core theme. If you fork this repository, customize it, then pull again, you'll probably get merge conflicts. If you want to save your various .yml configuration files and markdown files, you can delete the repository and fork it again. Or you can manually patch. 

To support this, all changes to the underlying code appear as a closed issue with the tag 'code change' -- get the list [here](https://github.com/academicpages/academicpages.github.io/issues?q=is%3Aclosed%20is%3Aissue%20label%3A%22code%20change%22%20). Each issue thread includes a comment linking to the single commit or a diff across multiple commits, so those with forked repositories can easily identify what they need to patch.
