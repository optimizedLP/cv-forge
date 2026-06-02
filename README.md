<div align="center">
<h1>RenderCV</h1>

_Resume builder for academics and engineers, deployed at [rendercv.com](https://rendercv.com)_

[![test](https://github.com/rendercv/cvforge/actions/workflows/test.yaml/badge.svg?branch=main)](https://github.com/rendercv/cvforge/actions/workflows/test.yaml)
[![coverage](https://coverage-badge.samuelcolvin.workers.dev/cvforge/cvforge.svg)](https://coverage-badge.samuelcolvin.workers.dev/redirect/cvforge/cvforge)
[![docs](<https://img.shields.io/badge/docs-mkdocs-rgb(0%2C79%2C144)>)](https://docs.rendercv.com)
[![pypi-version](<https://img.shields.io/pypi/v/cvforge?label=PyPI%20version&color=rgb(0%2C79%2C144)>)](https://pypi.python.org/pypi/cvforge)
[![pypi-downloads](<https://img.shields.io/pepy/dt/cvforge?label=PyPI%20downloads&color=rgb(0%2C%2079%2C%20144)>)](https://pypistats.org/packages/cvforge)

</div>

Write your CV or resume as YAML, then run RenderCV,

```bash
cvforge render John_Doe_CV.yaml
```

and get a PDF with perfect typography.

With RenderCV, you can:

- Version-control your CV — it's just text.
- Focus on content — don't worry about the formatting.
- Get perfect typography — consistent alignment and spacing, handled for you.

A YAML file like this:

```yaml
cv:
  name: John Doe
  location: San Francisco, CA
  email: john.doe@email.com
  website: https://rendercv.com/
  social_networks:
    - network: LinkedIn
      username: cvforge
    - network: GitHub
      username: cvforge
  sections:
    Welcome to RenderCV:
      - RenderCV reads a CV written in a YAML file, and generates a PDF with professional typography.
      - See the [documentation](https://docs.rendercv.com) for more details.
    education:
      - institution: Princeton University
        area: Computer Science
        degree: PhD
        date:
        start_date: 2018-09
        end_date: 2023-05
        location: Princeton, NJ
        summary:
        highlights:
          - "Thesis: Efficient Neural Architecture Search for Resource-Constrained Deployment"
          - "Advisor: Prof. Sanjeev Arora"
          - NSF Graduate Research Fellowship, Siebel Scholar (Class of 2022)
    ...
```

becomes one of these PDFs. Click on the images to preview.

| [![Classic Theme Example of RenderCV](https://raw.githubusercontent.com/cvforge/cvforge/main/docs/assets/images/examples/classic.png)](https://github.com/rendercv/cvforge/blob/main/examples/John_Doe_ClassicTheme_CV.pdf) | [![Engineeringresumes Theme Example of RenderCV](https://raw.githubusercontent.com/cvforge/cvforge/main/docs/assets/images/examples/engineeringresumes.png)](https://github.com/rendercv/cvforge/blob/main/examples/John_Doe_EngineeringresumesTheme_CV.pdf) | [![Sb2nov Theme Example of RenderCV](https://raw.githubusercontent.com/cvforge/cvforge/main/docs/assets/images/examples/sb2nov.png)](https://github.com/rendercv/cvforge/blob/main/examples/John_Doe_Sb2novTheme_CV.pdf) |
| --- | --- | --- |
| [![Moderncv Theme Example of RenderCV](https://raw.githubusercontent.com/cvforge/cvforge/main/docs/assets/images/examples/moderncv.png)](https://github.com/rendercv/cvforge/blob/main/examples/John_Doe_ModerncvTheme_CV.pdf) | [![Engineeringclassic Theme Example of RenderCV](https://raw.githubusercontent.com/cvforge/cvforge/main/docs/assets/images/examples/engineeringclassic.png)](https://github.com/rendercv/cvforge/blob/main/examples/John_Doe_EngineeringclassicTheme_CV.pdf) | [![Harvard Theme Example of RenderCV](https://raw.githubusercontent.com/cvforge/cvforge/main/docs/assets/images/examples/harvard.png)](https://github.com/rendercv/cvforge/blob/main/examples/John_Doe_HarvardTheme_CV.pdf) |
| [![Ink Theme Example of RenderCV](https://raw.githubusercontent.com/cvforge/cvforge/main/docs/assets/images/examples/ink.png)](https://github.com/rendercv/cvforge/blob/main/examples/John_Doe_InkTheme_CV.pdf) | [![Opal Theme Example of RenderCV](https://raw.githubusercontent.com/cvforge/cvforge/main/docs/assets/images/examples/opal.png)](https://github.com/rendercv/cvforge/blob/main/examples/John_Doe_OpalTheme_CV.pdf) | [![Ember Theme Example of RenderCV](https://raw.githubusercontent.com/cvforge/cvforge/main/docs/assets/images/examples/ember.png)](https://github.com/rendercv/cvforge/blob/main/examples/John_Doe_EmberTheme_CV.pdf) |


## JSON Schema

RenderCV's JSON Schema lets you fill out the YAML interactively, with autocompletion and inline documentation.

![JSON Schema of RenderCV](https://raw.githubusercontent.com/cvforge/cvforge/main/docs/assets/images/json_schema.gif)


## Extensive Design Options

You have full control over every detail.

```yaml
design:
  theme: classic
  page:
    size: us-letter
    top_margin: 0.7in
    bottom_margin: 0.7in
    left_margin: 0.7in
    right_margin: 0.7in
    show_footer: true
    show_top_note: true
  colors:
    body: rgb(0, 0, 0)
    name: rgb(0, 79, 144)
    headline: rgb(0, 79, 144)
    connections: rgb(0, 79, 144)
    section_titles: rgb(0, 79, 144)
    links: rgb(0, 79, 144)
    footer: rgb(128, 128, 128)
    top_note: rgb(128, 128, 128)
  typography:
    line_spacing: 0.6em
    alignment: justified
    date_and_location_column_alignment: right
    font_family: Source Sans 3
  # ...and much more
```

![Design Options of RenderCV](https://raw.githubusercontent.com/cvforge/cvforge/main/docs/assets/images/design_options.gif)

> [!TIP]
> Want to set up a live preview environment like the one shown above? See [how to set up VS Code for RenderCV](https://docs.rendercv.com/user_guide/how_to/set_up_vs_code_for_cvforge).

## Strict Validation

No surprises. If something's wrong, you'll know exactly what and where. If it's valid, you get a perfect PDF.

![Strict Validation Feature of RenderCV](https://raw.githubusercontent.com/cvforge/cvforge/main/docs/assets/images/validation.gif)


## Any Language

Fill out the locale field for your language.

```yaml
locale:
  language: english
  last_updated: Last updated in
  month: month
  months: months
  year: year
  years: years
  present: present
  month_abbreviations:
    - Jan
    - Feb
    - Mar
  ...
```

## AI Agent Skill

Let AI coding agents create and edit your CV. Install the RenderCV skill:

```bash
npx skills add cvforge/cvforge-skill
```

Works with any AI agent that supports the [skills standard](https://skills.sh). The skill is [auto-generated](https://github.com/rendercv/cvforge/blob/main/scripts/cvforge_skill/generate.py) from RenderCV's source code and [evaluated](https://github.com/rendercv/cvforge/tree/main/scripts/cvforge_skill/evals) with promptfoo against RenderCV's own Pydantic validation pipeline. See the [documentation](https://docs.rendercv.com/user_guide/how_to/use_the_ai_agent_skill) for details.

## Get Started

Install RenderCV (Requires Python 3.12+):

```
pip install "cvforge[full]"
```

Create a new CV yaml file:

```
cvforge new "John Doe"
```

Edit the YAML, then render:

```
cvforge render "John_Doe_CV.yaml"
```

For more details, see the [user guide](https://docs.rendercv.com/user_guide/).

## CV-Forge Extra Features

CV-Forge adds several new features on top of RenderCV:

### ATS Keyword Checker

Check your CV's compatibility with a job description:

```bash
cvforge ats John_Doe_CV.pdf --job-desc job_description.txt
```

Or check against specific keywords:

```bash
cvforge ats John_Doe_CV.pdf --keywords "Python,SQL,Machine Learning"
```

Requires `PyMuPDF` (included in `cvforge[full]`).

### Live Preview Server

Start a local preview server with hot-reload:

```bash
cvforge serve John_Doe_CV.yaml
```

Opens at [http://localhost:8888](http://localhost:8888). Edit your YAML and the preview auto-refreshes.

### YAML Minifier

Strip comments and whitespace from your CV YAML:

```bash
cvforge minify John_Doe_CV.yaml -o minified.yaml
```

### LinkedIn → YAML Import

Convert a LinkedIn profile into a CV YAML starter:

```bash
# Paste from clipboard
cvforge linkedin --paste

# Or read from file
cvforge linkedin --file linkedin_profile.txt -o my_cv.yaml
```

(Note: best-effort parsing — review the generated YAML before rendering.)

### Section Ordering

Reorder sections without editing your YAML:

```yaml
settings:
  section_order:
    - Skills
    - Experience
    - Education
    - Projects
```

### Custom Output Naming

Use `NAME_IN_TITLE_SNAKE_CASE` to get title-case file names like `Dhruv_Jani_CV.pdf`:

```yaml
settings:
  render_command:
    pdf_path: OUTPUT_FOLDER/NAME_IN_TITLE_SNAKE_CASE_CV.pdf
```

### New Themes

Four additional built-in themes:
- `minimal` — ultra-clean, all black, lots of whitespace
- `sleek` — dark-accented, compact professional design
- `academic` — serif font, dense layout for academic CVs
- `executive` — bold, spacious, leadership-oriented

```yaml
design:
  theme: minimal
```
