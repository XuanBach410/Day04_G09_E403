import os
import sys
import json
from openai import OpenAI
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')


# Load API key từ file .env
load_dotenv()

# Khởi tạo OpenAI client (sẽ tự lấy OPENAI_API_KEY từ biến môi trường)
client = OpenAI()

# ==========================================
# 1. Định nghĩa Tool (Hàm Python thực thi)
# ==========================================
def get_stock_info(symbol: str) -> str:
    """
    Sử dụng vnstock3 để lấy dữ liệu chứng khoán.
    """
    print(f"\n[Tool Execution] Đang kéo dữ liệu thật cho mã {symbol} từ vnstock3...")
    try:
        from vnstock.api.quote import Quote
        # Khởi tạo đối tượng lấy dữ liệu chứng khoán từ vci
        stock = Quote(symbol=symbol.upper(), source='vci')
        
        # Lấy lịch sử giá (ví dụ lấy 10 ngày giao dịch gần nhất)
        df = stock.history(start='2024-01-01', end='2024-12-31') 
        
        # Lấy 5 dòng gần nhất để tránh context quá dài
        recent_data = df.tail(5) 
        
        print("[Tool Execution] Lấy dữ liệu thành công!")
        return recent_data.to_string()
    except Exception as e:
        print(f"\n[DEBUG] Lỗi thật sự bên trong là: {str(e)} ({type(e).__name__})")
        return f"Lỗi khi lấy dữ liệu: {str(e)}"

# ==========================================
# 2. Khai báo Tool Schema cho OpenAI biết
# ==========================================
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_stock_info",
            "description": "Lấy thông tin lịch sử giá của một mã cổ phiếu Việt Nam trong thời gian gần đây.",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Mã cổ phiếu trên sàn chứng khoán Việt Nam (VD: FPT, HPG, VCB)"
                    }
                },
                "required": ["symbol"]
            }
        }
    }
]

# ==========================================
# 3. Vòng lặp chính của Agent (Agent Loop)
# ==========================================
def run_agent(user_query: str):
    print(f"User: {user_query}")
    
    # Khởi tạo lịch sử chat
    messages = [
        {"role": "system", "content": "Bạn là chuyên gia chứng khoán Việt Nam. Hãy gọi tool get_stock_info để lấy dữ liệu trước khi trả lời. Trả lời ngắn gọn, súc tích."},
        {"role": "user", "content": user_query}
    ]
    
    # Bước 1: Gửi câu hỏi và công cụ cho AI
    response = client.chat.completions.create(
        model="gpt-4o-mini", # Hoặc gpt-3.5-turbo
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    
    ai_message = response.choices[0].message
    
    # Bước 2: Kiểm tra xem AI có muốn gọi Tool không
    if ai_message.tool_calls:
        for tool_call in ai_message.tool_calls:
            if tool_call.function.name == "get_stock_info":
                # Phân tích arguments mà AI truyền vào
                args = json.loads(tool_call.function.arguments)
                symbol = args.get("symbol", "")
                
                # Thực thi hàm thật
                tool_result = get_stock_info(symbol)
                
                # Bước 3: Gắn kết quả vào lịch sử và gửi lại cho AI
                messages.append(ai_message) # Lưu lại quyết định gọi tool
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_call.function.name,
                    "content": tool_result
                })
                
                # Báo AI tổng hợp kết quả
                final_response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages
                )
                print(f"\nAgent: {final_response.choices[0].message.content}")
    else:
        # Nếu AI tự trả lời luôn mà không gọi tool
        print(f"\nAgent: {ai_message.content}")

if __name__ == "__main__":
    # Test thử MVP
    query = "Xem giá HPG gần đây"
    run_agent(query)
