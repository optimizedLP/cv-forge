"""ATS keyword scorer command for CV-Forge."""

import pathlib
import re
import string
from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ..app import app
from ..error_handler import handle_user_errors

console = Console()


def extract_text_from_pdf(pdf_path: pathlib.Path) -> str:
    """Extract plain text from a PDF file using PyMuPDF.

    Falls back to reading raw bytes if PyMuPDF is not available.
    """
    try:
        import fitz  # PyMuPDF

        doc = fitz.open(str(pdf_path))
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except ImportError:
        console.print(
            "[yellow]PyMuPDF not installed. Install with: pip install PyMuPDF[/yellow]"
        )
        raise typer.Exit(1)


def tokenize(text: str) -> set[str]:
    """Tokenize text into lowercase words, removing punctuation and stopwords."""
    stopwords = {
        "a",
        "an",
        "the",
        "and",
        "or",
        "but",
        "in",
        "on",
        "at",
        "to",
        "for",
        "of",
        "with",
        "by",
        "from",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "being",
        "have",
        "has",
        "had",
        "do",
        "does",
        "did",
        "will",
        "would",
        "could",
        "should",
        "may",
        "might",
        "can",
        "shall",
        "you",
        "your",
        "we",
        "they",
        "their",
        "our",
        "its",
        "it",
        "this",
        "that",
        "these",
        "those",
        "not",
        "no",
        "very",
        "just",
        "about",
        "also",
    }
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    words = text.split()
    return {w for w in words if w not in stopwords and len(w) > 2}


def extract_keywords(job_description: str) -> list[str]:
    """Extract meaningful single and multi-word keywords from a job description."""
    # Remove common filler words
    cleaned = re.sub(
        r"(?i)\b(a|an|the|and|or|but|in|on|at|to|for|of|with|by|from|is|are|was|were|be|been|being|have|has|had|do|does|did|will|would|could|should|may|might|can|shall|you|your|we|they|their|our)\b",
        "",
        job_description,
    )

    # Extract capitalized phrases (likely proper nouns/technologies)
    capitalized = re.findall(r"\b[A-Z][a-z]*(?:\s+[A-Z][a-z]*)*\b", job_description)

    # Extract technical terms (words containing special chars or numbers)
    technical = re.findall(r"\b\w*[\d.]+\w*\b", job_description)

    # Standard single words
    words = tokenize(job_description)

    # Combine and deduplicate
    all_keywords = set(
        w.lower().strip()
        for w in [*capitalized, *technical, *words]
        if len(w.strip()) > 2
    )

    return sorted(all_keywords)


@app.command(
    name="ats",
    help=(
        "Check CV compatibility with a job description. Example:"
        " [yellow]cvforge ats John_Doe_CV.pdf --job-desc job.txt[/yellow]"
    ),
)
@handle_user_errors
def cli_command_ats(
    pdf_path: Annotated[
        pathlib.Path,
        typer.Argument(help="Path to the generated CV PDF file."),
    ],
    job_desc: Annotated[
        str | None,
        typer.Option(
            "--job-desc",
            "-j",
            help=(
                "Job description text. Either provide the text directly, or a path"
                " to a text file containing the job description."
            ),
        ),
    ] = None,
    keywords: Annotated[
        str | None,
        typer.Option(
            "--keywords",
            "-k",
            help=(
                "Comma-separated keywords to check against (e.g.,"
                " 'Python,SQL,Machine Learning')."
            ),
        ),
    ] = None,
    min_score: Annotated[
        int,
        typer.Option(
            "--min-score",
            "-m",
            help="Minimum score threshold to highlight (0-100).",
        ),
    ] = 0,
) -> None:
    """Score a CV PDF against a job description or keywords.

    Extracts text from the PDF, compares against keywords from the job
    description or provided list, and reports a compatibility score.
    """
    if not pdf_path.exists():
        console.print(f"[red]PDF not found: {pdf_path}[/red]")
        raise typer.Exit(1)

    if not job_desc and not keywords:
        console.print(
            "[red]Provide either --job-desc or --keywords with a file or text.[/red]"
        )
        raise typer.Exit(1)

    # Extract CV text
    console.print(f"\n[bold]Extracting text from:[/bold] {pdf_path}")
    cv_text = extract_text_from_pdf(pdf_path)
    cv_tokens = tokenize(cv_text)
    console.print(f"  ✓ Extracted {len(cv_tokens)} unique keywords from CV\n")

    # Get target keywords
    if job_desc:
        # Check if it's a file path
        job_desc_path = pathlib.Path(job_desc)
        if job_desc_path.exists() and job_desc_path.is_file():
            job_desc = job_desc_path.read_text(encoding="utf-8")
        target_keywords = set(extract_keywords(job_desc))
    elif keywords:
        target_keywords = set(k.strip().lower() for k in keywords.split(","))
    else:
        target_keywords = set()

    if not target_keywords:
        console.print("[red]No keywords extracted from job description.[/red]")
        raise typer.Exit(1)

    # Score
    matched = target_keywords & cv_tokens
    missing = target_keywords - cv_tokens

    if target_keywords:
        score = int((len(matched) / len(target_keywords)) * 100)
    else:
        score = 0

    # Display results
    table = Table(
        title="ATS Compatibility Report", show_header=True, header_style="bold"
    )
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    table.add_row("Total Keywords in Job", str(len(target_keywords)))
    table.add_row("Matched Keywords", str(len(matched)))
    table.add_row("Missing Keywords", str(len(missing)))
    table.add_row(
        "Compatibility Score",
        f"{'[red]' if score < 50 else '[yellow]' if score < 75 else '[green]'}{score}%[/]",
    )
    console.print(table)

    # Show matched keywords
    if matched:
        console.print(
            Panel(
                ", ".join(sorted(matched)),
                title="✓ Matched Keywords",
                border_style="green",
            )
        )

    # Show missing keywords
    if missing:
        priority_missing = [k for k in sorted(missing) if len(k) > 5]
        console.print(
            Panel(
                ", ".join(priority_missing[:30]),
                title=f"✗ Missing Keywords ({len(missing)} total, showing top 30)",
                border_style="red",
            )
        )

    # Tips
    if score < 70:
        console.print("\n[yellow]Tips to improve your score:[/yellow]")
        console.print("  • Add missing technical skills if you have them")
        console.print("  • Use industry-standard terminology from the job description")
        console.print(
            "  • Ensure all relevant experience is listed with proper keywords"
        )
