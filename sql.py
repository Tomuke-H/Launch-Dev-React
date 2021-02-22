import struct
import pyodbc
import msal

def getSQLToken(app_config):

    clientSecret = app_config.CLIENT_SECRET
    clientID = app_config.CLIENT_ID
    authority_url = app_config.AUTHORITY
    context = msal.ConfidentialClientApplication(client_id=clientID, client_credential=clientSecret,authority=authority_url)
    token = context.acquire_token_for_client(scopes=[app_config.SQLRESOURCE])
    return token

def getSQLConnection(app_config):
    token = getSQLToken(app_config)
    tokenb = bytes(token["access_token"], "UTF-8")
    exptoken = b''

    for i in tokenb:
        exptoken += bytes({i})
        exptoken += bytes(1)

    tokenstruct = struct.pack("=i", len(exptoken)) + exptoken

    driver = "Driver={ODBC Driver 17 for SQL Server}"
    server = ";SERVER={0}".format(app_config.SQLSERVER)
    database = ";DATABASE={0}".format(app_config.SQLDATABASE)

    connString = driver + server + database

    SQL_COPT_SS_ACCESS_TOKEN = 1256
    conn = pyodbc.connect(connString, attrs_before={SQL_COPT_SS_ACCESS_TOKEN:tokenstruct})
    return conn