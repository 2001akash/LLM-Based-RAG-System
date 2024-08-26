import streamlit as st
import requests

st.title("LLM-based RAG Search")

# Input for user query
query = st.text_input("Enter your query:")

if st.button("Search"):
    # Define the Flask backend URL
    backend_url = "http://localhost:5001/query"
    
    # Make a POST request to the Flask API with the user's query
    response = requests.post(backend_url, json={'query': query})
    
    if response.status_code == 200:
        # Display the generated answer
        answer = response.json().get('answer', "No answer received.")
        st.write("Answer:", answer)
    else:
        st.error(f"Error: {response.status_code}")
