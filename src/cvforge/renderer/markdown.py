import pathlib

from cvforge.schema.models.cvforge_model import RenderCVModel

from .path_resolver import resolve_cvforge_file_path
from .templater.templater import render_full_template


def generate_markdown(cvforge_model: RenderCVModel) -> pathlib.Path | None:
    """Generate Markdown file from CV model via Jinja2 templates.

    Why:
        Markdown provides human-readable CV format for version control and
        web platforms. Acts as intermediate format for HTML generation.

    Args:
        cvforge_model: Validated CV model with content.

    Returns:
        Path to generated Markdown file, or None if generation disabled.
    """
    if cvforge_model.settings.render_command.dont_generate_markdown:
        return None
    markdown_path = resolve_cvforge_file_path(
        cvforge_model, cvforge_model.settings.render_command.markdown_path
    )
    markdown_contents = render_full_template(cvforge_model, "markdown")
    markdown_path.write_text(markdown_contents, encoding="utf-8")
    return markdown_path
