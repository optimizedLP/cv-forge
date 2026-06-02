"""YAML minifier command for CV-Forge."""

import pathlib
from typing import Annotated

import typer
from rich.console import Console

from ..app import app
from ..error_handler import handle_user_errors

console = Console()


@app.command(
    name="minify",
    help=(
        "Minify a YAML file by removing comments and extra whitespace. Example:"
        " [yellow]cvforge minify John_Doe_CV.yaml[/yellow]"
    ),
)
@handle_user_errors
def cli_command_minify(
    input_file: Annotated[
        pathlib.Path,
        typer.Argument(help="The YAML file to minify."),
    ],
    output: Annotated[
        pathlib.Path | None,
        typer.Option(
            "--output",
            "-o",
            help=(
                "Output path for the minified file. If not provided, prints to stdout."
            ),
        ),
    ] = None,
    strip_comments: Annotated[
        bool,
        typer.Option(
            "--strip-comments/--keep-comments",
            help="Strip comments from the YAML. Default: strip.",
        ),
    ] = True,
    strip_empty_lines: Annotated[
        bool,
        typer.Option(
            "--strip-empty-lines/--keep-empty-lines",
            help="Strip empty lines. Default: strip.",
        ),
    ] = True,
) -> None:
    """Minify a YAML input file.

    Strips comments and/or empty lines to produce a compact version
    suitable for embedding or storage.
    """
    if not input_file.exists():
        console.print(f"[red]File not found: {input_file}[/red]")
        raise typer.Exit(1)

    lines = input_file.read_text(encoding="utf-8").splitlines()

    minified_lines = []
    for line in lines:
        # Strip inline comments (but not URL lines starting with # yaml-language-server)
        if strip_comments and "#" in line:
            # Keep schema directive lines
            if line.strip().startswith("# yaml-language-server"):
                minified_lines.append(line)
                continue
            # Strip inline comments
            comment_pos = line.find("#")
            if comment_pos > 0:
                line = line[:comment_pos]

        stripped = line.rstrip()

        # Skip empty lines
        if strip_empty_lines and not stripped:
            continue

        minified_lines.append(stripped)

    result = "\n".join(minified_lines)

    # Remove trailing whitespace from all lines
    result = "\n".join(line.rstrip() for line in result.splitlines())

    # Remove multiple consecutive blank lines
    while "\n\n\n" in result:
        result = result.replace("\n\n\n", "\n\n")

    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(result + "\n", encoding="utf-8")
        original_size = input_file.stat().st_size
        new_size = output.stat().st_size
        reduction = int((1 - new_size / original_size) * 100) if original_size else 0
        console.print(
            f"[green]✓ Minified YAML saved to: {output}[/green]"
            f" ({original_size} → {new_size} bytes, {reduction}% smaller)"
        )
    else:
        console.print(result)
