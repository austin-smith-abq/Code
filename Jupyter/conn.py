"""
Python module to connect to various endpoints.
"""
from pathlib import Path

import pandas as pd

# ----------------------------------------------------


def gdrive():
    # establish connection with google drive with gspread
    import gspread
    import json
    p = Path(__file__).parent.joinpath("includes").joinpath("credentials.json")
    with p.open("r") as f:
        g_dict = json.load(f)

    gc = gspread.service_account_from_dict(g_dict)
    return gc

def pydrive():
    # establish connection with google drive with pydrive
    from pydrive.auth import GoogleAuth
    from pydrive.drive import GoogleDrive
    from oauth2client.service_account import ServiceAccountCredentials
    
    scope = ["https://www.googleapis.com/auth/drive"]

    p = Path(__file__).parent.joinpath("includes").joinpath("credentials.json")

    gauth = GoogleAuth()
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(p, scope)
    drive = GoogleDrive(gauth)
    return drive

def gcalendar():
    
    from googleapiclient.discovery import build
    from google.oauth2 import service_account
    scope = ['https://www.googleapis.com/auth/calendar']
    p = Path(__file__).parent.joinpath("includes").joinpath("credentials.json")
    creds = service_account.Credentials.from_service_account_file(
        p, 
        scopes=scope,
        subject='accounts@da2nd.state.nm.us'
    )
    service = build('calendar', 'v3', credentials=creds, cache_discovery=False)


    return service

def drive():
    
    from googleapiclient.discovery import build
    from google.oauth2 import service_account
    scope = ['https://www.googleapis.com/auth/drive']
    p = Path(__file__).parent.joinpath("includes").joinpath("credentials.json")
    creds = service_account.Credentials.from_service_account_file(
        p, 
        scopes=scope,
    )
    service = build('drive', 'v3', credentials=creds, cache_discovery=False)


    return service


def gchat():
    from httplib2 import Http
    from googleapiclient.discovery import build
    from oauth2client.service_account import ServiceAccountCredentials

    scope = ['https://www.googleapis.com/auth/chat.bot']
    p = Path(__file__).parent.joinpath("includes").joinpath("credentials.json")
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        p, 
        scopes=scope,
    )
    service = build('chat', 'v1', http=credentials.authorize(Http()), cache_discovery=False)
    
    return service

def elastic():
    from elasticsearch import Elasticsearch

    es = Elasticsearch(
        [
            "http://user:Analytics5601@172.30.143.211:9200",
            "http://user:Analytics5601@172.30.143.214:9200",
            "http://user:Analytics5601@172.30.143.80:9200",
        ]
    )
    return es


def nmdx():
    """
    Connect to NMdataXchange with Socrata API
    """
    from sodapy import Socrata

    sc = Socrata(
        "www.nmdataxchange.gov",
        None,
        username="austin.smith@da2nd.state.nm.us",
        password="520Lom@$",
    )
    return sc

def raw_sql(db='raw_data'): 
    from sqlalchemy import create_engine
    engine = create_engine(f"postgresql://admin:Catalina4801@172.30.141.21:5400/{db}")
    con = engine.connect()
    return con

def hippo_sql(): 
    from sqlalchemy import create_engine
    engine = create_engine(f"postgresql://admin:Catalina4801@172.30.141.21:5401/hippo")
    con = engine.connect()
    return con


def cms():
    import pymssql

    cms = pymssql.connect(
        server="192.168.150.31",
        user="rtsqluser",
        password="7rK&Rk1ezV^sQ$za4MTo#iWE",
        database="2da_cms",
        port="1433",
    )
    return cms

def ad():
    
    from ldap3 import Connection, Server, ALL
    
    host = "ldaps://da02army.da2nd.state.nm.us:636"
    dn = "CN=DA2nd Applications LDAP,OU=Utilities,DC=DA2ND,DC=STATE,DC=NM,DC=US"
    pw = "Twelve0six"
    server = Server(host, use_ssl=True, get_info=ALL)
    conn = Connection(server, dn, pw, auto_bind=True)
    
    return conn

# def cms():
#     import pyodbc        
#     cms = pyodbc.connect("Driver={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.8.so.1.1};"
#                           "Server=192.168.150.31;"
#                           "Database=2da_cms;"
#                           "UID=rtsqluser;"
#                           "PWD=7rK&Rk1ezV^sQ$za4MTo#iWE")
#     return cms

# def google_credentials():
#     import json

#     p = Path(__file__).parent.joinpath("includes").joinpath("credentials.json")
#     with p.open("r") as f:
#         g_dict = json.load(f)
#     return g_dict

