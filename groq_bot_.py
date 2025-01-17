import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.output_parsers import StrOutputParser


# from dotenv import load_dotenv
# load_dotenv()
## load the GROQ API Key
# os.environ['GROQ_API_KEY']=os.getenv("GROQ_API_KEY")

# groq_api_key=os.getenv("GROQ_API_KEY")

groq_api_key=st.secrets['API_KEYS'].get("GROQ_API_KEY", 'no api key found')

llm=ChatGroq(groq_api_key=groq_api_key,model_name="Llama3-70b-8192")

prompt_template = """You are Technical tutor with lots of experience in the field of Data science/AI. You need to answer the user quesries
with real world scenarios and practical guidence. Make the learning fun and excite the learners with your explanation. 

If the user asks something unrelated to the current scope reply with Sorry, I can only answer questions related to Data science/AI.

Use the given chat history along with the current query to maintain the flow of the conversation.

question: {query}
chat history: {chat_history}

"""

prompt = PromptTemplate.from_template(template=prompt_template)

# Initialize the LLM (replace with your LLM provider and configuration)

# Create the chain
chain = LLMChain(prompt=prompt, llm=llm)

# Function to generate response
def generate_response(query, chat_history):
    inputs = {
        "query": query,
        "chat_history": chat_history,
    }
    response = chain.invoke(inputs)
    return response['text']

# Example usage
response = generate_response(
    query="What is data science?",
    chat_history="",
)
print(response)