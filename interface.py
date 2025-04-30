import streamlit as st
import Request

st.title("Simple RAG system :")


if "long_process_done" not in st.session_state:
    st.session_state.long_process_done = False

if "graph" not in st.session_state:
    st.session_state.graph = None

if not st.session_state.long_process_done:
    with st.spinner("Reading data..."):
        graph = Request.set_up(Request.API_KEY,Request.MODE)
        st.session_state.graph = graph
        st.session_state.result = "Process complete!"
        st.session_state.long_process_done = True
    
user_input = st.text_input("Enter your question:")

if st.button("Confirm"):
    st.session_state.confirmed_text = user_input

if "confirmed_text" in st.session_state:
    response = Request.get_response(st.session_state.graph,st.session_state.confirmed_text)
    st.markdown("### Response:")
    st.write(response)
