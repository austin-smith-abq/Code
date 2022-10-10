"""
Python module for preventative detention motions.
"""
import pandas as pd
import numpy as np
import re
import dataio


def pull():

    sheet_id = '1IZ0CALnhBa1ATuOst1oTnkO5VVD7z-R1vshvw0mDodQ'

    current_df  = dataio.pull_from_sheet(sheet_id, "PDM Tracking")
    backfill_df = dataio.pull_from_sheet(sheet_id, "Backfill PDM Tracking")

    # concatenate
    df = pd.concat([backfill_df, current_df], ignore_index=True)

    # drop an extra header row
    df = df[(df.da_num != "") & (df.da_num != "DA Number (20YY-#####-#)")]

    # remove extra white spaces
    for col in df.columns:
        try:
            df[col] = df[col].str.strip()
        except:
            continue

    # clean the column names
    df = dataio.clean_colnames(df)

    # remove rows where it is not a pdm
    df = df[df.notpdm != 'TRUE']

    # Fills blank firearm accounts with false
    df.firearm = df.firearm.replace('', 'FALSE')

    # just keep the desired columns
    keep_cols = ['da_num', 'pdm_number', 'def_last', 'def_first', 'def_dob', 'pdm_filedate',
                 'pdm_heardate', 'pdm_ada', 'pdm_judge', 'pdm_outcome', 'metro_num',
                 'psa_flag', 'psa_nca', 'psa_fta', 'psa_na', 'firearm', 'fed_ref']
    df = df[keep_cols]

    # for consistency
    df = df.rename(columns={'da_num': 'cms_case_num'})
    
    # prefix everything with a pdm
    df.columns = 'pdm_' + df.columns.str.replace('pdm_', '')
    
    df.pdm_psa_fta = df.pdm_psa_fta.replace('', np.nan)
    df.pdm_psa_nca = df.pdm_psa_nca.replace('', np.nan)

    df['pdm_psa_recommendation'] = 'Relase'
    df['pdm_psa_recommendation'] =  np.where((df.pdm_psa_fta == '6') | 
                                         (df.pdm_psa_nca == '6') |
                                         (df.pdm_psa_nca == '5') & (df.pdm_psa_fta == '5'),
                                          'Detain', 'Release')
    
    return df.reset_index(drop=True)

def pull_pdm_charges(df):
    pdm_case_list = "', '".join(df.pdm_cms_case_num.str.strip().astype(str).unique())
    df_charges = dataio.pull_cms_master(case_where=f"CrimeCase.CMSDACase in ('{pdm_case_list}')" )

    # merge left on the pdm df
    df = pd.merge(df, df_charges, how="left", left_on='pdm_cms_case_num', right_on='cms_case_num')
    
    # print out cases where no charges were found
    n_missing = pd.isnull(df.cms_case_num).sum()
    if n_missing:
        print(f'No CMS charges found for {n_missing} PDM Hearings:')
        print(df[pd.isnull(df.cms_case_num)][['pdm_cms_case_num','pdm_number','pdm_metro_num','cms_case_num']])
    return df

def pull_guid(df):    
    # pull cms defendant GUID
    da_num_list = "', '".join(df.pdm_cms_case_num.str.strip().astype(str).unique())    
    def_guid = dataio.pull_cms_defendant_guids(where=f"CrimeCase.CMSDACase in ('{da_num_list}')")
    
    # drop duplicated charges with different close dates; just want 1 row per guid/case
    def_guid = def_guid.drop_duplicates(subset = ['def_cms_case_num', 'def_defendant_guid'])

    # rename the column to follow conventions
    def_guid = def_guid.rename(columns={'def_defendant_guid':'cms_defendant_guid'})
    
    # merge left on the pdm df
    df = pd.merge(df, def_guid, how="left", left_on='pdm_cms_case_num', right_on='def_cms_case_num')
    
    # drop unecessary columns
    df.drop(columns = ['def_cms_case_num', 'def_closed_date'])
    
    # print out cases where no GUID was found
    n_missing = pd.isnull(df.cms_defendant_guid).sum()
    if n_missing:
        print(f'No GUID found for {n_missing} PDM Defendants:')
        print(df[pd.isnull(df.cms_defendant_guid)][['pdm_cms_case_num','pdm_number','pdm_def_last','cms_defendant_guid']])
    return df

