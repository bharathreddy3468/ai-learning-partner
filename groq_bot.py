import os
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder
from langchain_community.vectorstores import FAISS



from dotenv import load_dotenv
load_dotenv()
## load the GROQ API Key
os.environ['GROQ_API_KEY']=os.getenv("GROQ_API_KEY")

groq_api_key=os.getenv("GROQ_API_KEY")

llm=ChatGroq(groq_api_key=groq_api_key,model_name="Llama3-8b-8192")

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vdb = FAISS.load_local('C:/Users/bhara/OneDrive/Desktop/ai/interviewbot/faiss_index', embeddings, allow_dangerous_deserialization=True)

retriever=vdb.as_retriever()


system_prompt=(
    """
    Answer the questions based on the provided context only if the query and context are related.
    Else generate an appropriate response for the query.
    Please provide the most accurate respone based on the question.

    if the user is trying to greet you or trying to end the conversation do not mention that this is out of context and just generate the response
    <context>
    {context}
    <context>
    Question:{input}

    """

)

contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)

contextualize_q_prompt= ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

history_aware_retriever=create_history_aware_retriever(llm,retriever,contextualize_q_prompt)
history_aware_retriever

qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

document_chain=create_stuff_documents_chain(llm,qa_prompt)
retrieval_chain=create_retrieval_chain(history_aware_retriever,document_chain)


def generate_response(query, chat_history):

    response=retrieval_chain.invoke({"input":query.strip(),"chat_history":chat_history})

    return response['answer']

