"""
Python module to push and pull data.
"""
import sys
sys.path.append("C:/Users/Administrator/Jupyter/Libraries")
from pathlib import Path
import pandas as pd
import conn
import dahelp
# ----------------------------------------------------

def pull_cms_master(case_where=None, charge_where=None):
    import re
    cms = conn.cms()

    sql_file = open(Path(__file__).parent.joinpath("SQL").joinpath('master_stanford.sql'), 'r')
    q = sql_file.read()
        
    felony_charge_def_files = ['@MURDER_CHARGE_CODES@',
                               '@AGGRAVATED_ASSAULT_CHARGE_CODES@',
                               '@ARMED_ROBBERY_CHARGE_CODES@',
                               '@RAPE_CHARGE_CODES@']
    felony_charge_codes = ''
    for f in felony_charge_def_files:
        felony_charge_codes = felony_charge_codes + open(Path(__file__).parent.joinpath("SQL").joinpath(f), 'r').read()   

    tags = re.findall(r'@.+@', q)
    for tag in tags:    
        if tag == '@FELONY_CHARGE_CODES@':
            rep_str = felony_charge_codes
        else:
            rep_str = open(Path(__file__).parent.joinpath("SQL").joinpath(tag), 'r').read()
        q = q.replace(tag, rep_str)
    
    if case_where:
        q = q.replace("1 = 1", case_where)
    
    if charge_where:
        q = q.replace("2 = 2", charge_where)

    df = pd.read_sql_query(q, cms)
    
    df = clean_datecols(df)
    
    return df

def clean_date(df):
    for col in df.columns:
        if 'date' in col:
            df[col] = pd.to_datetime(df[col])
        if 'day' in col:
            df[col] = pd.to_datetime(df[col])
    return df


def clean_colnames(df):
    from janitor import clean_names
    try:
        df = df.drop('', axis=1)
    except:
        pass
    return df.clean_names(remove_special=True)


def combine_queries(df1, df2, left, right=False):

    if right:
        return pd.merge(df1, df2, how="left", left_on=left, right_on=right) 

    else:
        return pd.merge(df1, df2, how="left", on=left)


def download_gdrive_file(file_id, new_file_name):
    import io
    from googleapiclient.http import MediaIoBaseDownload
    drive = conn.drive()
    
    request = drive.files().get_media(fileId=file_id)
    file = io.BytesIO()
    downloader = MediaIoBaseDownload(file, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    Path(new_file_name).write_bytes(file.getvalue())
    
def clean_datecols(df):
    date_cols = df.columns[df.columns.str.contains('date') | df.columns.str.contains('dob')]
    for col in date_cols:
        try:
            df[col] = df[col].replace('', pd.NaT)
            df[col] = pd.to_datetime(df[col])
        except:
            print(f'Datetime conversion failed for column {col}')
            continue
    return df