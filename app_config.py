import os

CLIENT_ID = "9c66ac20-b784-4480-9966-a33083937ac9" # Application (client) ID of app registration

CLIENT_SECRET = os.getenv("MICROSOFT_PROVIDER_AUTHENTICATION_SECRET")
if not CLIENT_SECRET:
    raise ValueError("Need to define CLIENT_SECRET environment variable")

AUTHORITY = "https://login.microsoftonline.com/72f988bf-86f1-41af-91ab-2d7cd011db47"

SQLRESOURCE = 'HTTPS://database.windows.net/.default'

#DEBUG = True
MAXSERVER = os.getenv("MAXSERVER")
MAXDATABASE = os.getenv("MAXDATABASE")
SQLSERVER= os.getenv("SQL_Server")
if not SQLSERVER:
    raise ValueError("Need to define SQL_SERVER environment variable")

SQLDATABASE=os.getenv("SQL_DATABASE")
if not SQLDATABASE:
    raise ValueError("Need to define SQL_DATABASE environment variable")

REDIRECT_PATH = "/getAToken"  # Used for forming an absolute URL to your redirect URI.
                              # The absolute URL must match the redirect URI you set
                              # in the app's registration in the Azure portal.

SCOPE = ["User.Read"]

SESSION_TYPE = "filesystem"  # Specifies the token cache should be stored in server-side session

