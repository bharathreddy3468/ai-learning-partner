import streamlit as st
from streamlit_chat import message
from langchain_core.messages import AIMessage,HumanMessage
from mi_bot import generate_response
import PyPDF2 as pdf



fu = st.file_uploader(label='upload your resume to get the ats score', type='pdf')

if not fu:
    st.error('Please upload your resume.')
else:
    with st.success('Resume uploaded'):
        reader=pdf.PdfReader(fu)
        resume=""
        for page in range(len(reader.pages)):
            page=reader.pages[page]
            resume+=str(page.extract_text())

    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.chat_history = []


    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
        
    # Get user input
    query = st.chat_input("Say Hello to start your interview")

    if query:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": query})
        # Display user message
        with st.chat_message("user"):
            st.markdown(query)

        chatbot_response = generate_response(answer=query, chat_history=st.session_state.chat_history, resume=resume)
        # Add bot message to chat history
        st.session_state.messages.append({"role": "assistant", "content": chatbot_response})
        st.session_state.chat_history.extend([HumanMessage(query.strip()), AIMessage(chatbot_response)])
        # Display bot message
        with st.chat_message("assistant"):
            st.markdown(chatbot_response)