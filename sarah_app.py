import streamlit as st
import streamlit_authenticator as stauth
from google.cloud import firestore
from google.oauth2 import service_account
# import pyrebase



# Authenticate to Firestore with the JSON account key.
import json
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="sarah-app-2023")

st.sidebar.success("^^ pages will be added added here ^^.")

# Now let's make a reference to ALL of the posts
posts_ref = db.collection("posts")

# For a reference to a collection, we use .stream() instead of .get()
for doc in posts_ref.stream():
	st.write("The id is: ", doc.id)
	st.write("The contents are: ", doc.to_dict())

# This time, we're creating a NEW post reference for Apple
doc_ref = db.collection("posts").document("Apple")

# And then uploading some data to that reference
doc_ref.set({
	"title": "App video",
	"url": "Leo Cat"
})


# firebase_config = {
# apiKey: "AIzaSyACe6cZbHMXQC2W3N1biiBqrtm0U4V-O0k",
# authDomain: "sarah-app-2023.firebaseapp.com",
# projectId: "sarah-app-2023",
# storageBucket: "sarah-app-2023.appspot.com",
# messagingSenderId: "836429532416",
# appId: "1:836429532416:web:b81fc9d093a43e8caaf7e5",
# measurementId: "G-HT0HG024LP"
# }

# firebase=pyrebase.initilize_app(firebase_config)

# storage=firebase.storage()






          

