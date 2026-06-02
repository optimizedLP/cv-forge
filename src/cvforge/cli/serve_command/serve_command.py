"""Live preview server command for CV-Forge."""

import http.server
import pathlib
import socketserver
import threading
from typing import Annotated

import typer
from rich.console import Console

from ..app import app
from ..error_handler import handle_user_errors

console = Console()

# Will be imported at runtime to avoid circular imports
_run_cvforge = None


def _get_run_cvforge():
    """Lazy import to avoid circular dependency."""
    global _run_cvforge
    if _run_cvforge is None:
        from ..render_command.run_cvforge import run_cvforge  # noqa: PLC0415

        _run_cvforge = run_cvforge
    return _run_cvforge


def _get_progress_panel():
    """Lazy import progress panel."""
    from ..render_command.progress_panel import ProgressPanel  # noqa: PLC0415

    return ProgressPanel


def _get_collect_input_file_paths():
    """Lazy import file collector."""
    from ..render_command.run_cvforge import (  # noqa: PLC0415
        collect_input_file_paths,
    )

    return collect_input_file_paths


def _get_watcher():
    """Lazy import watcher."""
    from ..render_command.watcher import (  # noqa: PLC0415
        run_function_if_files_change,
    )

    return run_function_if_files_change


def _get_parse_override_arguments():
    """Lazy import arg parser."""
    from ..render_command.parse_override_arguments import (  # noqa: PLC0415
        parse_override_arguments,
    )

    return parse_override_arguments


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler that suppresses log output."""

    def log_message(self, format, *args):
        pass  # Suppress logs


def start_server(directory: pathlib.Path, port: int) -> socketserver.TCPServer:
    """Start a simple HTTP server in a background thread."""
    import os

    # Save and restore cwd instead of permanent chdir
    original_cwd = os.getcwd()
    os.chdir(str(directory))

    class CwdHandler(QuietHandler):
        def __init__(self, *args, **kwargs):
            os.chdir(str(directory))
            super().__init__(*args, **kwargs)

    handler = CwdHandler
    server = socketserver.TCPServer(("localhost", port), handler)
    os.chdir(original_cwd)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


@app.command(
    name="serve",
    help=(
        "Start a live preview server for your CV. Example:"
        " [yellow]cvforge serve John_Doe_CV.yaml[/yellow]"
    ),
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
)
@handle_user_errors
def cli_command_serve(
    input_file_name: Annotated[
        pathlib.Path,
        typer.Argument(help="The YAML input file to serve."),
    ],
    port: Annotated[
        int,
        typer.Option(
            "--port",
            "-p",
            help="Port to serve on (default: 8888).",
        ),
    ] = 8888,
    theme: Annotated[
        str | None,
        typer.Option(
            "--theme",
            "-t",
            help="Theme to use for rendering.",
        ),
    ] = None,
    extra_context: typer.Context = None,  # ty: ignore[invalid-parameter-default]
) -> None:
    """Start a local preview server with hot-reload for CV rendering.

    Renders the CV, starts an HTTP server serving the output folder,
    and watches the input file for changes to auto-re-render.
    """
    input_file_path = pathlib.Path(input_file_name).absolute()

    if not input_file_path.exists():
        console.print(f"[red]File not found: {input_file_path}[/red]")
        raise typer.Exit(1)

    run_cvforge_fn = _get_run_cvforge()
    ProgressPanel = _get_progress_panel()
    collect_input_file_paths = _get_collect_input_file_paths()
    run_function_if_files_change = _get_watcher()
    parse_override_arguments = _get_parse_override_arguments()

    # Parse extra args as overrides
    overrides = parse_override_arguments(extra_context) if extra_context else {}

    # Build render arguments
    from cvforge.schema.cvforge_model_builder import (  # noqa: PLC0415
        BuildRendercvModelArguments,
    )

    arguments: BuildRendercvModelArguments = {
        "design_yaml_file": None,
        "locale_yaml_file": None,
        "settings_yaml_file": None,
        "output_folder": None,
        "typst_path": None,
        "pdf_path": None,
        "markdown_path": None,
        "html_path": None,
        "png_path": None,
        "dont_generate_typst": None,
        "dont_generate_html": None,
        "dont_generate_markdown": None,
        "dont_generate_pdf": None,
        "dont_generate_png": None,
        "overrides": overrides,
    }

    # Determine output folder - use the one from settings or default
    resolved_files = collect_input_file_paths(input_file_path)

    # Build render arguments (output_folder=None means use default from YAML settings)

    def render_and_notify() -> None:
        """Render the CV and print a message."""
        console.print("\n[bold cyan]🔄 Rendering CV...[/bold cyan]")
        with ProgressPanel(quiet=False) as progress:
            run_cvforge_fn(input_file_path, progress, **arguments)
        console.print(
            f"[green]✓ CV rendered![/green] Preview at"
            f" [bold cyan]http://localhost:{port}[/bold cyan]"
        )

    # Initial render
    render_and_notify()

    # Determine actual output folder by checking what run_cvforge produced
    from cvforge.schema.cvforge_model_builder import (  # noqa: PLC0415
        build_cvforge_dictionary_and_model,
    )

    main_yaml = input_file_path.read_text(encoding="utf-8")
    _, model = build_cvforge_dictionary_and_model(
        main_yaml, input_file_path=input_file_path, **arguments
    )
    output_folder = model.settings.render_command.output_folder

    # Start HTTP server
    console.print(
        f"\n[bold green]🚀 Live preview server started![/bold green]\n"
        f"  📂 Serving: [bold]{output_folder}[/bold]\n"
        f"  🌐 URL: [bold cyan]http://localhost:{port}[/bold cyan]\n"
        f"  📝 Edit [bold]{input_file_path.name}[/bold] to auto-reload\n"
        f"  🛑 Press [bold]Ctrl+C[/bold] to stop\n"
    )

    server = start_server(output_folder, port)

    try:
        # Watch for changes and re-render
        watch_paths = list(resolved_files.values())
        run_function_if_files_change(watch_paths, render_and_notify)
    except KeyboardInterrupt:
        console.print("\n[yellow]Shutting down server...[/yellow]")
    finally:
        server.shutdown()
        console.print("[green]Server stopped.[/green]")
