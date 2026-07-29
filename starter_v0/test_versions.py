import json
from pathlib import Path
from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from chat import run_model_tool_loop

ROOT = Path(__file__).parent
ARTIFACTS_DIR = ROOT / "artifacts"
load_lab_env(ROOT)

provider = make_provider("openai")
decls = load_tool_declarations(ARTIFACTS_DIR / "tools.yaml")
openai_tools = to_openai_tools(decls)

prompt = "Hãy kiểm tra giá cổ phiếu HPG, đồng thời phân tích dòng tiền cá voi mã này."

for version in ["v0", "v1", "v3"]:
    system_prompt = (ARTIFACTS_DIR / f"system_prompt_{version}.md").read_text(encoding="utf-8")
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    
    print(f"\\n{'='*40}\\nTesting {version.upper()}\\n{'='*40}")
    
    allowed_tools = []
    if "v0" in version:
        allowed_tools = []
    elif "v1" in version:
        allowed_tools = [t for t in openai_tools if t["function"]["name"] != "market_flow"]
    else:
        allowed_tools = openai_tools

    result = run_model_tool_loop(
        provider=provider,
        messages=messages,
        tools=allowed_tools,
        model=provider.default_model,
        max_tool_rounds=4
    )
    
    print(f"Assistant Text: {result.get('assistant_text')}")
    for round_data in result.get("rounds", []):
        for tool_call in round_data.get("tool_calls", []):
            print(f"Tool called: {tool_call['name']}")
