# EMCR'2028 website

Official website source for **EMCR'2028 — Electrochemical Methods in Corrosion Research**, Vigo, Spain, May 2028.

The conference and attendee accommodation are planned at **Attica21 Vigo Business & Wellness, Samil, Vigo**.

## Repository structure

```text
.
├── index.html
├── styles.css
├── script.js
├── assets/
│   └── emcr2028-logo.png
├── tools/
│   └── check_site.py
├── .github/
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/
│       ├── check-site.yml
│       └── deploy-pages.yml
├── .gitignore
├── .nojekyll
└── README.md
```

## Recommended branch workflow

- `development` — normal content and design work.
- Pull Request — review and automatic site validation.
- `main` — public production version.
- Every push to `main` triggers deployment to GitHub Pages.

Suggested flow:

```text
development → Pull Request → main → GitHub Actions → GitHub Pages
```

## First-time GitHub setup

1. Create a GitHub repository, for example `emcr2028`.
2. Upload or push the contents of this folder to the repository.
3. Ensure the production branch is named `main`.
4. In **Settings → Pages → Build and deployment → Source**, choose **GitHub Actions**.
5. Push to `main`, or run the workflow manually from the **Actions** tab.
6. GitHub Pages will publish the site at a URL similar to:
   `https://USERNAME.github.io/emcr2028/`

## Development branch

After the first push, create the working branch:

```bash
git checkout -b development
git push -u origin development
```

Use `development` for routine edits. When changes are ready, open a Pull Request into `main`.

## Local validation

Before committing changes, run:

```bash
python tools/check_site.py
```

The validator checks:

- local CSS, JavaScript and image references;
- internal `#fragment` links;
- missing required site files;
- root-absolute local paths that may fail when GitHub Pages publishes the site inside a project subdirectory.

No third-party Python packages are required.

## GitHub Actions

### `check-site.yml`

Runs automatically on:

- Pull Requests;
- pushes to `development`.

It validates local links and required assets.

### `deploy-pages.yml`

Runs on every push to `main` and can also be launched manually. It:

1. validates the website;
2. configures GitHub Pages;
3. uploads the static site;
4. deploys it to the `github-pages` environment.

## Publishing content safely

Before merging to `main`, verify that all public conference information is confirmed, especially:

- exact conference dates;
- abstract submission and acceptance deadlines;
- registration fees and payment instructions;
- invited and plenary speakers;
- scientific and organising committee membership;
- final scientific programme;
- Attica21 reservation instructions, included nights and room conditions;
- social programme and transport arrangements;
- official contact addresses.

## Custom domain (optional)

If an official domain is added later, configure it in **Settings → Pages → Custom domain**. GitHub can then create or use a `CNAME` file. Do not add a `CNAME` file until the actual domain is known.

## Updating the conference logo

Replace:

```text
assets/emcr2028-logo.png
```

with the revised file while keeping the same filename. The current HTML will use it automatically.
