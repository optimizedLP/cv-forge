"""LinkedIn to CV YAML converter command for CV-Forge."""

import pathlib
import re
from typing import Annotated

import typer
from rich.console import Console

from ..app import app
from ..error_handler import handle_user_errors

console = Console()


def parse_linkedin_text(text: str) -> dict:
    """Parse LinkedIn profile text into structured CV data.

    Expects text pasted from a LinkedIn profile page.
    Detects sections by looking for common LinkedIn headers.
    """
    result = {
        "name": "",
        "headline": "",
        "location": "",
        "experience": [],
        "education": [],
        "skills": [],
    }

    lines = text.strip().split("\n")
    lines = [l.strip() for l in lines if l.strip()]

    if not lines:
        return result

    # First non-empty line is typically the name
    result["name"] = lines[0]

    # Second line is typically the headline/title
    if len(lines) > 1 and not _is_section_header(lines[1]):
        result["headline"] = lines[1]

    # Look for location line (usually contains city, state or "·")
    for i, line in enumerate(lines[:10]):
        if "·" in line or re.search(r"\b[A-Z][a-z]+,\s*[A-Z]{2}\b", line):
            # Extract location part
            parts = line.split("·")
            for part in parts:
                part = part.strip()
                if re.search(r"\b[A-Z][a-z]+,\s*[A-Z]{2}\b", part) or re.search(
                    r"\b[A-Z][a-z]+ Area\b", part
                ):
                    result["location"] = part
                    break
            break

    # Parse sections
    current_section = None
    current_entries = []
    current_entry = {}

    section_patterns = {
        "experience": re.compile(
            r"(?i)^(experience|work experience|professional experience)$"
        ),
        "education": re.compile(r"(?i)^(education|academic background)$"),
        "skills": re.compile(r"(?i)^(skills|top skills|expertise)$"),
    }

    i = 0
    while i < len(lines):
        line = lines[i]

        # Check if line is a section header
        new_section = None
        for section_name, pattern in section_patterns.items():
            if pattern.match(line):
                new_section = section_name
                break

        if new_section:
            # Save previous section data
            if current_section == "experience" and current_entries:
                result["experience"] = current_entries
            elif current_section == "education" and current_entries:
                result["education"] = current_entries
            elif current_section == "skills" and current_entries:
                result["skills"] = current_entries

            current_section = new_section
            current_entries = []
            current_entry = {}
            i += 1
            continue

        if current_section == "experience":
            # LinkedIn shows position title first (bold), then company name below.
            # line = position title, lines[i+1] = company name
            if (
                i + 1 < len(lines)
                and lines[i + 1]
                and not line.startswith("·")
                and not line.endswith("·")
            ):
                if current_entry:
                    current_entries.append(current_entry)
                position_title = line
                company_name = lines[i + 1]
                location = ""
                date = ""
                # Look ahead for location/date info
                if i + 2 < len(lines) and "·" in lines[i + 2]:
                    meta = lines[i + 2]
                    parts = [p.strip() for p in meta.split("·")]
                    date = parts[0] if parts else ""
                    location = parts[-1] if len(parts) > 1 else ""

                current_entry = {
                    "company": company_name,
                    "position": position_title,
                    "location": location,
                    "start_date": date.split(" - ")[0].strip()
                    if " - " in date
                    else date,
                    "end_date": date.split(" - ")[1].strip()
                    if " - " in date
                    else "present",
                    "highlights": [],
                }
                i += 2
                continue
            if current_entry and line and not _is_section_header(line):
                current_entry.setdefault("highlights", []).append(
                    line.lstrip("·- ").strip()
                )
        elif current_section == "education":
            # Detect school entry
            if (
                i + 1 < len(lines)
                and not line.startswith("·")
                and not _is_section_header(lines[i + 1])
                and not _is_section_header(line)
            ):
                if current_entry:
                    current_entries.append(current_entry)
                school = line
                degree = lines[i + 1]
                date = ""
                if i + 2 < len(lines) and "·" in lines[i + 2]:
                    date = lines[i + 2].split("·")[0].strip()

                current_entry = {
                    "institution": school,
                    "area": degree,
                    "degree": "",
                    "date": date,
                }
                i += 2
                continue
        elif current_section == "skills":
            if line and not _is_section_header(line):
                current_entries.append(line)

        i += 1

    # Save final section
    if current_section == "experience" and current_entry:
        current_entries.append(current_entry)
        result["experience"] = current_entries
    elif current_section == "education" and current_entry:
        current_entries.append(current_entry)
        result["education"] = current_entries
    elif current_section == "skills" and current_entries:
        result["skills"] = current_entries

    return result


def _is_section_header(line: str) -> bool:
    """Check if a line looks like a LinkedIn section header."""
    section_keywords = [
        "experience",
        "education",
        "skills",
        "about",
        "licenses",
        "certifications",
        "volunteering",
        "projects",
        "honors",
        "languages",
        "recommendations",
    ]
    line_lower = line.lower().strip()
    return line_lower in section_keywords


