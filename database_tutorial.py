import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

### Make app to interact with auth & firestore ###
# Documentation for client : https://googleapis.dev/python/firestore/latest/client.html
# Documentation for firebase_admin : https://firebase.google.com/docs/reference/admin/python
# Get creditentails using token from service account (.json file, Sam can send it to you)
cred = credentials.Certificate("C:/Users/samja/OneDrive/Loyola - Semester 8/COMP 363/OpenMed/openmed-comp363-firebase-adminsdk-qglti-767b82d10f.json")
# Create instance of application
app = firebase_admin.initialize_app(cred)


### Interact with auth ###


### Interact with firestore ###
# Create client for interacting with firestore
# Documentation : https://googleapis.dev/python/firestore/latest/document.html
client = firestore.client(app=app)

documentRef = client.document("medical_events/example")  # Get the Document Reference using the filepath (string)
documentSnap = documentRef.get()   # .get() gets a Document Snapshot
dictionary_of_Data = documentSnap.to_dict()   # .to_dict() turns the document data into a python dictionary
does_document_exist = documentSnap.exists   # boolean whether or not the document exists
document_id = documentSnap.id   # string of document's ID
specific_field_ICD10 = documentSnap.get("ICD10")   # rather than getting a whole dictionary, you can also just get a specific field
