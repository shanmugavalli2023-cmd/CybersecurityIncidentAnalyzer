
import streamlit as st
from dotenv import load_dotenv
import os

# LangChain Imports
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate

# Groq LLM
from langchain_groq import ChatGroq

# ---------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

# ---------------------------------------------------
# Streamlit Page Config
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Powered Chatbot")
st.markdown("Built using LangChain + Groq + Streamlit")

# ---------------------------------------------------
# Initialize Session State
# ---------------------------------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------------------------------------------
# Initialize LLM
# ---------------------------------------------------

llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama3-8b-8192",
    temperature=0.7
)

# ---------------------------------------------------
# Conversation Memory
# ---------------------------------------------------

memory = ConversationBufferMemory()

# ---------------------------------------------------
# Prompt Template
# ---------------------------------------------------

template = """
You are an intelligent AI assistant.

Current conversation:
{history}

Human: {input}
AI Assistant:
"""

prompt = PromptTemplate(
    input_variables=["history", "input"],
    template=template
)

# ---------------------------------------------------
# Conversation Chain
# ---------------------------------------------------

conversation = ConversationChain(
    llm=llm,
    memory=memory,
    prompt=prompt,
    verbose=False
)

# ---------------------------------------------------
# User Input
# ---------------------------------------------------

user_input = st.chat_input("Ask me anything...")

# ---------------------------------------------------
# Chat Processing
# ---------------------------------------------------

if user_input:

    # Store User Message
    st.session_state.chat_history.append(
        ("user", user_input)
    )

    try:

        # Generate AI Response
        response = conversation.predict(
            input=user_input
        )

        # Store AI Response
        st.session_state.chat_history.append(
            ("assistant", response)
        )

    except Exception as e:
        st.error(f"Error: {e}")

# ---------------------------------------------------
# Display Chat Messages
# ---------------------------------------------------

for role, message in st.session_state.chat_history:

    with st.chat_message(role):
        st.markdown(message)
