"""Function(s) for cleaning the data set(s)."""

import pandas as pd
import numpy as np

from unemployed_work.config import OCCUPATION_CODE_MAPPING_UNIVERSAL


def clean_data(data, occupation_code_mapping_universal):
    """Clean data set.

    Args:
        data (pandas.DataFrame): The raw data downloaded 

    Returns:
        pandas.DataFrame: The cleaned data set.
    """
  
    clean_data = pd.DataFrame()

    clean_data['ID'] = data['ID']
    clean_data['PNum'] = data['PNUM']
    clean_data["Year_Survey"] = data['YEAR']#.astype('int')
    clean_data['Sex'] = data['SEX']
    clean_data['Birth_Year'] = data['BIRTHYEAR']#.astype('int')
    clean_data['Age'] = clean_data['Year_Survey'] - clean_data['Birth_Year']
    clean_data['Education_Years'] = data['EDUYEAR']

    #Earnings
    clean_data['Real_Earnings'] = clean_real_earnings_column(data['EARNINDR'])
    clean_data['Real_Earnings_With_Partner'] = data['EARNINDRRC']
    clean_data['Employment_Status_First'] = data['EMPWORK']
    clean_data['Employment_Status_Multi'] = data['EMPWORKMM']
    clean_data['Total_Family_Income_Real'] = data['INCFAMR']
    clean_data['Unemployment_Indicator'] = np.where(pd.isnull(clean_data['Real_Earnings']), np.nan, np.where(clean_data['Real_Earnings'] <= (1523/2), 1, 0))

    #Occupation

    clean_data['Occupation_First_Mention_1970'] = data['OCC1970C']
    clean_data['Occupation_First_Mention_1970_Category'] =  clean_data['Occupation_First_Mention_1970'].astype(str).str[0].astype(int).map(occupation_code_mapping_universal)

    clean_data['Occupation_First_Mention_2000'] = data['OCC2000C1M']
    clean_data['Occupation_First_Mention_2000_Category'] = data['Occupation_First_Mention_2000'].astype(str).str[0].astype(int).map(occupation_code_mapping_universal)
    clean_data['Occupation_Second_Mention_2000'] = data['OCC2000C2M']
    clean_data['Occupation_Third_Mention_2000'] = data['OCC2000C3M']
    clean_data['Occupation_Fourth_Mention_2000'] = data['OCC2000C4M']


    clean_data['Occupation_First_Mention_2010'] = data['OCC2010C1M']
    clean_data['Occupation_First_Mention_2010'] = data['OCC2000C1M']
    clean_data['Occupation_First_Mention_2010_Only_Code'] = data['Occupation_First_Mention_2010'].str.extract(r'=(\d{4})')
    clean_data['Occupation_First_Mention_2010_Category'] = clean_data['Occupation_First_Mention_2010_Only_Code'].astype(int).map(occupation_code_mapping_universal)
    clean_data['Occupation_Second_Mention_2010'] = data['OCC2010C2M']
    clean_data['Occupation_Third_Mention_2010'] = data['OCC2010C3M']
    clean_data['Occupation_Fourth_Mention_2010'] = data['OCC2010C4M']

    data['Occupation_Code'] = data[['Occupation_First_Mention_2010_Category', 'Occupation_First_Mention_2000_Category', 'Occupation_First_Mention_1970_Category']].apply(get_occupation_code_from_either_year, axis=1)

    return clean_data


def clean_real_earnings_column(column):
    """This function takes in the real earnings column from the raw PSID data and cleans it."""

    return column.replace('Zero dollars', 0).astype('float')


def create_dataset_for_occupation_unemployment_regression(data):
    """This function takes in the cleaned data and returns a dataset that can be used for the occupation unemployment regression.

    Args:
        data (pandas.DataFrame): The cleaned data set.

    Returns:
        pandas.DataFrame: The data set for the occupation unemployment regression.
        Columns:
        - Occupation (Category)
        - Year (int): This is the year of the last unemployment period
        - Employment_Length: Length of the subsequent employment period
        """
    
    grouped_data = prepare_clean_data_to_calculate_employment_length(data)


    regression_data = create_regression_data_from_grouped_data(grouped_data)

    return regression_data
  


def create_regression_data_from_grouped_data(grouped_data):

    output_data = pd.DataFrame()

    for group_number, group_df in grouped_data.groupby('PNum'):
        # Calculate employment lengths for each group
        employment_lengths = calculate_employment_length(group_df)

        # Filter the DataFrame for rows where Change_Unemployment_to_Employment == 1
        filtered_df = group_df[group_df['Change_Unemployment_to_Employment'] == 1].copy()

        # Assign the employment lengths to the new column
        filtered_df['Employment_Length'] = employment_lengths

        # Append the filtered DataFrame to the output DataFrame
        output_data = pd.concat([output_data, filtered_df])

    return output_data


    

def prepare_clean_data_to_calculate_employment_length(data):

    grouped_data = data.groupby('PNum').apply(lambda x: x.sort_values('Year')).reset_index(drop=True)

    grouped_data['Next_Year_Unemployment_Indicator'] = grouped_data.groupby('PNum')['Unemployment_Indicator'].shift(-1)
    grouped_data['Next_Year_Occupation_Category'] = grouped_data.groupby('PNum')['Occupation_Category'].shift(-1)

    conditions = [
    (grouped_data['Unemployment_Indicator'].isna()) | (grouped_data['Next_Year_Unemployment_Indicator'].isna()),
    (grouped_data['Unemployment_Indicator'] == 1) & (grouped_data['Next_Year_Unemployment_Indicator'] == 0)
]

    choices = [np.nan, 1]

    grouped_data["Change_Unemployment_to_Employment"] = np.select(conditions, choices, default=0)

    return grouped_data.reset_index(drop=True)


def calculate_employment_length(df):

    employment_lengths = []
    count = 0
    start_counting = False
    for _, row in df.iterrows():

        #I first initialize when there is a change from unemployment to employment
        if not start_counting and row['Change_Unemployment_to_Employment'] != 1:
            continue
        else:
            start_counting = True


        #Now I start counting all employment lengths
        if row['Change_Unemployment_to_Employment'] == 1:
            count = 0
        elif row['Unemployment_Indicator'] == 0:
            count += 1
            if row['Next_Year_Unemployment_Indicator'] == 1:
                employment_lengths.append(count)
                count = 0
        else:
            if count > 0:
                employment_lengths.append(count)
            count = 0

    #This is the safety conditions if the individual is still unemployed at the end of the data
    if count > 0:
        employment_lengths.append(np.NaN)

    return employment_lengths



def get_occupation_code_from_either_year(row):
    codes = [code for code in row if pd.notnull(code)]
    if len(set(codes)) > 1:
        return 'conflict'
    elif codes:
        return codes[0]
    else:
        return np.nan












def create_first_mentioned_occupation_column(data):
    """THis function takes all occupation columns and creates a new column with the first occupation mentioned - this can be in the 1970, 2000 or 2010 occupation code"""
    pass

def map_occupation_codes_to_common_mapping(occupation_column):
    """This function maps the occupation codes to our common mapping of occupation codes."""
    pass



