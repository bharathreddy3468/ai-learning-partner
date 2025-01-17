import streamlit as st
from streamlit_chat import message
from groq_bot_ import generate_response
from langchain_core.messages import AIMessage,HumanMessage
from streamlit_option_menu import option_menu
from ats import ats


with st.sidebar:
    selected = option_menu(
        menu_title= "Main menu",
        options=['Home','ATS checker'],
        default_index=0
    )

if selected == 'ATS checker':
    ats()


if selected=='Home':
# Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.chat_history = []
    

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
        
    # Get user input
    query = st.chat_input("Your message")

    if query:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": query})
        # Display user message
        with st.chat_message("user"):
            st.markdown(query)

        chatbot_response = generate_response(query=query, chat_history=st.session_state.chat_history)
        # Add bot message to chat history
        st.session_state.messages.append({"role": "assistant", "content": chatbot_response})
        st.session_state.chat_history.extend([HumanMessage(query.strip()), AIMessage(chatbot_response)])
        # Display bot message
        with st.chat_message("assistant"):
            st.markdown(chatbot_response)