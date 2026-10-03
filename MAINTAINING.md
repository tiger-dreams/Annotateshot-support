# Maintaining the support hub

Languages: English (`en`), Korean (`ko`), and Japanese (`ja`), matching the macOS app's localization set.

Edit `content/locales.json`, then run `python3 scripts/build.py`. The script uses only the Python standard library and generates the localized READMEs, guides, HTML pages, and issue forms. Commit both the content and generated files. `docs/assets/style.css` is maintained directly.

GitHub Pages publishes `main:/docs` to https://tiger-dreams.github.io/Annotateshot-support/. The root page uses English; every page offers English, Korean, and Japanese links to the same page in the selected language. Pages render without JavaScript.

Do not copy private app source, internal release notes, credentials, customer details, or unreleased screenshots into this repository. App Store and in-app support links are managed separately after owner review.
