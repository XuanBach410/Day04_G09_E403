import traceback
from vnstock.api.quote import Quote

try:
    print("Testing VIC with vci...")
    df = Quote('VIC', 'vci').history(start='2024-01-01', end='2024-12-31')
    print(df.tail())
except Exception as e:
    traceback.print_exc()

try:
    print("\nTesting VIC with msn...")
    df = Quote('VIC', 'msn').history(start='2024-01-01', end='2024-12-31')
    print(df.tail())
except Exception as e:
    traceback.print_exc()
