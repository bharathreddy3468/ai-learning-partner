import streamlit as st
from streamlit_chat import message
from langchain_core.messages import AIMessage,HumanMessage
from mi_bot import generate_response
import PyPDF2 as pdf


def mock_interview():
    fu_mi = st.file_uploader(label='upload your resume', type='pdf')

    if not fu_mi:
        st.error('Please upload your resume.')
    else:
        with st.success('Resume uploaded'):
            reader_mi=pdf.PdfReader(fu_mi)
            resume_mi=""
            for page in range(len(reader_mi.pages)):
                page=reader_mi.pages[page]
                resume_mi+=str(page.extract_text())

        if "messages_mi" not in st.session_state:
            st.session_state.messages_mi = []
            st.session_state.chat_history_mi = []


        # Display chat messages_mi from history
        for message in st.session_state.messages_mi:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
            
        # Get user input
        query = st.chat_input("Say Hello to start your interview")

        if query:
            # Add user message to chat history
            st.session_state.messages_mi.append({"role": "user", "content": query})
            # Display user message
            with st.chat_message("user"):
                st.markdown(query)

            chatbot_response = generate_response(answer=query, chat_history_mi=st.session_state.chat_history_mi, resume_mi=resume_mi)
            # Add bot message to chat history
            st.session_state.messages_mi.append({"role": "assistant", "content": chatbot_response})
            st.session_state.chat_history_mi.extend([HumanMessage(query.strip()), AIMessage(chatbot_response)])
            # Display bot message
            with st.chat_message("assistant"):
                st.markdown(chatbot_response)