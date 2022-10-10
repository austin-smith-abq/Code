"""
Python module to help accelerate and homogenize 
data ingestion, formatting, and pushing tasks for the
2nd Judicial District Attorney's Office. 
If you have ideas for making work easier, contribute and document below!
"""
import pandas as pd
from pathlib import Path
import geo
import dataio
import conn
import notifications
import pdm
from dotenv import dotenv_values
#----------------------------------------------------

def config():
    return dotenv_values(Path(__file__).parent.joinpath("variables.env"))
    
def move_column(df, col_name, position = 0):
    df = df.copy()
    column_to_move = df.pop(col_name)
    df.insert(position, col_name, column_to_move)
    return df

def add_nibrs(df, nibrs = pd.DataFrame()):
    if nibrs.empty:
        nibrs = dataio.pull_nibrs()
    
    df.charge_code = df.charge_code.fillna('').astype(str)
    nibrs.charge_code = nibrs.charge_code.fillna('').astype(str)
    df = pd.merge(df, nibrs, how="left", on='charge_code')
    return df

def format_date(df, subset = None, 
                date_filter = ['date', 'dob'], date_format = '%Y-%m-%d', 
                quiet = False):
    # useful if importing a sheet with get_all_records()
    df = df.copy()
    if subset is None:
        subset = df.columns

    if subset is None: subset = df.columns
    if isinstance(date_filter, str): date_filter = list(date_filter)
    
    # format dates as dates            
    for col in subset:
        if any(filt in col for filt in date_filter):
            if not quiet: print(f'converting to date: {col}')
            df[col] = df[col].astype('datetime64').dt.date

    return df

def format_bool(df, subset = None,
                bool_filter = ['flag'], 
                bool_dict = {'TRUE': True, 'FALSE': False, 'True': True, 'False': False}, 
                quiet = False):
    # useful if importing a sheet with get_all_records()
    df = df.copy()
    if subset is None: subset = df.columns
    if isinstance(bool_filter, str): bool_filter = bool_filter.split(',')
    
    # format booleans as booleans
    for col in subset:
        if any(filt in col for filt in bool_filter):
            if not quiet: print(f'converting to bool: {col}')
            df[col] = df[col].astype(str)
            df[col] = df[col].str.strip()
            df[col] = df[col].map(bool_dict)

    return df
    
def repair_case_num(case_num, case_num_type, extract = True, keep = 'first'):
    """Repairs and extracts District, Magistrate and DACase numbers from a string input
    
    Parameters
    ----------
    case_num       :  case number, or string containing case number
    case_num_type  :  one of 'da', 'metro', ('pdm', 'dis', 'mag')
    extract        :  flag to extract the case number from the string              [True]
    keep           :  indicator to extract 'first', 'last', or 'all' case numbers  ['first']
                      
    
    Returns
    ----------
    case_num       :  repaired and/or extracted case number in a str 
                      If keep == 'all', returns extracted case numbers as a list
    
    Usage    
    ----------
    # extract a repaired PDM number
        repair_case_num('Case# is D202LR202000080', 'pdm')
    # repair a column of a data frame
        df['DistDocket'].apply(lambda x: repair_case_num(x, 'district'))
    # return the string intact, with the case number repaired
        repair_case_num('Case# is D202LR202000080', 'pdm', extract = False)
    # return all Metro case numbers in a list
        repair_case_num('Related cases: T4FR202202459; T-4-FR-2019-004731', 'metro', keep = 'all')
    # return first metro case
        repair_case_num('T4FR202202459; T-4-FR-2019-004731', 'metro', keep = 'first')
    """
    
    import re    
    case_num = str(case_num)
    case_num_type = case_num_type.lower()
    case_num = case_num.strip().upper().replace('--', '-')    

    if case_num_type[0:3] in ['pdm', 'dis', 'mag']:
        pattern = 'D-?202-?(\w{2})-?(\d{4})-?0(\d{4})'
        case_num = re.sub(pattern, r'D-202-\1-\2-0\3', case_num)                
    elif case_num_type == 'metro':        
        pattern = 'T-?4-?(\w{2})-?(\d{4})-?0?(\d{5})'
        case_num = re.sub(pattern,  r'T-4-\1-\2-0\3', case_num)                   
    elif case_num_type == 'da':
        pattern = '(\d{4})-?(\d{5})-?(\d{1})(\w{0,3})'
        case_num = re.sub(pattern, r'\1-\2-\3\4', case_num)         
    if extract:
        case_num_list = re.findall(pattern.replace('(','').replace(')',''), case_num)
        if keep   == 'first': 
            if case_num_list:
                return case_num_list[0]
            else:
                return ''
        elif keep == 'last':
            if case_num_list:
                return case_num_list[0]
            else:
                return ''
        elif keep == 'all'   : return case_num_list    
    return case_num

