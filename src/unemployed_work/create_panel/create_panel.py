import numpy as np
import pandas as pd


def merge_panel_with_single_family_file(panel, family_file, variable_dictionary_head, variable_dictionary_spouse):
    """This function takes the panel from the prepare_individual_file_for_panel function and merges it with the family file from a single wave.

    Parameters
    ----------
    panel : pd.DataFrame
        The panel from the prepare_individual_file_for_panel function.
    family_file : pd.DataFrame
        The family file from a single wave as downloaded from PSID and preprocessed in R (I know this is a bit messy :/)
    variable_dictionary_head : dict
        A dictionary mapping the variable names for the head of the family to the year
    variable_dictionary_spouse : dict
        A dictionary mapping the variable names for the spouse of the family to the year
    
    Returns
    -------
    pd.DataFrame
        The merged panel with added columns for the given variables
    """

    pass


def add_variables_from_family_file_to_panel(panel, family_file, year,variable_name, head_variables, spouse_variables,family_interview_number_mapping_df):
    """This function takes the panel from the prepare_individual_file_for_panel function and adds a variable from the family file to it.

    Parameters
    ----------
    panel : pd.DataFrame
        The panel from the prepare_individual_file_for_panel function.
    family_file : pd.DataFrame
        The family file from a single wave as downloaded from PSID and preprocessed in R (I know this is a bit messy :/)
    year : int
    variable_name : str
        The name of the variable you want to add to the panem
    variable_PSID_variable_name_mapping : dict
        A dictionary mapping the variable names to the variable names in the PSID data
    
    Returns
    -------
    pd.DataFrame
        The panel with the added variable
    """

    if variable_name not in panel.columns:
        panel[variable_name] = np.nan

    head_PSID_variable_name = head_variables[variable_name][year]

    spouse_PSID_variable_name = spouse_variables[variable_name][year]

    family_interview_number_variable_family_file = family_interview_number_mapping_df.loc[family_interview_number_mapping_df["Year"] == year, "Family_File"].values[0]

    panel_merged = pd.merge(panel, family_file[[family_interview_number_variable_family_file, head_PSID_variable_name, spouse_PSID_variable_name]], left_on="Family_Interview_Number", right_on=family_interview_number_variable_family_file, how="left", validate="m:1")

    return panel_merged





def prepare_individual_file_for_panel(individual_file, interview_ids_dataframe, family_status_variables_to_year_mapping):
    """This function takes the individual file donwloaded from the PSID website and prepares it to be matched with the data from the family files. 

    Parameters
    ----------
    individual_file : pd.DataFrame
        The individual file downloaded from the PSID website.
    list_interview_ids : pd.DataFrame
      Dataframe with a column of the year, the corresponding variable name for the family interview id and the corresponding variable name for the individual interview id
    family_status_mapping : dict
    This dictionary maps the family status codes to the roles in the family (head/spouse)

    Returns
    -------
    pd.DataFrame
        The prepared individual file
        colums: Individual_ID (This is the 1968 fmaily number times 1000 plus the person number)
        Family_ID(This is the 1968 family number)
        Year (The year of the interview)
        Interview_ID: The interview id of the family interview
        Individual_Role: The role of the individual in the family
    """
    individual_file["Individual_ID"] = (individual_file["ER30001"] * 1000) + individual_file["ER30002"].astype(int)

    panel_with_individual_id_and_family_interview_number = create_panel_with_individual_id_and_interview_number(individual_file, interview_ids_dataframe)

    panel_with_individual_id_and_family_role = create_panel_with_individual_id_and_family_role(individual_file, family_status_variables_to_year_mapping)

    output_panel = panel_with_individual_id_and_family_interview_number.merge(panel_with_individual_id_and_family_role, on=["Individual_ID", "Year"], how="left", validate="1:1")

    return output_panel



def create_panel_with_individual_id_and_interview_number(individual_file, interview_ids_dataframe):
    """
    Transforms the PSID individual file by reshaping it and adding a Year column.

    Parameters:
    individual_file (pd.DataFrame): The individual file to transform.
    interview_ids_dataframe (pd.DataFrame): A DataFrame containing interview IDs and years.

    Returns:
    pd.DataFrame: The transformed individual file.
    """
    # Create a list of family IDs variables
    family_ids_variables_list = list(interview_ids_dataframe["Individual_File"])

    # Select relevant columns from the individual file
    family_interview_numbers_dataset = individual_file[["Individual_ID", "ER30020", "ER30043"]]

    # Reshape the dataset from wide to long format
    family_file_interiew_number_long = family_interview_numbers_dataset.melt(
        id_vars=["Individual_ID"], 
        value_vars=family_ids_variables_list, 
        var_name="Family_Interview_Number_Variable", 
        value_name="Family_Interview_Number"
    )

    # Add a Year column by mapping the Family_Interview_Number_Variable column to years
    family_file_interiew_number_long["Year"] = family_file_interiew_number_long["Family_Interview_Number_Variable"].map(
        dict(zip(interview_ids_dataframe["Individual_File"], interview_ids_dataframe["Year"]))
    )

    return family_file_interiew_number_long


def create_panel_with_individual_id_and_family_role(individual_file, family_status_variable_names):
    """
    Transforms a dataset by reshaping it and adding a Year column.

    Parameters:
    test_data (pd.DataFrame): The dataset to transform.
    FAMILY_STATUS_VARIABLE_NAMES (dict): A dictionary mapping variable names to years.

    Returns:
    pd.DataFrame: The transformed dataset.
    """
    # Select relevant columns from the dataset
    relation_to_head_dataset = individual_file[["Individual_ID"] + list(family_status_variable_names.values())]

    # Reshape the dataset from wide to long format
    relation_to_head_long = relation_to_head_dataset.melt(
        id_vars=["Individual_ID"], 
        value_vars=list(family_status_variable_names.values()), 
        var_name="Relation_To_Head_Variable_Name", 
        value_name="Relation_To_Head_Value"
    )

    # Add a Year column by mapping the Relation_To_Head_Variable_Name column to years
    relation_to_head_long["Year"] = relation_to_head_long["Relation_To_Head_Variable_Name"].map(
        {value: key for key, value in family_status_variable_names.items()}
    )

    return relation_to_head_long