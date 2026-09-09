import yfinance as yf
from db_manager import save_market_data

def fetch_and_save_stock_data(symbol="ETH-USD"):
    """Belirtilen sembolün güncel fiyat verisini çeker ve veritabanına kaydeder."""
    print(f"🔄 {symbol} verisi çekiliyor...")
    ticker = yf.Ticker(symbol)
    df = ticker.history(period="1d", interval="1m")

    if not df.empty:
        latest = df.tail(1)  # sadece en güncel dakikalık veri
        save_market_data(latest, symbol)
    else:
        print(f"⚠️ {symbol} için veri bulunamadı.")

def fetch_and_save_all(symbols=None):
    if symbols is None:
        symbols = ["ETH-USD", "BTC-USD", "NVDA"]
    for symbol in symbols:
        fetch_and_save_stock_data(symbol)

if __name__ == "__main__":
    fetch_and_save_all()