# def extract_case_num(case_num, case_num_type):
#     """Extracts PDM, District, Magristrate, Metro or DA case number from an input (such as a dataframe column).
#     Case Number Type arguments available are: 'pdm', dis', 'mag', metro', and 'da'.
#     This function assumes that repair_case_num has already been run on the input.
#     NOTE!! Deprecated: use repair_case_num(... extract = True)
#     """
    
#     print('Deprecated: use repair_case_num(... extract = True)')
    
#     import re
#     #case_num = str(case_num).strip().upper()    

#     if case_num_type[0:3] in ['pdm', 'dis', 'mag']:
      
#         case_num = re.search(r'D-202-(\w{2})-(\d{4})-(\d{5})', case_num)        

#     elif case_num_type == 'metro':        

#         case_num = re.search(r'T-4-(\w{2})-(\d{4})-(\d{6})', case_num)
        
#     elif case_num_type == 'da':

#         case_num = re.search(r'(\d{4})-(\d{5})-(\d{1})(\w{0,2})', case_num)      
        
#     if case_num:
#         return case_num.group()


def cms_query_main(cms, match_sql = None):
    # cms_main.sql
    sql_file = open(Path(__file__).parent.joinpath("includes").joinpath('cms_core.sql'), 'r')
    q = sql_file.read()
    if match_sql:
        q = q.replace('WHERE 1=1', match_sql)
    df = pd.read_sql_query(q, cms)
    return df

