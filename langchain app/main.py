import streamlit as st 
from langchain_utils import execute_chain
import os

st.set_page_config(page_title="NL2SQL Chatbot", layout="wide")
st.title("NL2SQL Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask a question about your database:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response using LangChain
    with st.spinner("Generating SQL query and fetching results..."):
        response = execute_chain(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)