def pull_def_charges(df):
    
    if not('cms_defendant_guid' in df.columns):
            df = pull_guid(df)
    
    # pull all charges for these guids
    guid_list = "','".join(df[~pd.isnull(df.cms_defendant_guid)].cms_defendant_guid.unique().astype(str))
    df_charges = dataio.pull_cms_master(case_where=f"CrimeCase.Defendant in ('{guid_list}')") 
    
    # merge left on the pdm df
    df = pd.merge(df, df_charges, how="left", on='cms_defendant_guid')
    
    # print out cases where no charges were found
    n_missing = pd.isnull(df.cms_case_num).sum()
    if n_missing:
        print(f'No CMS charges found for {n_missing} PDM Hearings:')
        print(df[pd.isnull(df.cms_case_num)][['pdm_cms_case_num','pdm_number','pdm_metro_num','cms_case_num']])
    return df

def categorize_charges(df):
    date_cols = df.columns[df.columns.str.contains('date')]
    for col in date_cols:
        try:
            df[col] = df[col].replace('', pd.NaT)
            df[col] = pd.to_datetime(df[col])
        except:
            print(f'Datetime conversion failed for column {col}')
            continue
    
    #----------------------------------------------
    # Define the search window
    df['pdm_win_start_date'] = df.pdm_heardate
    df['pdm_win_end_date']   = df.def_closed_date.fillna(pd.to_datetime('today').strftime('%m/%d/%Y'))    
    
    #----------------------------------------------
    # Define the date of the incident 
    df['temp_charge_date']   = df.charge_start_date

    # If empty, fill with the date of the earliest charge in that case
    df['temp_charge_date'] = df['temp_charge_date'].fillna(df.groupby('pdm_cms_case_num')['temp_charge_date'].transform('min'))
    
    # If empty, try using the complaint date (may be close to the incident)
    df['temp_charge_date'] = np.where(pd.isnull(df.temp_charge_date), df.complaint_date, df.temp_charge_date)
    
    # If empty, try using the open date (should be the latest date)
    df['temp_charge_date'] = np.where(pd.isnull(df.temp_charge_date), df.open_date, df.temp_charge_date)
   
    #----------------------------------------------
    # Categorize based on the temp_charge_date and window dates
    df['pdm_case_type'] = 'Uncategorized'
    
    df['pdm_case_type'] = np.where((df.pdm_cms_case_num == df.cms_case_num), 'PDM', df.pdm_case_type)
    
    df['pdm_case_type'] = np.where((df.temp_charge_date < df.pdm_win_start_date) &
                                   (df.pdm_cms_case_num != df.cms_case_num), 'Historical', df.pdm_case_type)
    
    df['pdm_case_type'] = np.where((df.temp_charge_date >= df.pdm_win_start_date) &
                                   (df.temp_charge_date <= df.pdm_win_end_date) &
                                   (df.pdm_cms_case_num != df.cms_case_num),'In Window', df.pdm_case_type)
    
    df['pdm_case_type'] = np.where((df.temp_charge_date > df.pdm_win_end_date) &
                                   (df.pdm_cms_case_num != df.cms_case_num), 'Subsequent', df.pdm_case_type)
            
    return df



def sanitize(df):
    for col in df.columns:
        if "guid" in col:
            continue
        elif "pdm_case_type" in col:
            continue
        elif "date" in col or "dob" in col:
            try:
                df[col] = pd.to_datetime(df[col])
            except:
                continue
        try:
            df[col] = df[col].str.strip()
        except:
            continue
        if "num" in col:
            try:
                df[col] = df[col].str.upper()
            except:
                continue
        else:
            try:
                df[col] = df[col].str.title()
            except:
                continue

    return df