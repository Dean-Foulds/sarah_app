import streamlit as st
import streamlit_authenticator as stauth
from google.cloud import firestore
from google.oauth2 import service_account



# Authenticate to Firestore with the JSON account key.
import json
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="sarah-app-2023")

st.sidebar.success("Select a demo above.")

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
	"title": "Apple",
	"url": "www.apple.com"
})






          

