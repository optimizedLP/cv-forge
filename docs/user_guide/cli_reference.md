---
toc_depth: 1
---

# CLI Reference

RenderCV provides a command-line interface with three main commands:

- **`cvforge new`** - Generate a sample CV to get started
- **`cvforge render`** - Generate PDF, Markdown, HTML, and PNG from your YAML input
- **`cvforge create-theme`** - Create a custom theme with editable templates

!!! tip "New to command line?"
    Commands are typed in your terminal/command prompt. Options starting with `--` modify behavior:

    ```bash
    cvforge new "John Doe" --theme moderncv
    ```

    **You can combine multiple options** in a single command:

    ```bash
    cvforge render CV.yaml --watch --dont-generate-html --dont-generate-png
    ```

    This renders your CV with auto-reload enabled, skipping HTML and PNG generation.

## `cvforge`

Check your installed version:

```bash
cvforge --version
```

Get help anytime:

```bash
cvforge --help
```

## `cvforge new`

Generate a sample CV file to start editing.

**Basic usage:**

```bash
cvforge new "John Doe"
```

This creates `John_Doe_CV.yaml` in your current folder.

**Choose a different theme:**

```bash
cvforge new "John Doe" --theme moderncv
```

Available themes: << available_themes >>

**Use a different language:**

```bash
cvforge new "John Doe" --locale french
```

Available locales: << available_locales >>

**For advanced users - generate editable templates:**

```bash
cvforge new "John Doe" --create-typst-templates
```

This creates template files you can customize for complete design control. See [Override Default Templates](how_to/override_default_templates.md) for details.

## `cvforge render`

Generate your CV outputs (PDF, Markdown, HTML, PNG) from a YAML file.

**Basic usage:**

```bash
cvforge render John_Doe_CV.yaml
```

This creates a `cvforge_output` folder with all formats.

### Common Scenarios

**Auto-reload while editing:**

```bash
cvforge render John_Doe_CV.yaml --watch
```

The CV regenerates automatically whenever you save changes. Great for live preview!

**Only generate PDF:**

```bash
cvforge render John_Doe_CV.yaml --dont-generate-markdown --dont-generate-html --dont-generate-png
```

Or use the short form:

```bash
cvforge render John_Doe_CV.yaml -nomd -nohtml -nopng
```

**Custom output location:**

```bash
cvforge render John_Doe_CV.yaml --pdf-path ~/Desktop/MyCV.pdf
```

### All Options

| Option                     | Short     | What it does                     |
| -------------------------- | --------- | -------------------------------- |
| `--watch`                  | `-w`      | Re-render when file changes      |
| `--quiet`                  | `-q`      | Hide all messages                |
| `--design FILE`            | `-d`      | Load design from separate file   |
| `--locale-catalog FILE`    | `-lc`     | Load locale from separate file   |
| `--settings FILE`          | `-s`      | Load settings from separate file |
| `--pdf-path PATH`          | `-pdf`    | Custom PDF location              |
| `--typst-path PATH`        | `-typ`    | Custom Typst location            |
| `--markdown-path PATH`     | `-md`     | Custom Markdown location         |
| `--html-path PATH`         | `-html`   | Custom HTML location             |
| `--png-path PATH`          | `-png`    | Custom PNG location              |
| `--dont-generate-pdf`      | `-nopdf`  | Skip PDF generation              |
| `--dont-generate-typst`    | `-notyp`  | Skip Typst generation            |
| `--dont-generate-markdown` | `-nomd`   | Skip Markdown generation         |
| `--dont-generate-html`     | `-nohtml` | Skip HTML generation             |
| `--dont-generate-png`      | `-nopng`  | Skip PNG generation              |

**Override any YAML value:**

Use dot notation to change specific fields. This overrides values in the YAML without editing the file.

```bash
cvforge render CV.yaml --cv.phone "+1-555-555-5555"
cvforge render CV.yaml --cv.sections.education.0.institution "MIT"
cvforge render CV.yaml --design.theme "moderncv"
```

## `cvforge create-theme`

Create your own theme with full control over the design.

**Basic usage:**

```bash
cvforge create-theme "mytheme"
```

This creates a `mytheme/` folder with template files you can edit. See [Override Default Templates](how_to/override_default_templates.md) for details.
