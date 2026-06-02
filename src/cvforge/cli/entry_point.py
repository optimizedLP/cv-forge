"""Entry point for the RenderCV CLI.

Why:
    Users might install RenderCV with `pip install cvforge` instead of
    `pip install cvforge[full]`. This module catches that case and shows a helpful
    error message instead of a confusing `ImportError`.
"""

import sys


def entry_point() -> None:
    """Entry point for the RenderCV CLI."""
    try:
        from .app import app as cli_app  # NOQA: PLC0415
    except ImportError:
        error_message = """
It looks like you installed RenderCV with:

    pip install cvforge

But RenderCV needs to be installed with:

    pip install "cvforge[full]"

Please reinstall with the correct command above.
"""
        sys.stderr.write(error_message)
        raise SystemExit(1) from None

    cli_app()
