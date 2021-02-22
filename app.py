import uuid
import requests
from flask import Flask, jsonify, request, render_template, session, url_for, redirect
from flask_session import Session # https://pythonhosted.org/Flask-Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
import msal
import struct
import pyodbc
import os
from os.path import join, dirname, realpath
import pandas as pd
import io
from sql import getSQLConnection
from datetime import datetime


# when working local, set Local to True and copy app_config to app_config_local to put in values.  This will be in Git ignore and won't be pulled into source.  
Local = True

if Local==False:
    import app_config as app_config
else:
    import app_config_local as app_config


#import pandas as pd

app = Flask(__name__)
app.config.from_object(app_config)
Session(app)


# This section is needed for url_for("foo", _external=True) to automatically
# generate http scheme when this sample is running on localhost,
# and to generate https scheme when it is deployed behind reversed proxy.
# See also https://flask.palletsprojects.com/en/1.0.x/deploying/wsgi-standalone/#proxy-setups
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)



#Routing
@app.route('/')
def home():
    #un comment below for auth.
    if not session.get("user"):
        return redirect(url_for("login"))
    return render_template('index.html')

@app.route("/login")
def login():
    # Technically we could use empty list [] as scopes to do just sign in,
    # here we choose to also collect end user consent upfront
    session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE)
    return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)

@app.route('/launchplans')
def launchesearch():
    if not session.get("user"):
        return redirect(url_for("login"))
    return render_template('launchplans.html')   

@app.route('/launchinsights')
def launchinsights():
    if not session.get("user"):
        return redirect(url_for("login"))
    return render_template('launchinsights.html')

@app.route('/launchprofile')
def launches():
    if not session.get("user"):
        return redirect(url_for("login"))
    return render_template('launchprofile.html')

@app.route(app_config.REDIRECT_PATH)  # Its absolute URL must match your app's redirect_uri set in AAD
def authorized():
    try:
        cache = _load_cache()
        result = _build_msal_app(cache=cache).acquire_token_by_auth_code_flow(
            session.get("flow", {}), request.args)
        if "error" in result:
            return render_template("auth_error.html", result=result)
        session["user"] = result.get("id_token_claims")
        _save_cache(cache)
    except ValueError:  # Usually caused by CSRF
        pass  # Simply ignore them
    return redirect(url_for("/"))

@app.route("/logout")
def logout():
    session.clear()  # Wipe out user and its token cache from session
    return redirect(  # Also logout from your tenant's web session
        app_config.AUTHORITY + "/oauth2/v2.0/logout" +
        "?post_logout_redirect_uri=" + url_for("index", _external=True))

# Auth Helper Functions
def _load_cache():
    cache = msal.SerializableTokenCache()
    if session.get("token_cache"):
        cache.deserialize(session["token_cache"])
    return cache
def _save_cache(cache):
    if cache.has_state_changed:
        session["token_cache"] = cache.serialize()
def _build_msal_app(cache=None, authority=None):
    return msal.ConfidentialClientApplication(
        app_config.CLIENT_ID, authority=authority or app_config.AUTHORITY,
        client_credential=app_config.CLIENT_SECRET, token_cache=cache)
def _build_auth_code_flow(authority=None, scopes=None):
    return _build_msal_app(authority=authority).initiate_auth_code_flow(
        scopes or [],
        redirect_uri=url_for("authorized", _external=True))
def _get_token_from_cache(scope=None):
    cache = _load_cache()  # This web app maintains one cache per session
    cca = _build_msal_app(cache=cache)
    accounts = cca.get_accounts()
    if accounts:  # So all account(s) belong to the current signed-in user
        result = cca.acquire_token_silent(scope, account=accounts[0])
        _save_cache(cache)
        return result
# SQL Helper functions
def _getSQLToken():
    clientSecret = app_config.CLIENT_SECRET
    clientID = app_config.CLIENT_ID
    authority_url = app_config.AUTHORITY
    context = msal.ConfidentialClientApplication(client_id=clientID, client_credential=clientSecret,authority=authority_url)
    token = context.acquire_token_for_client(scopes=[app_config.SQLRESOURCE])
    return token
#APIS     

@app.route('/launchprofiles', methods=['GET', 'POST'])
def launchprofiles():
    if not session.get("user"):
        return redirect(url_for("login"))
    if request.method == 'POST':
        data = request.form.to_dict()
        print(data)
        #df = pd.DataFrame.from_dict(data)
        conn = getSQLConnection(app_config=app_config)
        with conn.cursor() as cursor:
            insert = text('INSERT INTO [launchmodeldev].[dbo].[FactLaunchProfiles] VALUES(NEWID(),?,?,?,?,?,?,?,?,?,?,?,?,?)')
            LaunchName = data.get('launchnameid')
            CodeName = data.get('codenameid')
            LOB = data.get('lobid')
            LaunchDate = data.get('launchdateid')
            PQS = data.get('pqsdateid')
            LaunchType = data.get('launchtypeid')
            Region = data.get('regionsid')
            AnnouceDate = data.get('annoucedateid')
            IPQRegion = data.get('ipqregionid')
            RetailDTSVolume = data.get('retaildtsvolume')
            Notes = data.get('pqsdateid')
            ChangeDate = datetime.now()
            UpdatedBy = 'chosbo@microsoft.com'
            params =(LaunchName,CodeName,LOB,LaunchDate,PQS,LaunchType,Region,AnnouceDate,IPQRegion,RetailDTSVolume,Notes,ChangeDate,UpdatedBy)
            cursor.execute(str(insert),params)
            print("Entered")
        return(print("Success"))

    if request.method == 'GET':
        data = request.get_json()
        conn = getSQLConnection(app_config=app_config)
        with conn.cursor() as cursor:
            id = cursor.execute("SELECT DISTINCT * FROM [launchmodeldev].[dbo].[FactLaunchProfiles]")
            columns = [column[0] for column in id.description]
            print(columns)
            results = []
            for row in id.fetchall():
                results.append(dict(zip(columns, row)))
        return jsonify(results)

