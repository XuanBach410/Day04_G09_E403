with open("artifacts/tools.yaml", "a", encoding="utf-8") as f:
    f.write('''
  - name: market_flow
    description: "Phân tích dòng tiền cá voi (whale money flow) và thanh khoản thị trường cho một mã chứng khoán. Sử dụng để phát hiện dòng tiền lớn mua gom hoặc xả hàng."
    parameters:
      type: object
      properties:
        symbol:
          type: string
          description: "Mã chứng khoán (ví dụ: HPG, VIC)"
        days:
          type: integer
          description: "Số ngày phân tích (mặc định 30)"
        threshold_multiplier:
          type: number
          description: "Hệ số đột biến thanh khoản so với trung bình 20 phiên (mặc định 2.0)"
      required: [symbol]
''')
