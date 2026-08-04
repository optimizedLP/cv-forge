from datetime import date as Date

from cvforge.renderer.templater.templater import render_full_template
from cvforge.schema.models.cv.cv import Cv
from cvforge.schema.models.cv.entries.experience import ExperienceEntry
from cvforge.schema.models.cv.entries.grouped_experience import (
    GroupedExperienceEntry,
    PositionEntry,
)
from cvforge.schema.models.cvforge_model import RenderCVModel
from cvforge.schema.models.settings.settings import Settings


def create_experience_model(theme: str) -> RenderCVModel:
    """Build a model with a long Experience highlight for theme layout testing."""
    cv = Cv(
        name="John Doe",
        sections={
            "Experience": [
                ExperienceEntry(
                    company="Example Company",
                    position="Research Engineer",
                    start_date="2020-01",
                    end_date="2024-01",
                    highlights=[
                        "Led a long-running research and engineering initiative that improved system reliability across multiple production teams."
                    ],
                )
            ]
        },
    )
    return RenderCVModel(
        cv=cv,
        design={"theme": theme},
        settings=Settings(current_date=Date(2025, 1, 1)),
    )


def test_standard_reserves_date_column_for_experience_highlights():
    """Standard wraps Experience highlights in a main-column-only row."""
    standard_output = render_full_template(
        create_experience_model("standard"), "typst"
    )
    academic_output = render_full_template(create_experience_model("academic"), "typst")

    assert "columns: (1fr, 3.5cm)" in standard_output
    assert "#v(0.2em)" in standard_output
    assert "columns: (1fr, 3.5cm)" not in academic_output
    assert "#v(0.2em)" not in academic_output


def test_standard_applies_spacing_to_grouped_experience_highlights():
    """Standard applies the same protected row to grouped Experience positions."""
    cv = Cv(
        name="John Doe",
        sections={
            "Experience": [
                GroupedExperienceEntry(
                    company="Example Company",
                    positions=[
                        PositionEntry(
                            position="Research Engineer",
                            start_date="2020-01",
                            end_date="2024-01",
                            highlights=["Led a long-running research initiative."],
                        )
                    ],
                )
            ]
        },
    )
    model = RenderCVModel(
        cv=cv,
        design={"theme": "standard"},
        settings=Settings(current_date=Date(2025, 1, 1)),
    )

    output = render_full_template(model, "typst")

    assert "columns: (1fr, 3.5cm)" in output
    assert "#v(0.2em)" in output
