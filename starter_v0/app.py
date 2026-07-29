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

st.set_page_config(page_title="AI Research Agent - Đấu Trường", page_icon="🤖", layout="wide")

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

st.title("🤖 Đấu Trường AI: So sánh đa phiên bản")
st.caption("Gõ 1 lệnh duy nhất ở dưới cùng để 3 Agent cùng xử lý và so sánh kết quả.")

if "provider" not in st.session_state:
    st.session_state.provider = make_provider("openai")

if "tools" not in st.session_state:
    decls = load_tool_declarations(ARTIFACTS_DIR / "tools.yaml")
    st.session_state.tools = to_openai_tools(decls)

VERSIONS = ["V3 (Phép thuật - Auto Fallback)", "V2 (Thiên tài - 100đ)", "V1 (Thông minh - 85đ)", "V0 (Ngốc nghếch - Gốc)"]

def get_prompt_text(version_name: str) -> str:
    if version_name.startswith("V3"):
        return (ARTIFACTS_DIR / "system_prompt_v3.md").read_text(encoding="utf-8")
    elif version_name.startswith("V2"):
        return (ARTIFACTS_DIR / "system_prompt_v2.md").read_text(encoding="utf-8")
    elif version_name.startswith("V1"):
        return (ARTIFACTS_DIR / "system_prompt_v1.md").read_text(encoding="utf-8")
    else:
        return (ARTIFACTS_DIR / "system_prompt_v0.md").read_text(encoding="utf-8")

# Initialize columns state
if "cols_data" not in st.session_state:
    st.session_state.cols_data = [
        {"id": 1, "version": VERSIONS[0], "messages": [], "history": []},
        {"id": 2, "version": VERSIONS[1], "messages": [], "history": []},
        {"id": 3, "version": VERSIONS[2], "messages": [], "history": []}
    ]

# Layout: 3 columns
cols = st.columns(3)
msg_containers = []

# Render selectbox and messages for each column
for i, col in enumerate(cols):
    col_data = st.session_state.cols_data[i]
    with col:
        st.subheader(f"Màn hình {i+1}")
        
        # Selectbox to change version
        new_version = st.selectbox(
            "Chọn Version", 
            VERSIONS, 
            index=VERSIONS.index(col_data["version"]),
            key=f"sb_{i}",
            label_visibility="collapsed"
        )
        
        # If version changed, clear history
        if new_version != col_data["version"]:
            col_data["version"] = new_version
            col_data["messages"] = []
            col_data["history"] = []
            st.rerun()
            
        # Create a container for messages to allow scrolling
        msg_container = st.container(height=650)
        msg_containers.append(msg_container)
        
        with msg_container:
            for msg in col_data["messages"]:
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

# Handle user input globally
if prompt := st.chat_input("Gõ 1 lệnh để cả 3 màn hình cùng xử lý (VD: Hãy phân tích dòng tiền HPG)..."):
    # Append user msg to all columns
    for col_data in st.session_state.cols_data:
        col_data["messages"].append({"role": "user", "content": prompt})
    
    st.rerun()

# Processing Phase (Sequential generation for columns)
for i, col in enumerate(cols):
    col_data = st.session_state.cols_data[i]
    if col_data["messages"] and col_data["messages"][-1]["role"] == "user":
        prompt = col_data["messages"][-1]["content"]
        with msg_containers[i]:
            with st.chat_message("assistant"):
                with st.spinner(f"Agent đang xử lý ({col_data['version'][:2]})..."):
                    # Build context
                    system_prompt = get_prompt_text(col_data["version"])
                    context = [
                        {"role": "system", "content": system_prompt},
                        *trim_history(col_data["history"], 5),
                        {"role": "user", "content": prompt}
                    ]
                    
                    # Lọc tool cứng dựa trên Version
                    allowed_tools = []
                    if "V0" in col_data["version"]:
                        allowed_tools = [] # V0 cấm xài tool
                    elif "V1" in col_data["version"]:
                        allowed_tools = [t for t in st.session_state.tools if t["function"]["name"] != "market_flow"]
                    else:
                        allowed_tools = st.session_state.tools
                        
                    result = run_model_tool_loop(
                        provider=st.session_state.provider,
                        messages=context,
                        tools=allowed_tools,
                        model=st.session_state.provider.default_model,
                        max_tool_rounds=4
                    )

                assistant_text = result.get("assistant_text", "")
                rounds = result.get("rounds", [])
                
                # Display the result briefly before rerun pushes it to main loop
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
                    
                # Save to state
                col_data["messages"].append({
                    "role": "assistant", 
                    "content": assistant_text,
                    "rounds": rounds
                })
                col_data["history"].append({"role": "user", "content": prompt})
                col_data["history"].append({"role": "assistant", "content": assistant_text})
                
        # Rerun to process the next column (or finish)
        st.rerun()
