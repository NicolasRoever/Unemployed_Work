import numpy as np
import pandas as pd
import pytest
from src.unemployed_work.config import TEST_DIR
from src.unemployed_work.data_management.clean_data import create_dataset_for_occupation_unemployment_regression, calculate_employment_length


def test_create_dataset_for_occupation_unemployment_regression():

    test_input = pd.DataFrame({
        'PNum': [1, 1, 1, 2, 2, 2],
        'Year': [1970, 1971, 1972, 1970, 1971, 1972], 
        'Unemployment_Indicator': [0, 1, 0, 1, 0, 1],
        'Occupation_Category': ['0', 'A', '0', 'B', 'B', '0']
    })



    expected_output = pd.DataFrame({
        'PNum':[1,2], 
        'Next_Year_Occupation_Category':['0', 'B' ],
        'Employment_Length':[np.NaN,1 ]
    })

    actual_output = create_dataset_for_occupation_unemployment_regression(test_input)[['PNum', 'Next_Year_Occupation_Category', 'Employment_Length']].reset_index(drop=True)

    pd.testing.assert_frame_equal(actual_output, expected_output.reset_index(drop=True), 
                                  check_dtype=False, check_like=True, check_index_type=False, check_column_type=False, check_frame_type=False, check_datetimelike_compat=False)
    

    

def test_calculate_employment_length():
    # Create a sample DataFrame
    test_input = pd.DataFrame({
        'Change_Unemployment_to_Employment': [1, 0, 0, 0, 1, 0],
        'Unemployment_Indicator': [0, 1, 0, 1, 1, 0],
        'Next_Year_Unemployment_Indicator': [1, 0, 1, 0, 0, np.NaN]
    })

    expected_output = [1,np.NaN]

    # Call the function with the sample DataFrame
    actual_output = calculate_employment_length(test_input)

    # Check the result
    assert expected_output == actual_output



def test_create_dataset_for_occupation_unemployment_regression_person_with_multiple_lenghts():

    test_input = pd.DataFrame({
        'PNum': [1, 1, 1, 1, 1, 1],
        'Year': [1970, 1971, 1972, 1973, 1974, 1975], 
        'Unemployment_Indicator': [0, 1, 0, 1, 0, 1],
        'Occupation_Category': ['A', '0', 'C', '0', 'D', '0']
    })



    expected_output = pd.DataFrame({
        'PNum':[1,1], 
        'Next_Year_Occupuation_Category':['C', 'D' ],
        'Employment_Length':[1,1]
    })

    actual_output = create_dataset_for_occupation_unemployment_regression(test_input)[['PNum', 'Next_Year_Occupation_Category', 'Employment_Length']]



    pd.testing.assert_frame_equal(actual_output, expected_output, 
                                  check_dtype=False, check_like=True, check_index_type=False, check_column_type=False, check_frame_type=False, check_datetimelike_compat=False)
