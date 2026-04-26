import streamlit as st
from groq import Groq

st.set_page_config(page_title="Aria AI Chatbot", page_icon="✦", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600&display=swap');
html, body, [class*="css"] { font-family: 'Sora', sans-serif; background-color: #0c0b14; color: #f1f0ff; }
.stApp {
    background: radial-gradient(ellipse at 20% 20%, rgba(124,111,255,0.12), transparent 60%),
                radial-gradient(ellipse at 80% 80%, rgba(192,132,252,0.08), transparent 60%), #0c0b14;
}
.stChatMessage { background: rgba(255,255,255,0.05) !important; border: 1px solid rgba(124,111,255,0.15) !important; border-radius: 16px !important; padding: 12px !important; }
textarea { background: rgba(255,255,255,0.05) !important; border: 1px solid rgba(124,111,255,0.3) !important; border-radius: 12px !important; color: #f1f0ff !important; font-family: 'Sora', sans-serif !important; }
h1 { background: linear-gradient(135deg, #7c6fff, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 600; font-size: 2rem !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("# ✦ Aria — AI Chatbot")
st.markdown("<p style='color: rgba(241,240,255,0.5); margin-top: -12px; font-size: 14px;'>Built with Python & Streamlit</p>", unsafe_allow_html=True)
st.divider()

api_key = st.sidebar.text_input("🔑 Enter your Groq API Key", type="password")
st.sidebar.markdown("[Get a free API key →](https://console.groq.com)", unsafe_allow_html=True)
st.sidebar.divider()
st.sidebar.markdown("About this project")
st.sidebar.markdown("An AI chatbot built with Python, Streamlit, and Groq AI.")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hey! I'm Aria ✦ — your AI assistant. Ask me anything, I'm here to help!"}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask Aria anything..."):
    if not api_key:
        st.error("⚠️ Please enter your Groq API key in the sidebar to continue.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Aria is thinking..."):
                try:
                    client = Groq(api_key=api_key)
                    history = [{"role": "system", "content": "You are Aria, a helpful and friendly AI assistant. Be concise, warm, and genuinely useful."}]
                    for m in st.session_state.messages:
                        history.append({"role": m["role"], "content": m["content"]})
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=history,
                        max_tokens=1000
                    )
                    reply = response.choices[0].message.content
                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                except Exception as e:
                    st.error(f"Error: {str(e)}")
