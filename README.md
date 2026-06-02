# CV-Forge

> Build professional CVs in YAML. Forked from [RenderCV](https://github.com/rendercv/rendercv) (MIT) by [Sina Atalay](https://github.com/sinaatalay).

Write your CV as YAML — get a PDF with perfect typography. Version-control your CV like code, focus on content, and let the tool handle formatting, alignment, and spacing.

```bash
pip install -e ".[full]"
cvforge new "Your Name"
cvforge render Your_Name_CV.yaml
```

## What's Different from RenderCV

CV-Forge extends RenderCV v2.8 with features for data scientists and engineers:

| Feature | Command |
|---------|---------|
| **ATS Keyword Checker** | `cvforge ats cv.pdf --job-desc job.txt` |
| **Live Preview Server** | `cvforge serve cv.yaml` → `localhost:8888` |
| **YAML Minifier** | `cvforge minify cv.yaml -o min.yaml` |
| **LinkedIn → YAML** | `cvforge linkedin --paste` |
| **Section Ordering** | Add `section_order:` in settings |
| **Title-Case Output** | `pdf_path: OUTPUT_FOLDER/NAME_IN_TITLE_SNAKE_CASE_CV.pdf` |

## Themes

12 built-in themes — 8 from RenderCV + 4 new ones:

- **New:** `minimal` · `sleek` · `academic` · `executive`
- **Original:** `classic` · `engineeringclassic` · `engineeringresumes` · `harvard` · `sb2nov` · `moderncv` · `ink` · `opal` · `ember`

```yaml
design:
  theme: minimal
```

## Quick Example

```yaml
cv:
  name: Jane Doe
  location: New York, NY
  email: jane@example.com
  sections:
    experience:
      - company: Acme Corp
        position: Data Scientist
        highlights:
          - Built ML pipelines serving 1M+ users
    skills:
      - label: Languages
        details: Python, SQL, R
design:
  theme: sleek
```

## Credit

This project is a fork of **[RenderCV](https://github.com/rendercv/rendercv)** (v2.8, MIT License) by [Sina Atalay](https://github.com/sinaatalay). The original rendering engine, Typst pipeline, JSON Schema, and 8 base themes are RenderCV's work. CV-Forge adds themes, CLI commands, and quality-of-life features on top.

For full RenderCV documentation: [docs.rendercv.com](https://docs.rendercv.com)
