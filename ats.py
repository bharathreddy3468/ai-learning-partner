import streamlit as st
import PyPDF2 as pdf
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser

# load_dotenv()
# ## load the GROQ API Key
# os.environ['GROQ_API_KEY']=os.getenv("GROQ_API_KEY")

# groq_api_key=os.getenv("GROQ_API_KEY")

groq_api_key = st.secrets['API_KEYS'].get("GROQ_API_KEY", 'no api key found')

llm=ChatGroq(groq_api_key=groq_api_key,model_name="gemma2-9b-it")

prompt_template = """ You are a Techincal recruiter with lots of experience in the field of Data Science/AI. Review the following resume
and share precise summary. Compare it with the given JD and analyse the following

1)Percentage match - weightage:50%
2)Detect all the sections in the resume(example : skills, experience, projects, etc..)
2)Missing Key words - weightage:20%
3)spelling and grammatical mistakes - weightage:10%
4)Highly repetative words (only if they are not key words and just a common word which does not add any value) - weightage:10%
5)Section wise analysis which are strong sections and weak sections - weightage:10%
6)Compute overall score for the resume based on all the above criteria with their respective weightage
7)Interpret the overscore in detial without revealing the actual criteria
8)Provide scope of improve with respect to all the above points.

Be very accurate with requirements.

resume: {text}
JD: {JD}

percentage match(%): \n\n
missing key words:
Overall Score:
"""


def ats():
    st.title('ATS checker')
    JD = st.text_area(label='Provide your Job description')
    fu = st.file_uploader(label='upload your resume to get the ats score', type='pdf')

    if fu:
        with st.status('Processing your resume...'):
            reader=pdf.PdfReader(fu)
            text=""
            for page in range(len(reader.pages)):
                page=reader.pages[page]
                text+=str(page.extract_text())

            prompt = PromptTemplate(template=prompt_template, input_variables=[text, JD])
            output_parser=StrOutputParser()

            chain  = prompt|llm|output_parser
            response = chain.invoke({'text':text, 'JD':JD})
        st.write(response)