def cms_query(cms, match_on = None, match_to = None, match_sql = None,
                only_adult = False, only_felony = False, all_time = False,                
                by_charge = False, by_alias = False, by_address = False 
             ):
    """
    Returns a dataframe of cases from a SQL query of CMS. 
    The base SQL query is found in ./includes/cms_cases.sql
    
    Parameters
    ----------
    cms       :  cms client, returned by conn_cms()
    
    # Filtering Method 1
    match_on  : CMS column on which to match e.g., 'CMSDACase', 'DistDocket', 'MagDocket', 'CaseClass.ClassName'
    match_to  : dataframe series or list of instances to match to
    
    # Filtering Method 2
    match_sql : sql WHERE string to perform the matching. 
                If match_sql is specified, match_on and match_to are ignored.
    
    # Filtering Flags
    only_adult  : Flag to return all or only adult cases                    [False]
    only_felony : Flag to return all or only felony cases                   [False]
    all_time    : Flag to return all or only cases opened after 2015-01-01  [False]

    # Level of Output Flags
    by_charge   : Flag to return all charges, rather than top charge only   [False]
    by_alias    : Flag to return all alias, rather than primary only        [False]
    by_address  : Flag to return all def, addresses rather than pimary only [False]
    
    Returns
    ----------
    df  :  dataframe with results 
    
    Usage    
    ----------
    # return all cases in CMS since 2015-01-01 (one row per case)
        cms_query(cms)
    # return all cases matching provided Metro case numbers (one row per case)
        cms_query(cms, match_on = 'MagDocket', match_to = df.metro_case)          
    # return all **charges** for this defendant (one row per charge, from any cases)
        cms_query(cms, match_on = 'Defendant', match_to ='8DCD99F7-0581-42EB-99AE-784868CD8430', by_charge=True) 
    # return all charges for cases matching the provided DA Case numbers
        cms_query(cms, match_on = 'CMSDACase', match_to = df.da_num, by_charge = True) 
    # return all charges and aliases matching the provided DA Case numbers 
        cms_query(cms, match_on = 'CMSDACase', match_to = df.da_num, by_alias = True)
    # return all cases matching the provided DA Case numbers, with no time constraint
        cms_query(cms, match_on = 'CMSDACase', match_to = df.da_num, all_time = True)
    """
    import re
    sql_file = open(Path(__file__).parent.joinpath("includes").joinpath('cms_cases.sql'), 'r')
    q = sql_file.read()
    
    # Filter on Matching
    if match_on and any(match_to):         
        if type(match_to) is pd.Series:
            match_to = "', '".join(match_to.astype(str))
        elif isinstance(match_to, list):
            match_to = "', '".join(match_to)
            
        if match_on == 'DistDocket':
            # last dash is missing in CMS
            match_to = re.sub(r'D-202-(\w{2})-(\d{4})-(\d{5})', r'D-202-\1-\2\3', match_to)
        str_with_match = f"WHERE {match_on} in ('{match_to}')"        
        q = q.replace('WHERE 1=1', str_with_match)
    elif match_sql:
        q = q.replace('WHERE 1=1', match_sql)

    # Additional Filtering
    if only_adult:  
        append_sql = open(Path(__file__).parent.joinpath("includes").joinpath('cms_only_adult.sql'), 'r')
        q = q + append_sql.read()                    
    if only_felony:  
        append_sql = open(Path(__file__).parent.joinpath("includes").joinpath('cms_only_felony.sql'), 'r')
        q = q + append_sql.read()                    
    if all_time:    q = q.replace("AND OpenDate >= '2015-01-01'", '--')
    if by_charge:   q = q.replace('AND Charges.[Primary] = 1', '--')
    if by_alias:    q = q.replace('AND DefendantAlias.[Primary] = 1', '--')
    # if by_address:  q = q.replace('AND DefendantAddress.AddressSeq = 1', '--')    
    if by_address:  q = q.replace('(DefendantAddress.AddressSeq IS NULL OR DefendantAddress.AddressSeq = 1)', '--')    
          
    df = pd.read_sql_query(q, cms)
    # Should we clean the columns before we return them?
    # repair case names, strip, upper
    return df

