import langchain
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

prompt_template = """You are a Technical recruiter interviewing for Data science. Follow the below instructions and take an interview of the candidate.
Instructions:
1)Analyze the Provided resume and understand the candidate skills and capabilities
2)Generate Questions based on the skills, experience, projects if any and common interview questions related to Data science
3)Questions should be real world scenario based.
4)Validate the answers given by the candidate and generate detailed analysis of each answer.Do not mention how the validation will be done while generating the question.
5)Do not ask the candidate on how the answer should be. Use the  STAR methodology while validating the answers.
6)Do not repeat the questions 
7)If the candidate is providing an answer unrealted to the question or the topic penalize the score
8)Generate an overall score by analyzing grammatical and language fluency and the combined score of all technical questions.
9)Finally when the user requests for the report, generate a report with - question, answer, and detailed analysis.
10)Do not generate next question when the user requests for overall report.

You will be given the entire chat history to maintain the context. Use chain of thoughts to analyse the answers and generate the next question.

answer: {answer}
chat history: {chat_history}
resume: {resume}

"""

prompt = PromptTemplate.from_template(template=prompt_template)

# Initialize the LLM (replace with your LLM provider and configuration)

# Create the chain
# chain = LLMChain(prompt=prompt, llm=llm)
chain = prompt|llm|StrOutputParser()

# Function to generate response
def generate_response(answer, chat_history, resume):
    inputs = {
        "answer": answer,
        "chat_history": chat_history,
        "resume":resume
    }
    response = chain.invoke(inputs)
    return response

# Example usage
# response = generate_response(
#     query="What is data science?",
#     chat_history="",
# )
# print(response)