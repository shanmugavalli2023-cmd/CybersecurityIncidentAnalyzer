import streamlit as st
from groq import Groq
import os

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Cybersecurity Incident Analyzer",
    page_icon="🛡️",
    layout="wide"
)

# =====================================================
# TITLE
# =====================================================

st.title("🛡️ AI Powered Cybersecurity Incident Analyzer")

st.markdown("""
Built using Groq + Streamlit
""")

# =====================================================
# API KEY
# =====================================================

# Read GROQ_API_KEY from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Check if the API key is available
if not GROQ_API_KEY:
    st.error("Groq API Key not found. Please set the GROQ_API_KEY environment variable.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# =====================================================
# SESSION MEMORY
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =====================================================
# DISPLAY CHAT HISTORY
# =====================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =====================================================
# USER INPUT
# =====================================================

user_input = st.chat_input(
    "Describe cybersecurity incident..."
)

# =====================================================
# AI RESPONSE
# =====================================================

if user_input:

    # Store User Message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Display User Message
    with st.chat_message("user"):
        st.markdown(user_input)

    # AI Response
    with st.chat_message("assistant"):

        with st.spinner("Analyzing Threat..."):

            prompt = f"""
            You are an expert AI Cybersecurity Analyst.

            Analyze this cybersecurity incident.

            Incident:
            {user_input}

            Generate:

            1. Incident Type
            2. Severity Level
            3. Attack Pattern
            4. Affected Systems
            5. Threat Analysis
            6. Mitigation Strategies
            7. Prevention Recommendations
            8. Final Security Assessment
            """

            try:

                completion = client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a cybersecurity expert."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.3,
                    max_tokens=1024
                )

                response = completion.choices[0].message.content

                st.markdown(response)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response
                    }
                )

            except Exception as e:

                st.error(f"Error: {e}")
