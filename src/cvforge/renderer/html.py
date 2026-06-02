import pathlib

from cvforge.schema.models.cvforge_model import RenderCVModel

from .path_resolver import resolve_cvforge_file_path
from .templater.templater import render_html


def generate_html(
    cvforge_model: RenderCVModel, markdown_path: pathlib.Path | None
) -> pathlib.Path | None:
    """Generate HTML file from Markdown source with styling.

    Why:
        HTML format enables web hosting and sharing CVs online. Converts
        Markdown to HTML body and wraps with CSS styling and metadata.

    Args:
        cvforge_model: CV model for path resolution and rendering context.
        markdown_path: Path to Markdown source file.

    Returns:
        Path to generated HTML file, or None if generation disabled.
    """
    if (
        cvforge_model.settings.render_command.dont_generate_html
        or markdown_path is None
    ):
        return None
    html_path = resolve_cvforge_file_path(
        cvforge_model, cvforge_model.settings.render_command.html_path
    )
    html_contents = render_html(
        cvforge_model, markdown_path.read_text(encoding="utf-8")
    )
    html_path.write_text(html_contents, encoding="utf-8")
    return html_path
