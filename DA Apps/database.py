from sqlalchemy import create_engine
from sqlalchemy import Table, column, select, update, insert, MetaData

def engine():
    connection = open("postgres_config", "r").read()
    engine = create_engine(connection)
    return engine

def add(table, values):
    conn = engine()
    metadata = MetaData(bind=conn)
    target_table = Table(table, metadata, autoload=True)
    i = insert(target_table)
    i = i.values(values)
    conn.execute(i)

def get_email_autocomplete():
    emails = {}
    conn = engine()
    metadata = MetaData(bind=conn)
    target_table = Table('users', metadata, autoload=True)
    query = select([target_table.columns.email])
    result = conn.execute(query).fetchall()
    for row in result:
        if row[0] != None:
            emails[row[0]] = row[0]
    return emails

def search_user_database(email):
    conn = engine()
    metadata = MetaData(bind=conn)
    target_table = Table('users', metadata, autoload=True)
    query = select([
        target_table.columns.first_name,
        target_table.columns.last_name,
        target_table.columns.user_type,
        target_table.columns.user_id,
        target_table.columns.division,
        target_table.columns.title,
        target_table.columns.supervisor
        ]).where(target_table.columns.email == email)
    result = conn.execute(query).fetchall()
    for row in result:
        print(row)