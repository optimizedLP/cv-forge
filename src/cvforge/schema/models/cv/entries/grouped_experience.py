"""Grouped experience entry: multiple positions at one company.

Why:
    Users who held different roles at the same company (e.g., promoted from
    Engineer to Senior Engineer) want them grouped under a single company
    header rather than repeating the company name for each stint.
"""

from typing import Literal

import pydantic
import pydantic_core

from cvforge.schema.models.base import BaseModelWithExtraKeys
from cvforge.schema.models.cv.entries.bases.entry import BaseEntry
from cvforge.schema.models.cv.entries.bases.entry_with_complex_fields import (
    ExactDate,
    get_date_object,
)
from cvforge.schema.models.cv.entries.bases.entry_with_date import ArbitraryDate
from cvforge.schema.pydantic_error_handling import CustomPydanticErrorTypes
from cvforge.schema.models.validation_context import get_current_date


class PositionEntry(BaseModelWithExtraKeys):
    """A single position within a grouped experience entry.

    Each position has its own title, date range, and optional highlights,
    all rendered under the shared company header.
    """

    model_config = pydantic.ConfigDict(
        extra="allow",
        validate_default=True,
        json_schema_extra={"description": None},
    )

    position: str = pydantic.Field(
        examples=["Software Engineer", "Senior Engineer", "Team Lead"],
    )
    start_date: ExactDate | None = pydantic.Field(
        default=None,
        description="The start date in YYYY-MM-DD, YYYY-MM, or YYYY format.",
        examples=["2020-09-24", "2020-09", "2020"],
    )
    end_date: ExactDate | Literal["present"] | None = pydantic.Field(
        default=None,
        description=(
            'The end date in YYYY-MM-DD, YYYY-MM, or YYYY format. Use "present" for'
            " ongoing positions, or omit it to indicate the position is ongoing."
        ),
        examples=["2024-05-20", "2024-05", "2024", "present"],
    )
    date: ArbitraryDate | None = pydantic.Field(
        default=None,
        description=(
            "The date of this position in YYYY-MM-DD, YYYY-MM, or YYYY format, or any"
            " custom text like 'Fall 2023'. Use this for single-day or imprecise dates."
            " For date ranges, use `start_date` and `end_date` instead."
        ),
        examples=["2020-09-24", "2020-09", "2020", "Fall 2023"],
    )
    location: str | None = pydantic.Field(
        default=None,
        examples=["Istanbul, Türkiye", "New York, NY", "Remote"],
    )
    summary: str | None = pydantic.Field(
        default=None,
        examples=[
            "Led a team of 5 engineers to develop innovative solutions.",
        ],
    )
    highlights: list[str] | None = pydantic.Field(
        default=None,
        description=(
            "Bullet points for key achievements, responsibilities, or contributions."
        ),
        examples=[
            [
                "Increased system performance by 40% through optimization.",
                "Mentored 3 junior developers and conducted code reviews.",
            ]
        ],
    )

    @pydantic.model_validator(mode="after")
    def check_and_adjust_dates(self, info: pydantic.ValidationInfo) -> "PositionEntry":
        date_is_provided = self.date is not None
        start_date_is_provided = self.start_date is not None
        end_date_is_provided = self.end_date is not None

        if date_is_provided:
            self.start_date = None
            self.end_date = None
        elif not start_date_is_provided and end_date_is_provided:
            self.date = self.end_date
            self.start_date = None
            self.end_date = None
        elif start_date_is_provided and not end_date_is_provided:
            self.end_date = "present"

        if self.start_date and self.end_date:
            current_date = get_current_date(info)
            start_date_object = get_date_object(self.start_date, current_date)
            end_date_object = get_date_object(self.end_date, current_date)
            if start_date_object > end_date_object:
                raise pydantic_core.PydanticCustomError(
                    CustomPydanticErrorTypes.other.value,
                    "`start_date` cannot be after `end_date`. The `start_date` is"
                    " {start_date} and the `end_date` is {end_date}.",
                    {
                        "start_date": self.start_date,
                        "end_date": self.end_date,
                    },
                )

        return self


class GroupedExperienceEntry(BaseEntry):
    """Multiple positions at one company, rendered under a shared company header.

    Why:
        When a person has held different roles at the same company, grouping
        them under a single company header produces a cleaner, more compact
        layout than repeating the company name for each entry.
    """

    company: str = pydantic.Field(
        examples=["Microsoft", "Google", "Princeton Plasma Physics Laboratory"],
    )
    positions: list[PositionEntry] = pydantic.Field(
        min_length=1,
        description="List of positions held at this company.",
        examples=[
            [
                {
                    "position": "Software Engineer",
                    "start_date": "2020-01",
                    "end_date": "2022-06",
                    "highlights": [
                        "Built the payments system from scratch",
                        "Scaled backend to handle 10x traffic growth",
                    ],
                },
                {
                    "position": "Senior Software Engineer",
                    "start_date": "2022-07",
                    "end_date": "present",
                    "highlights": [
                        "Led migration to microservices architecture",
                        "Mentored 4 junior engineers",
                    ],
                },
            ]
        ],
    )
    location: str | None = pydantic.Field(
        default=None,
        examples=["Istanbul, Türkiye", "New York, NY", "Remote"],
    )
    summary: str | None = pydantic.Field(
        default=None,
        examples=[
            "Leading the engineering team building next-generation products.",
        ],
    )
