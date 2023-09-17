import streamlit as st
import streamlit_authenticator as stauth


import yaml
from yaml.loader import SafeLoader
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

hashed_passwords = stauth.Hasher(['abc', 'def']).generate()

from google.cloud import firestore

# Authenticate to Firestore with the JSON account key.
db = firestore.Client.from_service_account_json("firestore.json")

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

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{name}*')
    st.title('Some content')
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')


if authentication_status:
    try:
        if authenticator.reset_password(username, 'Reset password'):
            st.success('Password modified successfully')
    except Exception as e:
        st.error(e)

try:
    if authenticator.register_user('Register user', preauthorization=False):
        st.success('User registered successfully')
except Exception as e:
    st.error(e)  

try:
    username_forgot_pw, email_forgot_password, random_password = authenticator.forgot_password('Forgot password')
    if username_forgot_pw:
        st.success('New password sent securely')
        # Random password to be transferred to the user securely
    else:
        st.error('Username not found')
except Exception as e:
    st.error(e)
try:
    username_forgot_username, email_forgot_username = authenticator.forgot_username('Forgot username')
    if username_forgot_username:
        st.success('Username sent securely')
        # Username to be transferred to the user securely
    else:
        st.error('Email not found')
except Exception as e:
    st.error(e)

if authentication_status:
    try:
        if authenticator.update_user_details(username, 'Update user details'):
            st.success('Entries updated successfully')
    except Exception as e:
        st.error(e)  


with open('config.yaml', 'w') as file:
    yaml.dump(config, file, default_flow_style=False)          

