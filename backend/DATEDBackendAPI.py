import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import Flask, request
import json

app = Flask(__name__)

cred = credentials.Certificate('auth.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


def login_data_validation(username, password):
    if (username == "" or password == ""):
        return False

    if (type(username) != str or type(password) != str):
        return False

    return True


def signup_data_validation(username=None, password=None, DOB=None, ID=None, firstName=None,lastName=None ):
    data = (username, password, DOB, ID, firstName, lastName)

    for loop in data:
        if loop == "":
            return False

    for loop in data:
        if type(loop) != str:
            return False

    return True

def signup_data_duplicate_check(username=None):
    doc_ref = db.collection(u'users')
    query_ref = doc_ref.where(u'username', u'==', username).stream()

    return_value = []

    for doc in query_ref:
        return_value = doc.to_dict()

    if (len(return_value) == 0):
        return False

    return True



@app.route('/')
def homePage():
    return "This is Google App Engine. Select a proper Route."


@app.route('/login', methods = ['POST', 'GET'])
def login():

    if request.method == 'GET':
        return "Access Denied"

    username = request.form.get('username')
    password = request.form.get('password')

    print(login_data_validation(username,password))
    if (login_data_validation(username,password) == False):
        print("Functon")
        return "Please Provide Valid Datatype <String>. Function: Flask/Login/Data_Validation"


    doc_ref = db.collection(u'users')
    query_ref = doc_ref.where(u'username',u'==',username).where(u'password', u'==', password).stream()

    return_value = []

    for doc in query_ref:
        return_value = doc.to_dict()
        print(u'{} => {}'.format(doc.id, type(doc.to_dict())))

    if (len(return_value) == 0):
        return "No Data found. Please update User/Signup"


    return json.dumps(return_value)


@app.route('/signup', methods = ['POST', 'GET'])
def signup():

    if request.method == 'GET':
        return "Access Denied"



    doc_ref   = db.collection(u'users')
    username  = request.form.get('username')
    password  = request.form.get('password')
    DOB       = request.form.get('DOB')
    firstName = request.form.get('firstName')
    lastName  = request.form.get('lastName')
    if(signup_data_duplicate_check(username)):
        return "Duplicate Data"


    #query_ref = doc_ref.where(u'first', u'==', u'Ada').stream()


    #if (signup_data_duplicate_check(username, "25") == False):
    #    return "Duplicate Account Detected. Please Enter new data"


    data = {
        u'DOB': DOB,
        u'username': username,
        u'password': password,
        u'firstName' : firstName,
        u'lastName'  : lastName,
        u'ID'        : 25
    }

    doc_ref.add(data)

    return "DONE"


@app.route('/overview', methods = ['POST', 'GET'])
def overview():
    if request.method == 'GET':
        return "Access Denied"

    token    = request.args.get('ID')
    doc_ref = db.collection(u'Overview')
    query_ref = doc_ref.where(u'UniqueID',u'==',27275).stream()

    data = []
    print(query_ref)
    for docs in query_ref:
        data = docs.to_dict()
        print(u'{} => {}'.format(docs.id, type(docs.to_dict())))

    if (len(data) == 0):
        return "NO DATA Found"
    return json.dumps(data)



@app.route('/teams', methods = ['POST', 'GET'])
def teams():
    if request.method == 'GET':
        return "Access Denied"

    ID = request.form.get('ID')
    doc_ref = db.collection(u'teams')
    query_ref = doc_ref.where(u'scoutID',u'==','27275').stream()

    data = []
    print(query_ref)
    for docs in query_ref:
        data = docs.to_dict()

        #This returns all the values
        #print(docs.to_dict())

    return json.dumps(data)


@app.route('/fundraisersGroups', methods = ['POST','GET'])
def fundraisersGroups():
    if request.method == 'GET':
        return "Access Denied"

    doc_ref = db.collection(u'fundraiser')
    query_ref = doc_ref.where(u'fundraiserID', u'==', u'167').stream()
    data = []
    for docs in query_ref:
        data = docs.to_dict()


    #if (1):
        #return "404"
    return json.dumps(data)




if __name__ == '__main__':
    app.run(debug=True)
    #Port 8080
