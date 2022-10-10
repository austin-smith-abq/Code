"""
Python module to push and pull data.
"""
from pathlib import Path
import pandas as pd
import conn
import dahelp
# ----------------------------------------------------

def pull_nmdx(table, info = False,
                  sql = None, where_sql = None, select_sql = None
             ):   
    """
    Returns a df from a SQL query of Odyssey dataXchange
    
    Parameters
    ----------
    table :  one of 'hearing', 'mdc', warrant', 'inmate', 'disposition', 'release', 'sentence', 'protection'
    info  :  flag to return the column names and descriptions for the table
    select_sql :  sql language for selecting columns
    where_sql  :  sql langauge for filtering rows
    sql   :  name of sql query file in ./includes
    limit :  max number of rows to return
    
    Returns
    ----------
    df  :  dataframe with results 
    
    Usage    
    ----------
    # Show what's in the hearing table:
        pull_nmdx('hearing', info = True)    
    
    # Select and filter data according to pre-existing query 'odyssey_calendar.sql':
        pull_nmdx('hearing', sql = 'calendar') 
    
    # Pull from hearing table, filtering on crt_court:
        pull_nmdx('release', 
                      where_sql = "crt_court='Second Judicial District Bernalillo County'")
    # Pull from hearing table, and just select some columns:
        pull_nmdx('release', 
                      where_sql  = "crt_court='Second Judicial District Bernalillo County'", 
                      select_sql = "crt_casetype, crt_court")
    """
    sc = conn.nmdx()
        
    import re
    
    # dictionary mapping table to table id    
    table_id = {'hearing'     : 'aws9-xwqm',
                'mdc'         : 'sm7s-eqqr',
                'warrant'     : 'k9iw-sv5b',
                'inmate'      : 'kk7s-kxuh',
                'alias'       : 'xkgk-es8k',
                'disposition' : '67aq-nuwb',
                'release'     : 'ybxv-h8dx',
                'sentence'    : 'nbc8-ah4q',
                'transport'   : 'anv4-uuzw',
                'protection'  : 'arjs-vngg'}
    metadata = sc.get_metadata(table_id[table])
    cols = [x['name'] for x in metadata['columns']]
    desc = [x['description'] if 'description' in x.keys() else '' for x in metadata['columns'] ]
    df_info = pd.DataFrame(list(zip(cols, desc)), columns = ['Column', 'Description'])

    # just provide information about the table to the user
    if info == True:
        return df_info
    
    if sql:
        sql_file = open(Path(__file__).parent.joinpath("includes").joinpath('odyssey_' + sql + '.sql'), 'r')
        q = sql_file.read()
        q = re.sub('SELECT ', '', q, flags=re.IGNORECASE)        
        q = re.split('WHERE ', q, flags=re.IGNORECASE)        
        select_sql = q[0]
        if len(q) > 1:
            where_sql = q[1]
            
    data = sc.get_all(table_id[table], where = where_sql, 
                  select = select_sql)   
    
    df = pd.DataFrame(data)
    
    return df

def push_to_sheet(key, sheetname, df, mode='new'):
    """    
    Writes a dataframe to a google sheet

    Parameters
    ----------
    key       :  sheet key
    sheetname :  name of worksheet
    df        :  dataframe
    mode      :  one of 'new', 'overwrite', 'append', 'append_unique'

    Usage    
    ----------
    # Write df to a new sheet
        my_key = '1JyNDiDD7Z6EPyIQGreMuBfs9E3s50WAs8hcZQzyB_AQ'
        push_to_sheet( my_key, 'mysheet', df, mode = 'new')   

    # Write df to a sheet and overwrite all existing data
        push_to_sheet(my_key, 'mysheet', df, mode = 'overwrite')   

    # Append df to a sheet 
        push_to_sheet(my_key, 'mysheet', df, mode = 'append')   

    # Append df to a sheet, keeping only non-duplicate rows
        push_to_sheet(my_key, 'mysheet', df, mode = 'append_unique')        
   """

    import gspread_dataframe as gd
    import gspread_formatting as gf
    gc = conn.gdrive()
    sh = gc.open_by_key(key)
    worksheet_names = []
    worksheets = []

    # get existing worksheets
    for ws in sh.worksheets():
        worksheet_names.append(ws.title)

    if (mode == 'new') & (sheetname in worksheet_names):
        sheetname = sheetname + '_new'

    if sheetname not in worksheet_names:
        # create a new worksheet
        worksheet = sh.add_worksheet(
            title=sheetname, rows=len(df)+1, cols=len(df.columns))

    worksheet = sh.worksheet(sheetname)
    worksheets.append(worksheet)

    # Formats header
    fmt = gf.cellFormat(
        backgroundColor=gf.color(0, 0.39, 45.88),
        textFormat=gf.textFormat(bold=True, foregroundColor=gf.color(1, 1, 1)),
        horizontalAlignment='LEFT'
    )

    gf.format_cell_range(worksheet, '1', fmt)

    # Sets header as frozen
    gf.set_frozen(worksheet, rows=1)

    if mode == 'new':
        gd.set_with_dataframe(worksheet, df)
    elif mode == 'overwrite':
        worksheet.clear()  # clear everything
        gd.set_with_dataframe(worksheet, df)
    elif mode == 'append':
        df_existing = pull_from_sheet(key, sheetname)
        df = pd.concat([df_existing, df])
        push_to_sheet(key, sheetname, df, mode='overwrite')
    elif mode == 'append_unique':
        print(len(df))
        # append first, since the process of writing/reading can change formatting
        push_to_sheet(key, sheetname, df, mode='append')
        df = pull_from_sheet(key, sheetname)
        df = df.drop_duplicates()
        push_to_sheet(key, sheetname, df, mode='overwrite')
    
    sheetId = worksheet._properties['sheetId']
    body = {
        "requests": [
            {
                "autoResizeDimensions": {
                    "dimensions": {
                        "sheetId": sheetId,
                        "dimension": "COLUMNS",
                        "startIndex": 0,  # Please set the column index.
                        "endIndex": len(df.columns)  # Please set the column index.
                    }
                }
            }
        ]
    }

    res = sh.batch_update(body)

    return worksheet


