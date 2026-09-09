import feedparser
from sentiment import analyze_sentiment
from db_manager import save_sentiment_data

def fetch_and_process_reddit_rss(subreddit="CryptoCurrency", limit=5):
    # Reddit RSS besleme adresi
    url = f"https://www.reddit.com/r/{subreddit}/new/.rss"
    
    # RSS verisini çekip ayrıştırıyoruz
    feed = feedparser.parse(url)
    
    if feed.entries:
        for entry in feed.entries[:limit]:
            title = entry.title
            
            # Duygu analizi yap
            result = analyze_sentiment(title)
            
            print(f"Başlık: {result['text']}")
            print(f"Skor: {result['compound']} | Etiket: {result['sentiment']}\n")
            
            save_sentiment_data(
                source="Reddit_Crypto",
                text=result['text'],
                compound_score=result['compound'],
                sentiment_label=result['sentiment']
            )
    else:
        print("Veri çekilemedi veya akış boş.")

if __name__ == "__main__":
    fetch_and_process_reddit_rss()