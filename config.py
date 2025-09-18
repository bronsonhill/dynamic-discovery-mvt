import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import os

def initialize_firebase():
    """Initialize Firebase connection if not already initialized."""
    if not firebase_admin._apps:
        # Try to get Firebase credentials from Streamlit secrets first
        try:
            # For Streamlit Cloud deployment
            firebase_config = st.secrets["firebase"]
            cred = credentials.Certificate({
                "type": firebase_config["type"],
                "project_id": firebase_config["project_id"],
                "private_key_id": firebase_config["private_key_id"],
                "private_key": firebase_config["private_key"],
                "client_email": firebase_config["client_email"],
                "client_id": firebase_config["client_id"],
                "auth_uri": firebase_config["auth_uri"],
                "token_uri": firebase_config["token_uri"],
                "auth_provider_x509_cert_url": firebase_config["auth_provider_x509_cert_url"],
                "client_x509_cert_url": firebase_config["client_x509_cert_url"]
            })
        except:
            # For local development - use service account key file
            if os.path.exists("firebase_key.json"):
                cred = credentials.Certificate("firebase_key.json")
            else:
                st.error("Firebase credentials not found. Please add firebase_key.json or configure Streamlit secrets.")
                st.stop()
        
        firebase_admin.initialize_app(cred)
    
    return firestore.client()

# Initialize database connection
def get_db():
    """Get Firestore database client."""
    return initialize_firebase()