@app.route('/launchplanning', methods=['GET', 'POST'])
def launchplans():
    if not session.get("user"):
        return redirect(url_for("login"))
     if request.method == 'GET':
        data = request.get_json()
        conn = getSQLConnection(app_config=app_config)
        with conn.cursor() as cursor:
            id = cursor.execute("SELECT DISTINCT * FROM [launchmodeldev].[dbo].[FactLaunchPlans]")
            columns = [column[0] for column in id.description]
            print(columns)
            results = []
            for row in id.fetchall():
                results.append(dict(zip(columns, row)))
            print(jsonify(results))
        return jsonify(results)


'''          
    @app.route('/launchprofiles',methods=['GET','POST'])
    def launchprofiles():
        if request.method == "GET":
            mylist = []
            conn = getSQLConnection(app_config=app_config)
            with conn.cursor() as cursor:
                id = cursor.execute("SELECT DISTINCT ID,Name FROM [launchmodeldev].[dbo].[FactLaunchProfiles]")
                result = id.fetchall()
            print(result)
            return str(result)
        #for launch in launches:
        #   launch = {'LaunchName':launch['name']}
        #   mylist.append(launch)
        # '''


launches = [
    {
        'launchName':"Spring Launch",
        "sku":[
            {
            "skuName": "Surface Laptop",
            "price": 109
            }
        ]
    }
]

launches = [
    {
        'LaunchProfile':"id",
        "data":[
            {
            "name": "FalconX",
            "launchdate": "12/12/12",
            "changedate": "12/12/12"
            }

        ]
    }
]


''''
#Post, add a launch
@app.route('/launchprofiles',methods=['POST'])
def create_launch():
    request_data = request.get_json()
    #new_launch = {'launchName':request_data['data']}
    return request_data
'''
launches = [
    
    {'id': 12,
    'name':'FalconX'}, 
    {'id': 13,
    'name':'FalconB'}
]
'''
@app.route('/launchprofiles',methods=['GET'])
def get_allLaunches():
    mylist = []
    for launch in launches:
        launch = {'LaunchName':launch['name']}
        mylist.append(launch)

    return jsonify(mylist)
'''

@app.route("/uploadfile", methods=['POST'])
def uploadFiles():
    if not session.get("user"):
        return redirect(url_for("login"))
    if request.method=="POST":
        f = request.files['fileupload']
        print(f)
        form = request.form
        for key in form.keys():
            for value in form.getlist(key):
                print(key,":",value)
        fstring = f.read()
        text_obj = fstring.decode('UTF-8')
        data = io.StringIO(text_obj)
        df = pd.read_csv(data,sep=",")
        #df = df.drop(label, inplace=True)
        
        #csv_dicts = [{k: v for k, v in row.items()} for row in csv.DictReader(fstring.splitlines(), skipinitialspace=True)]  
        print(df)
    return("Success")





'''
@app.route("/uploadfile", methods=['POST'])
def uploadFiles():
    if request.method=="POST":
        f = request.files['fileupload']
        test = request.form['form-select']
        print(test)
        form = request.form
        for key in form.keys():
            for value in form.getlist(key):
                print(key,":",value)
        fstring = f.read()
        text_obj = fstring.decode('UTF-8')
        data = io.StringIO(text_obj)
        df = pd.read_csv(data,sep=",")
        #csv_dicts = [{k: v for k, v in row.items()} for row in csv.DictReader(fstring.splitlines(), skipinitialspace=True)]  
        print(df)
    return("Success")
'''
    
    #return render_template("templates/launchplans.html")



#Post, add an item to a launch
@app.route('/launch/<string:name>/sku',methods=['POST'])
def create_sku_in_launch(name):
    if not session.get("user"):
        return redirect(url_for("login"))
    request_data = request.get_json()
    for launch in launches:
        if launch['launchName'] == name:
            new_sku = {'skuName':request_data['skuName'],'price':request_data['price']}
            launch['sku'].append(new_sku)
            return jsonify(new_sku)
    return jsonify({"Message":"That launch is not found!"})

#@app.route('/launch/<string:name>/file',methods=['POST'])
#def upload_launch_file(name):
    

#GET a specific Launch
@app.route('/launch/<string:name>')
def get_launch(name):
    if not session.get("user"):
        return redirect(url_for("login"))
    for launch in launches:
        if launch["launchName"] == name:
            return jsonify(launch)
    return jsonify({"message":"Launch Not Found"})

#GET all skus in a specific launch 
@app.route('/launch/<string:name>/sku')
def get_sku_in_launch(name):
    if not session.get("user"):
        return redirect(url_for("login"))
    for launch in launches:
        if launch["launchName"] == name:
            return jsonify({'sku':launch['sku']})
    return jsonify({"message":"Sku Not Found"})


app.jinja_env.globals.update(_build_auth_code_flow=_build_auth_code_flow)  # Used in template

if __name__ == '__main__':
    app.run(port=5000)