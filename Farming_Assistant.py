import streamlit as st
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

st.title("🧑‍🌾 Farming Assistant")
st.subheader("Ask agriculture-related questions!")

# Load API keys from .env
load_dotenv()

llm = ChatGroq(
    model_name="mixtral-8x7b-32768",
    temperature=0.5,
    api_key=os.getenv("GROQ_API_KEY")
)

conversation = ConversationChain(
    llm=llm,
    memory=ConversationBufferMemory(),
    verbose=True
)

user_input = st.text_input("Ask something...")

if user_input:
    prompt = f"""You are a knowledgeable agricultural assistant helping farmers with real, practical advice.
Only talk about farming topics like crops, fertilizers, irrigation, pest control, and yield.
Don't talk about human emotions or random facts. Focus only on agriculture.

User: {user_input}
Assistant:"""

    reply = conversation.run(prompt)
    st.write("🧑‍🌾 Bot:", reply)
