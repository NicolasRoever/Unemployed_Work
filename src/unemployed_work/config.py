"""All the general configuration of the project."""
from pathlib import Path

SRC = Path(__file__).parent.resolve()
BLD = SRC.joinpath("..", "..", "bld").resolve()

TEST_DIR = SRC.joinpath("..", "..", "tests").resolve()
PAPER_DIR = SRC.joinpath("..", "..", "paper").resolve()

GROUPS = ["marital_status", "qualification"]

__all__ = ["BLD", "SRC", "TEST_DIR", "GROUPS"]


import pandas as pd

OCCUPATION_CODE_MAPPING_1970 = {
    "1-99": "Management, Business, and Financial Operations",
    "100-199": "Professional and Technical Occupations",
    "200-299": "Healthcare Practitioners and Technical Occupations",
    "300-399": "Service Occupations",
    "400-499": "Sales and Office Occupations",
    "500-599": "Farming, Fishing, and Forestry Occupations",
    "600-699": "Construction and Extraction Occupations",
    "700-799": "Installation, Maintenance, and Repair Occupations",
    "800-899": "Production Occupations",
    "900-999": "Transportation and Material Moving Occupations"
}

OCCUPATION_CODE_MAPPING_UNIVERSAL= {
    1: "Managers, directors and senior officials",
    2: "Professional occupations",
    3: "Associate professional and technical occupations",
    4: "Administrative and secretarial occupations",
    5: "Skilled trades occupations",
    6: "Caring, leisure and other service occupations",
    7: "Sales and customer service occupations",
    8: "Process, plant and machine operatives",
    9: "Elementary occupations"
}