def pull_from_sheet(key, sheetname, head = 1):
    """    
    Reads a dataframe from a google sheet

    Parameters
    ----------
    key       :  sheet key
    sheetname :  name of worksheet
    head      :  row to use as column headers

    Returns
    ----------
    df        :  dataframe

    Usage    
    ----------
    # Read df from a sheet
        my_key = '1JyNDiDD7Z6EPyIQGreMuBfs9E3s50WAs8hcZQzyB_AQ'
        df = pull_from_sheet(my_key, 'mysheet', head = 2)           
   """

    gc = conn.gdrive()
    worksheet = gc.open_by_key(key).worksheet(sheetname)
    df = pd.DataFrame(worksheet.get_all_records(numericise_ignore=['all'], head = head))
    return df


def ingest_elastic(df, index_name, pipeline_name):

    from elasticsearch import helpers

    es = conn.elastic()

    es.indices.delete(index=index_name, ignore=[400, 404])

    def doc_generator(df, index_name, pipeline_name):

        df_iter = df.iterrows()
        for index, document in df_iter:
            yield {
                "_index": index_name,
                "_source": document.to_json(default_handler=str),
                "pipeline": pipeline_name,
            }

    helpers.bulk(es, doc_generator(df, index_name, pipeline_name))


def pull_nibrs():
    # pull from a google sheet, in progress...working on NIBRS definitions
    nibrs = pull_from_sheet('1QQFZ5DLI6874kuj28ivvCQxzMG6wEeiuNBOmnqX2RwA', 'MergeChargeCode')

    nibrs = nibrs[[
            "Charge_Code",
            "Offense_Type",
            "UCR_Part_I",
            "UCR_Part_II",
            "NIBRS_Group_A",
            "NIBRS_Group_B",
        ]]
    nibrs = nibrs.drop_duplicates()

    nibrs = clean_colnames(nibrs)
    
    nibrs.charge_code = nibrs.charge_code.astype(str)
    
    #nibrs.charge_code = nibrs.charge_code.fillna('').astype(int).astype(str)

    #nibrs.to_csv(Path(__file__).parent.joinpath("includes").joinpath('nibrs.csv'))

    return nibrs

def pull_cms_master(case_where=None, charge_where=None):
    import re
    cms = conn.cms()

    sql_file = open(Path(__file__).parent.joinpath("SQL").joinpath('master.sql'), 'r')
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

def pull_cms_defendant_guids(where=None):

    cms = conn.cms()

    sql_file = open(Path(__file__).parent.joinpath(
        "SQL").joinpath('def_guid.sql'), 'r')
    q = sql_file.read()

    if where:
        q = q.replace("1 = 1", where)

    df = pd.read_sql_query(q, cms)

    df = clean_datecols(df)
    
    return df

def pull_cms_custom(table, select=False, where=False, query_col_name=False, query_col=False):

    cms = conn.cms()

    sql_file = open(Path(__file__).parent.joinpath(
        "SQL").joinpath('custom_query.sql'), 'r')
    q = sql_file.read()
    
    q = q.replace("TABLE", table)

    if select:
        q = q.replace("*", f"DISTINCT {select}")
        
    if query_col_name:
        query_list = "', '".join(query_col.str.strip().astype(str))
        q = q.replace("1 = 1", f"{query_col_name} in ('{query_list}')")
    
    else:
        if where:
            q = q.replace("1 = 1", where)

    df = pd.read_sql_query(q, cms)

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