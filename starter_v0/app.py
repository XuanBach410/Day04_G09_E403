import streamlit as st
import json
from pathlib import Path
from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from chat import run_model_tool_loop, trim_history

# Setup paths and environment
ROOT = Path(__file__).parent
ARTIFACTS_DIR = ROOT / "artifacts"
load_lab_env(ROOT)

st.set_page_config(page_title="AI Research Agent V2", page_icon="🤖", layout="centered")

# Minimalist custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .stChatInputContainer {
        border-radius: 12px;
    }
    .tool-expander {
        font-family: monospace;
        font-size: 0.85em;
        background-color: #1E1E1E;
        padding: 10px;
        border-radius: 8px;
    }
    .status-text {
        color: #00FF00;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Version selector in sidebar
with st.sidebar:
    st.header("⚙️ Cấu hình Agent")
    selected_version = st.selectbox(
        "Chọn Version", 
        ["V3 (Phép thuật - Auto Fallback)", "V2 (Thiên tài - 100đ)", "V1 (Thông minh - 85đ)", "V0 (Ngốc nghếch - Gốc)"],
        index=0
    )
    
    # Map version to file
    if selected_version.startswith("V3"):
        prompt_file = "system_prompt_v3.md"
    elif selected_version.startswith("V2"):
        prompt_file = "system_prompt_v2.md"
    elif selected_version.startswith("V1"):
        prompt_file = "system_prompt_v1.md"
    else:
        prompt_file = "system_prompt_v0.md"
        
    current_prompt = (ARTIFACTS_DIR / prompt_file).read_text(encoding="utf-8")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = []
if "current_version" not in st.session_state:
    st.session_state.current_version = selected_version

# If version changed, update prompt and clear history
if st.session_state.current_version != selected_version:
    st.session_state.current_version = selected_version
    st.session_state.system_prompt = current_prompt
    st.session_state.messages = []
    st.session_state.history = []
    st.rerun()

if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = current_prompt

if "provider" not in st.session_state:
    st.session_state.provider = make_provider("openai")

if "tools" not in st.session_state:
    decls = load_tool_declarations(ARTIFACTS_DIR / "tools.yaml")
    st.session_state.tools = to_openai_tools(decls)

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "rounds" in msg:
            for r in msg["rounds"]:
                if r.get("tool_calls"):
                    with st.expander(f"🛠️ Đã dùng {len(r['tool_calls'])} công cụ"):
                        for call in r["tool_calls"]:
                            st.markdown(f"**`{call['name']}`**")
                            st.json(call["args"])
                        if r.get("tool_results"):
                            st.markdown("**Kết quả:**")
                            st.json(r["tool_results"])

# Handle user input
if prompt := st.chat_input("Hỏi gì đó đi (VD: Xem giá HPG gần đây, hoặc Tóm tắt tin AI)..."):
    # Append user msg to UI and history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Build context for the model
    context = [
        {"role": "system", "content": st.session_state.system_prompt},
        *trim_history(st.session_state.history, 5),
        {"role": "user", "content": prompt}
    ]

    # Show spinner while thinking
    with st.chat_message("assistant"):
        with st.spinner("Đang suy nghĩ và tra cứu..."):
            result = run_model_tool_loop(
                provider=st.session_state.provider,
                messages=context,
                tools=st.session_state.tools,
                model=st.session_state.provider.default_model,
                max_tool_rounds=4
            )

        assistant_text = result.get("assistant_text", "")
        rounds = result.get("rounds", [])
        
        # Display the result
        for r in rounds:
            if r.get("tool_calls"):
                with st.expander(f"🛠️ Đã dùng {len(r['tool_calls'])} công cụ"):
                    for call in r["tool_calls"]:
                        st.markdown(f"**`{call['name']}`**")
                        st.json(call["args"])
                    if r.get("tool_results"):
                        st.markdown("**Kết quả:**")
                        st.json(r["tool_results"])
                        
        if assistant_text:
            st.markdown(assistant_text)
            
        # Add to state
        st.session_state.messages.append({
            "role": "assistant", 
            "content": assistant_text,
            "rounds": rounds
        })
        st.session_state.history.append({"role": "user", "content": prompt})
        st.session_state.history.append({"role": "assistant", "content": assistant_text})
