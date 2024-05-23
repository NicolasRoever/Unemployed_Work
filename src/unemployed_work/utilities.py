"""Utilities used in various parts of the project."""

import yaml
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def _make_missing_values_heatmap(data, data_name, index=None):
    """Create a heatmap to visualize missing values in a DataFrame."""
    if index is not None:
        data = data.set_index(index)

    plt.figure(figsize=(10, 6))
    sns.heatmap(data.isnull(), cbar=False, cmap="viridis")
    plt.title("Missing Values in Dataset " + data_name)
    plt.show()


def _print_na_percentages_for_all_columns(df):
    for col in df.columns:
        na_percentage = round(df[col].isna().mean() * 100, 2)
        print(f'{col}: {na_percentage}% NA')