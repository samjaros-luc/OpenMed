import firebase_admin
from firebase_admin import auth, credentials, firestore
from google.cloud.firestore_v1 import client as db

##############################################
# Make app to interact with auth & firestore #
##############################################
# Documentation for client : https://googleapis.dev/python/firestore/latest/client.html
# Documentation for firebase_admin : https://firebase.google.com/docs/reference/admin/python
# Get creditentails using token from service account (.json file, Sam can send it to you)
cred = credentials.Certificate("C:/Users/samja/OneDrive/Loyola - Semester 8/COMP 363/OpenMed/openmed-comp363-firebase-adminsdk-qglti-767b82d10f.json")
# Create instance of application
app = firebase_admin.initialize_app(cred)

######################
# Interact with auth #
######################
username = "pass_is_password@gmail.com"   # Credentials given by user
password = "password"
user = None
try:
    user = firebase_admin.auth.get_user_by_email(username, app=app)   # Create
except auth.UserNotFoundError:
    print("The user was not found")



###########################
# Interact with firestore #
###########################
# Create client for interacting with firestore
# Documentation : https://googleapis.dev/python/firestore/latest/document.html
client = firestore.client(app=app)    # Create a client to edit data from. If you use the app, you are editing form the admin
# or
client = db.Client(credentials=userCred)

# Add a document
collectionRef = client.collection("patient")   # Get the Collection Reference for the collection you want to add to
patient_dict = {}   # Dictionary containing all of the patient information
patient_hash = ""   # Patient hashcode
collectionRef.add(document_data=patient_dict, document_id=patient_hash)

# Get a document
documentRef = client.document("medical_events/example")  # Get the Document Reference using the filepath (string)
# or
collectionRef = client.collection("medical_events")   # Get the Collection Reference
documentRef = collectionRef.document(document_id="example")   # Get the Document Reference

# Get a document's data
documentSnap = documentRef.get()   # .get() gets a Document Snapshot
dictionary_of_Data = documentSnap.to_dict()   # .to_dict() turns the document data into a python dictionary
does_document_exist = documentSnap.exists   # boolean whether or not the document exists
document_id = documentSnap.id   # string of document's ID
specific_field_ICD10 = documentSnap.get("ICD10")   # rather than getting a whole dictionary, you can also just get a specific field

# Update a document's data
document_data = {}   # Dictionary where keys are the field names and the values are the data
documentRef.update(document_data)