def tag_cases(cms, df, query_list):
    """Tags df **cases** with additional information extracted from CMS.
    
    Parameters
    ----------
    cms      : cms client, returned by conn_cms()
    df       : dataframe, with columns on which to match queries
    query_list : list of strings indicating queries to run
    
    Query                  Matches on         Columns Returned
    ----------------------------------------------------------    
    'case_disposition'   [on CMSDACase]  ->   'Case_Disposition' 
    
    'case_level_flags'   [on CMSDACase]  ->   'Case_Flag_Murder',
                                              'Case_Flag_Aggravated_Assault', 
                                              'Case_Flag_Armed_Robbery',
                                              'Case_Flag_Rape',
                                              'Case_Flag_Violent',
                                              'Case_Flag_Difficult_Victim',
                                              'Case_Flag_Property',
                                              'Case_Flag_Drug',
                                              'Case_Flag_DWI',
                                              'Case_Flag_Other'
                                                
    'nibrs'              [on Description] ->  'NIBRS_CaseClass', 
                                              'NIBRS_Offense_Type', 
                                              'UCR_Part_I', 
                                              'UCR_Part_II', 
                                              'NIBRS_Group_A', 
                                              'NIBRS_Group_B'
    Returns
    ----------
    df  :  dataframe with additional columns 
    
    Usage    
    ----------
    df = cms_tag_df(cms, df, query_list = ['case_disposition', 'nibrs'] # runs these two queries
    """
    
    if isinstance(query_list, str): 
        query_list = query_list.split(',')
        
    for query_type in query_list:
        print(f'Tagging df with {query_type}')
        if query_type == 'nibrs':        
            on_col = 'Description'           
            tag_df = pd.read_csv(Path(__file__).parent.joinpath("includes").joinpath('nibrs.csv'))            
        # elif query_type == 'case_felony': 
        #     on_col = 'CMSDACase'
        #     tag_df = cms_query(cms, match_on = on_col, match_to = df[on_col], only_felony = True, by_charge=True)            
        #     tag_df.drop_duplicates('CMSDACase')
        #     tag_df['Case_Flag_Felony'] = True
        #     tag_df = tag_df[['CMSDACase', 'Case_Flag_Felony']]
        else:
            on_col = 'CrimeCase'        
            sql_file = open(Path(__file__).parent.joinpath("includes").joinpath('cms_' + query_type + '.sql'), 'r')
            q_original = sql_file.read()
            # batch things up
            max_rows = 10000
            list_df = [df[i:i+max_rows] for i in range(0,len(df),max_rows)]
            list_tag_df = []
            for df_part in list_df:
                print(f'Batch {len(df_part)}')
                q = q_original            
                match_to = "', '".join(df_part[on_col].astype(str))
                #str_with_match = f"WHERE {on_col} in ('{match_to}')"        
                str_with_match = f"WHERE CrimeCase.CrimeCase in ('{match_to}')"        
                q = q.replace('WHERE 1=1', str_with_match)                    
                list_tag_df.append(pd.read_sql_query(q, cms))
            tag_df = pd.concat(list_tag_df)
            
            # should we run format_bool on these to turn them into proper booleans?
        if on_col in df:
            tag_df = tag_df.loc[:, ~tag_df.columns.str.contains('^Unnamed')]
            df = pd.merge(df, tag_df, how="left", on = on_col)
            # replace NaN with False for Flag columns
            # new_cols = list(tag_df.drop(columns = 'CMSDACase').columns)
            # for flag_col in [col for col in new_cols if "Flag" in col]:
            #     df[flag_col] = df[flag_col].fillna(False)  
            #     df[flag_col] = df[flag_col].map({'True':True,'False':False})              
            
        else:
            print(f'Could not tag df with {query_type} because column {on_col} was not present')
    # fill nan with False?
    # Clean up the columns and column name?
    # all_cases_df["Description"] = all_cases_df["Description"].str.replace(',','-')
    # all_cases_df["ChargeMethod"] = all_cases_df["ChargeMethod"].str.replace(',','-')
    # all_cases_df = all_cases_df.drop_duplicates()
    # all_cases_df = all_cases_df.drop('CASECLASS', 1)
    # all_cases_df = all_cases_df.loc[:,~all_cases_df.columns.duplicated()]    
    return df

# def pull_charge_table():
#     # where does the original charttable come from?  Can we pull it straight from CMS?
#     charge_table_df = pd.read_csv(Path(__file__).parent.joinpath("includes").joinpath('chargetable.csv'))
#     charge_table_df = charge_table_df[['Chg Code', 'F M', 'Degree']].copy()
#     charge_table_df = charge_table_df.rename(columns={'Chg Code': 'ChargeCode'})
#     charge_table_df.to_csv(Path(__file__).parent.joinpath("includes").joinpath('charge_table.csv'))

    
def df_to_json(df):
    """Returns a dataframe as json (uses a dict rather than json itself for readability)."""
    return df.to_json(orient='records')

