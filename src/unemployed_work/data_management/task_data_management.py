"""Tasks for managing the data."""

from pathlib import Path

import pandas as pd

from unemployed_work.config import BLD, SRC
from unemployed_work.data_management import clean_data



def task_clean_data_python(
    depends_on= SRC / 'data' / 'PSIDSHELF_1968_2019_LONG.dta',
    produces=BLD / "python" / "data" / "psid_clean.pkl",
):
    """Clean the data (Python version)."""
    raw_data = pd.read_stata(depends_on)

    cleaned_data = clean_data(raw_data)

    cleaned_data.to_pickle(produces)