def generate_yaml(data: dict, theme: str) -> str:
    """Generate a CV YAML string from parsed LinkedIn data."""
    name = data.get("name", "Your Name")
    headline = data.get("headline", "")
    location = data.get("location", "")

    yaml_lines = [
        "# yaml-language-server: $schema=../schema.json",
        "cv:",
        f"  name: {name}",
    ]

    if headline:
        yaml_lines.append(f"  headline: {headline}")
    if location:
        yaml_lines.append(f"  location: {location}")

    yaml_lines.extend(
        [
            "  email:",
            "  phone:",
            "  website:",
            "  social_networks:",
            "    - network: LinkedIn",
            "      username: yourusername",
            "    - network: GitHub",
            "      username: yourusername",
            "  sections:",
        ]
    )

    # Experience
    if data.get("experience"):
        yaml_lines.append("    experience:")
        for exp in data["experience"]:
            yaml_lines.append(f"      - company: {exp.get('company', '')}")
            position = exp.get("position", "").replace(":", "-")
            yaml_lines.append(f"        position: {position}")
            yaml_lines.append(f"        location: {exp.get('location', '')}")
            yaml_lines.append(f"        start_date: {exp.get('start_date', '')}")
            yaml_lines.append(f"        end_date: {exp.get('end_date', 'present')}")
            yaml_lines.append("        highlights:")
            for h in exp.get("highlights", []):
                h_clean = h.replace(":", "-")
                yaml_lines.append(f"          - '{h_clean}'")

    # Education
    if data.get("education"):
        yaml_lines.append("    education:")
        for edu in data["education"]:
            yaml_lines.append(f"      - institution: {edu.get('institution', '')}")
            yaml_lines.append(f"        area: {edu.get('area', '')}")
            yaml_lines.append(f"        degree: {edu.get('degree', '')}")
            if edu.get("date"):
                yaml_lines.append(f"        date: {edu.get('date', '')}")

    # Skills
    if data.get("skills"):
        yaml_lines.append("    skills:")
        for skill in data["skills"][:10]:
            skill_clean = skill.replace(":", "-")
            yaml_lines.append(f"      - label: {skill_clean}")
            yaml_lines.append("        details: ''")

    yaml_lines.extend(
        [
            "",
            "design:",
            f"  theme: {theme}",
            "",
            "locale:",
            "  language: english",
        ]
    )

    return "\n".join(yaml_lines)


@app.command(
    name="linkedin",
    help=(
        "Convert LinkedIn profile text to CV YAML. Example:"
        " [yellow]cvforge linkedin --paste[/yellow]"
    ),
)
@handle_user_errors
def cli_command_linkedin(
    output: Annotated[
        pathlib.Path | None,
        typer.Option(
            "--output",
            "-o",
            help="Output path for the generated YAML file.",
        ),
    ] = None,
    paste: Annotated[
        bool,
        typer.Option(
            "--paste",
            "-p",
            help="Read LinkedIn profile text from stdin (paste and press Ctrl+D).",
        ),
    ] = False,
    file: Annotated[
        pathlib.Path | None,
        typer.Option(
            "--file",
            "-f",
            help="Read LinkedIn profile text from a file.",
        ),
    ] = None,
    theme: Annotated[
        str,
        typer.Option(
            "--theme",
            "-t",
            help="Theme to use in the generated YAML.",
        ),
    ] = "classic",
) -> None:
    """Convert LinkedIn profile text into a CV-Forge YAML input file.

    Paste your LinkedIn profile text (from your profile page) and get
    a ready-to-use YAML input file.

    How to use:
    1. Go to your LinkedIn profile
    2. Copy all visible text (Cmd+A, Cmd+C)
    3. Run: cvforge linkedin --paste
    4. Paste the text and press Ctrl+D
    """
    if paste:
        console.print("[bold cyan]Paste your LinkedIn profile text below.[/bold cyan]")
        console.print(
            "[dim](Copy from your LinkedIn profile, paste here, then press"
            " Ctrl+D)[/dim]\n"
        )
        try:
            import sys

            text = sys.stdin.read()
        except KeyboardInterrupt:
            console.print("\n[yellow]Cancelled.[/yellow]")
            raise typer.Exit(0)
    elif file:
        if not file.exists():
            console.print(f"[red]File not found: {file}[/red]")
            raise typer.Exit(1)
        text = file.read_text(encoding="utf-8")
    else:
        console.print(
            "[red]Use --paste to paste text or --file to read from a file.[/red]"
        )
        raise typer.Exit(1)

    if not text.strip():
        console.print("[red]No text provided.[/red]")
        raise typer.Exit(1)

    console.print("\n[bold]Parsing LinkedIn profile text...[/bold]")
    parsed = parse_linkedin_text(text)

    # Show summary of what was found
    console.print(f"  📛 Name: [bold]{parsed['name']}[/bold]")
    console.print(f"  💼 Experiences: [bold]{len(parsed['experience'])}[/bold]")
    console.print(f"  🎓 Education: [bold]{len(parsed['education'])}[/bold]")
    console.print(f"  🛠️  Skills: [bold]{len(parsed['skills'])}[/bold]")

    yaml_content = generate_yaml(parsed, theme)

    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(yaml_content, encoding="utf-8")
        console.print(f"\n[green]✓ YAML saved to: {output}[/green]")
        console.print(
            f"\n[yellow]Next step:[/yellow] [cyan]cvforge render {output}[/cyan]"
        )
    else:
        console.print("\n[bold]Generated YAML:[/bold]")
        console.print(yaml_content)

    console.print(
        "\n[dim]Note: LinkedIn text parsing is best-effort. Review and edit the"
        " generated YAML before rendering.[/dim]"
    )
