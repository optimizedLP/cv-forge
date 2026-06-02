# Get Started

## Installation

1. Install [Python](https://www.python.org/downloads/) (3.12 or newer).

2. Run the command below to install RenderCV.

    === "pip"

        ```
        pip install "cvforge[full]"
        ```

    === "pipx"

        ```
        pipx install "cvforge[full]"
        ```

    === "uv"

        ```
        uv tool install "cvforge[full]"
        ```

    === "Docker"

        Docker image is available at [ghcr.io/cvforge/cvforge](https://github.com/rendercv/cvforge/pkgs/container/cvforge).

        ```bash
        docker run --rm -v "$PWD":/work -u $(id -u):$(id -g) -e HOME=/tmp -w /work ghcr.io/cvforge/cvforge new "Your Name"
        ```

## Quick Start

1. Create a new CV YAML input file

    ```bash
    cvforge new "Your Name"
    ```

    This creates a YAML input file called `Your_Name_CV.yaml`. This file contains the content, design options, translations and settings for RenderCV. See [YAML Input Structure](yaml_input_structure/index.md) for the full reference.

    See the [CLI Reference](cli_reference.md#cvforge-new) for the complete list of options available for the `new` command.

    !!! tip
        To get started with another language or theme, you can use the `--locale` and `--theme` options:

        ```bash
        cvforge new "Your Name" --locale "turkish" --theme "engineeringresumes"
        ```


2. Render the YAML input file with

    ```bash
    cvforge render "Your_Name_CV.yaml"
    ```

    This generates a `cvforge_output/` directory containing:

    - `John_Doe_CV.pdf`: Your CV as PDF
    - `John_Doe_CV.typ`: [Typst](https://typst.app) source code of the PDF
    - `John_Doe_CV_1.png`, `..._2.png`, ...: PNG images of each page of the PDF
    - `John_Doe_CV.md`: Your CV as Markdown
    - `John_Doe_CV.html`: Your CV as HTML (generated from the Markdown)

    See the [CLI Reference](cli_reference.md#cvforge-render) for the complete list of options available for the `render` command.

    !!! tip
        To re-render automatically whenever you save changes, use the `--watch` option:

        ```bash
        cvforge render --watch "Your_Name_CV.yaml"
        ```
