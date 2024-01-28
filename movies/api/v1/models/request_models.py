from enum import Enum
from typing import Optional

from fastapi import APIRouter, HTTPException, Query, Request
from pydantic import BaseModel, conint


class CaseInsensitiveEnum(Enum):
    """
    CaseInsensitiveEnum
    -------------

    CaseInsensitiveEnum class provides a way to handle case-insensitive value lookup.

    Methods:
        _missing_(value):
            Returns the enum member for a case-insensitive value lookup

            Args:
                value(str): The case-insensitive value to be looked up

            Returns:
                The enum member corresponding to the provided value, if found. Otherwise, None.
    """

    @classmethod
    def _missing_(cls, value):
        for member in cls:
            if member.value == value.upper():
                return member


class Language(CaseInsensitiveEnum):
    EN = "EN"
    TA = "TA"
    HI = "HI"
    ML = "ML"
    TL = "TL"
    KN = "KN"
    KO = "KO"


class SortBy(CaseInsensitiveEnum):
    POPULARITY = "POPULARITY"
    RELEASE_DATE = "RELEASE_DATE"
    TITLE = "TITLE"


class SortDirection(CaseInsensitiveEnum):
    ASCENDING = "ASC"
    DESCENDING = "DESC"
