"""Function(s) for cleaning the data set(s)."""

import pandas as pd


def clean_data(data):
    """Clean data set.

    Args:
        data (pandas.DataFrame): The raw data downloaded 

    Returns:
        pandas.DataFrame: The cleaned data set.
        columns:
            ID: the id of the observation
            PNum: the number of the person 
            Sex: sex of person
            Birth_Year (int)
            Age (int)
            Education_Years (int)
            Real_Earnings (int)
            Real_Earnings_With_Partner (int)
            Employment_Status_First
            Employment_Status_Multi
            Occupation_First_Mention 
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

    #Occupation

    clean_data['Occupation_First_Mention_1970'] = data['OCC1970C']
    clean_data['Occupation_First_Mention_2000'] = data['OCC2000C1M']
    clean_data['Occupation_Second_Mention_2000'] = data['OCC2000C2M']
    clean_data['Occupation_Third_Mention_2000'] = data['OCC2000C3M']
    clean_data['Occupation_Fourth_Mention_2000'] = data['OCC2000C4M']
    clean_data['Occupation_First_Mention_2010'] = data['OCC2010C1M']
    clean_data['Occupation_Second_Mention_2010'] = data['OCC2010C2M']
    clean_data['Occupation_Third_Mention_2010'] = data['OCC2010C3M']
    clean_data['Occupation_Fourth_Mention_2010'] = data['OCC2010C4M']

    return clean_data


def clean_real_earnings_column(column):
    """This function takes in the real earnings column from the raw PSID data and cleans it."""

    return column.replace('Zero dollars', 0).astype('float')

