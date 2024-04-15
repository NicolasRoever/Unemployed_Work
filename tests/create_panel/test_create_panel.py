from unemployed_work.create_panel.create_panel import prepare_individual_file_for_panel, add_variable_from_family_file_to_panel

from unemployed_work.config import FAMILY_INTERVIEW_ID_MATCHING, FAMILY_STATUS_MAPPING

import pandas as pd
import pytest

def test_add_variable_from_family_file_to_panel():


    test_data_panel = pd.DataFrame({
    "Individual_ID": [1001, 1002, 1001, 1002],
    'Family_Interview_Number_Variable':["ER30020","ER30020", "ER30043", "ER30043"],
    'Family_Interview_Number': [1597, 1597, 1331, 1331],
       "Year": [1969, 1969, 1970, 1970],
    "Relation_To_Head_Variable_Name": ['ER30022','ER30022', 'ER30045', 'ER30045'], 
        "Relation_To_Head_Value": [1, 2, 1,2],
         "Relation_To_Head_String": ['Head', 'Spouse', 'Head', 'Spouse']

    })

    test_data_family = pd.DataFrame({
    "V3": [1597, 1331],
    "V74": [2000, 0], 
    "V75": [0, 1000]

    })


    head_variables = {
        "Labor_Income_Previous_Year":{
    1969: 'V74'}

    }

    spouse_variables ={ "Labor_Income_Previous_Year":{ 1969: 'V75',
    1970: 'V516'}}

    family_interview_number_mapping_df = pd.DataFrame({
    'Year': [1969, 1970],
    'Family_File': ['V3', 'V1102'] })

    expected_result = pd.DataFrame({
    "Individual_ID": [1001, 1002, 1001, 1002],
    'Family_Interview_Number_Variable':["ER30020","ER30020", "ER30043", "ER30043"],
    'Family_Interview_Number': [1597, 1597, 1331, 1331],
       "Year": [1969, 1969, 1970, 1970],
    "Relation_To_Head_Variable_Name": ['ER30022','ER30022', 'ER30045', 'ER30045'], 
        "Relation_To_Head_Value": [1, 2, 1,2],
        "Relation_To_Head_String": ['Head', 'Spouse', 'Head', 'Spouse'], 
        "Labor_Income_Previous_Year": [2000, 1000, 2000, 1000]
    })

    breakpoint()
    actual_result = add_variable_from_family_file_to_panel(test_data_panel, test_data_family, 1969,"Labor_Income_Previous_Year", head_variables, spouse_variables, family_interview_number_mapping_df)

    pd.testing.assert_frame_equal(actual_result, expected_result, check_dtype=False)


def test_prepare_individual_file_for_panel():

    test_data = pd.DataFrame({
    "ER30001": [1.0, 1.0],
    "ER30002": [1.0, 2.0],
    "ER30020": [1597.0, 1597.0],
    "ER30043": [1331.0, 1331.0],
    "ER30022": [1.0, 2.0],
    "ER30045": [1, 2]})
    
    family_status_mapping = {
    1:"Head",
    2:"Wife"
    }

    family_status_variables_to_years_mapping = {
    1969: 'ER30022',
    1970: 'ER30045'
     }

    family_interview_id_matching = pd.DataFrame({
    'Year': [1969, 1970],
    'Family_File': ['V442', 'V1102'],
    'Individual_File': ['ER30020', 'ER30043']
    })

    expected_result = pd.DataFrame({
    "Individual_ID": [1001, 1002, 1001, 1002],
    'Family_Interview_Number_Variable':["ER30020","ER30020", "ER30043", "ER30043"],
    'Family_Interview_Number': [1597, 1597, 1331, 1331],
       "Year": [1969, 1969, 1970, 1970],
    "Relation_To_Head_Variable_Name": ['ER30022','ER30022', 'ER30045', 'ER30045'], 
        "Relation_To_Head_Value": [1, 2, 1,2]

    })


    actual_result = prepare_individual_file_for_panel(test_data, family_interview_id_matching, family_status_variables_to_years_mapping)

    pd.testing.assert_frame_equal(actual_result, expected_result, check_dtype=False)