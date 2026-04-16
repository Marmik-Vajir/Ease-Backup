import firebase_admin
import os
import json
from firebase_admin import credentials, firestore

firebase_json = os.getenv("FIREBASE_CONFIG")
cred_dict = json.loads(firebase_json)
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred)
db = firestore.client()
