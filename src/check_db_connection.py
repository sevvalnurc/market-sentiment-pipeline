import pandas as pd
from db_manager import save_market_data

test_data = {
    'Datetime': [pd.Timestamp.now()],
    'Close': [2500.50],
    'Volume': [1500]
}
df_test = pd.DataFrame(test_data)

print("🧪 test edelim bakalım")
save_market_data(df_test, symbol="TEST")
