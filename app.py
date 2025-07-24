import streamlit as st
from dotenv import load_dotenv
from utils.pdf_utils import load_and_embed_pdf
from utils.speech_utils import get_speech_input
from utils.agent_tools import get_tools
from utils.agent_executor import get_agent_executor
from utils.tts_utils import text_to_audio
from langchain.memory import ConversationBufferMemory

load_dotenv()

st.set_page_config(page_title="LangChain AI Agent", layout="centered")
st.title("🤖 AI Agent (RAG + Web + Wiki + Voice + TTS + Memory)")

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "agent_executor" not in st.session_state:
    st.session_state.agent_executor = None
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Mode
search_mode = st.radio("🔍 Search Mode:", ["📄 RAG Only", "🌐 Global (PDF + Web + Wiki)"], horizontal=True)

# PDF Upload
uploaded_file = st.file_uploader("📄 Upload PDF", type="pdf")

# Load Agent Executor
if uploaded_file and st.session_state.agent_executor is None:
    with st.spinner("Processing PDF and initializing agent..."):
        chunks, retriever, _ = load_and_embed_pdf(uploaded_file)
        tools = get_tools(retriever=retriever, mode="global" if search_mode == "🌐 Global (PDF + Web + Wiki)" else "rag")
        st.session_state.agent_executor = get_agent_executor(tools, st.session_state.memory)
    st.success("✅ Agent ready!")

elif not uploaded_file and st.session_state.agent_executor is None and search_mode == "🌐 Global (PDF + Web + Wiki)":
    with st.spinner("Initializing agent without PDF..."):
        tools = get_tools(retriever=None, mode="global")
        st.session_state.agent_executor = get_agent_executor(tools, st.session_state.memory)
    st.success("✅ Global agent initialized!")

# Input
query_option = st.radio("🧾 Input Method", ["🗣️ Voice", "⌨️ Text"], horizontal=True)
query = None

if st.session_state.agent_executor:
    if query_option == "🗣️ Voice":
        if st.button("🎤 Record & Ask"):
            with st.spinner("Listening..."):
                query = get_speech_input()
                st.write(f"🗣️ You said: `{query}`")
    else:
        query = st.text_input("Enter your question", key="text_query")
        ask_button = st.button("🔎 Ask")

    if (query_option == "🗣️ Voice" and query) or (query_option == "⌨️ Text" and ask_button and query):
        with st.spinner("Thinking..."):
            response_dict = st.session_state.agent_executor.invoke({"input": query})
            answer = response_dict["output"]
            steps = response_dict.get("intermediate_steps", [])
            source = steps[-1][0].tool if steps else "Unknown"

            full_answer = f"📚 **Source**: `{source}`\n\n🧠 **Answer**: {answer}"
            st.session_state.chat_history.append((query, full_answer))

            audio_path = text_to_audio(answer)
            with open(audio_path, "rb") as audio_file:
                st.audio(audio_file.read(), format="audio/mp3", autoplay=True)

# Chat History
if st.session_state.chat_history:
    st.markdown("### 🧵 Conversation History:")
    for i, (q, a) in enumerate(reversed(st.session_state.chat_history), 1):
        st.markdown(f"**❓ Q{i}:** {q}")
        st.markdown(a)
        st.markdown("---")