def count_attorneys(csvfile):
    import dataio
    e = pd.read_csv(csvfile)
    e = e.dropna(subset = 'Position')
    e = e[~e.Name.str.contains('VACANT')]
    e['attorney_value'] = 0.0
    e.loc[e.Position.str.contains("Attorney") == True, "attorney_value"]              = 1.0
    e.loc[(e.Position == "Chief Deputy District Attorney") == True, "attorney_value"] = 0.5
    e.loc[(e.Position == "District Attorney") == True, "attorney_value"]              = 0.0
    e = dataio.clean_colnames(e)
    e = dataio.clean_datecols(e)
    return e

def simplify_case_class(df):
    import numpy as np
    df['case_class'] = df.cms_case_class
    df['case_class'] = np.where(df.cms_case_class.str.startswith('Domestic Violence'), 
                                'Domestic Violence', df.case_class)
    df['case_class'] = np.where(df.cms_case_class.str.startswith('Sex'), 'Sexual Assault', df.case_class)
    df['case_class'] = np.where(df.cms_case_class.str.startswith('Driving While Intoxicated'), 'DWI', df.case_class)
    other_classes = ['Drug Prescription Cases', 
                     'Public Corruption Cases', 
                     'Dept. of Game and Fish',
                     'Truancy',
                     'Traffic Citations',
                     'Misdemeanor', 
                     'Non-Violent Felony']                                                         
    df['case_class'] = np.where(df.cms_case_class.isin(other_classes), 'Other', df.case_class)
    df['case_class'] = df.case_class.str.replace(' Cases', '')
    
    df.charge_description = df.charge_description.fillna('')
    # for non-violent felony, fix a few things
    df['case_class'] = np.where((df.cms_case_class == 'Non-Violent Felony') &
                                (df.charge_description.str.contains('FELON')) &
                                 df.charge_description.str.contains('FIREARM'),
                                'Felon in Possession',
                                df.case_class)
    df['case_class'] = np.where((df.cms_case_class == 'Non-Violent Felony') &
                                (df.charge_description.str.contains('TRAFFICKING')), 
                                'Drug Trafficking',
                                df.case_class)
    df['case_class'] = np.where((df.cms_case_class == 'Non-Violent Felony') &
                                (df.charge_description.str.contains('POSSESSION')) & 
                                    (
                                    (df.charge_description.str.contains('CONTROLLED SUBSTANCE')) |
                                    (df.charge_description.str.contains('DRUG')) |
                                    (df.charge_description.str.contains('MARIJUANA')) &
                                    ~(df.charge_description.str.contains('PARAPHERNALIA'))
                                    ), 
                                'Drug Possession',
                                df.case_class)
    df['case_class'] = np.where((df.cms_case_class == 'Non-Violent Felony') &
                                (
                                    (df.charge_description.str.contains('ASSAULT')) |
                                    (df.charge_description.str.contains('BATTERY'))
                                ) &
                               ~(df.charge_description.str.contains('PEACE OFFICER')), 
                                'Crimes Against Persons',
                                df.case_class)
    df['case_class'] = np.where((df.cms_case_class == 'Non-Violent Felony') &
                                (df.charge_description.str.contains('PEACE OFFICER')), 
                            'Peace Officer Crimes',
                            df.case_class)
    df['case_class'] = np.where((df.cms_case_class == 'Non-Violent Felony') &
                                (df.charge_description.str.contains('REGISTRATION OF SEX OFFENDERS')), 
                            'Sex Offender Registration',
                            df.case_class)
            
    
    return df


def display_output(field, value):
    from IPython.display import HTML, display
    
    return display(HTML(
            f"<h4><span style='color:{colors(2)[0]}'>{field}:</span> <span style='color:{colors(0)[0]}'>{value}</span></h4>"
            ))

def colors(idx = []):
    da_colors = ['#000175', '#cf000f', '#007def', '#ffcb00']
    
    if idx:
        if type(idx) == int:
            idx = [idx]
        return [da_colors[i] for i in idx]
    else:
        return da_colors

