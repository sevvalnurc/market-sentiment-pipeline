import feedparser
from sentiment import analyze_sentiment
from db_manager import save_sentiment_data

# Güvenilir Finans & Kripto Haber RSS Kaynakları
RSS_FEEDS = {
    "CoinDesk": "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "CoinTelegraph": "https://cointelegraph.com/rss",
    "CryptoSlate": "https://cryptoslate.com/feed/"
}

def fetch_and_process_news_rss(limit=5):
    print("📡 Finans & Haber RSS Akışı Başlatılıyor...")
    
    for source_name, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)
        
        if feed.entries:
            print(f"\n--- {source_name} Kaynağından Veri Çekiliyor ---")
            for entry in feed.entries[:limit]:
                title = entry.title
                
                # Duygu analizi yap
                result = analyze_sentiment(title)
                
                print(f"Başlık: {result['text']}")
                print(f"Skor: {result['compound']} | Etiket: {result['sentiment']}")
                
                # Veritabanına kaydet (Sütun boyutumuz 100 olduğu için rahatça kaydediyoruz)
                save_sentiment_data(
                    source=f"News/{source_name}",
                    text=result['text'],
                    compound_score=result['compound'],
                    sentiment_label=result['sentiment']
                )
        else:
            print(f"⚠️ {source_name} kaynağından veri çekilemedi.")

if __name__ == "__main__":
    fetch_and_process_news_rss()