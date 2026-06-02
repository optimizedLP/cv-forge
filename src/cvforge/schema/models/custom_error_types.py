from enum import StrEnum


class CustomPydanticErrorTypes(StrEnum):
    entry_validation = "cvforge_entry_validation_error"
    other = "cvforge_other_error"
