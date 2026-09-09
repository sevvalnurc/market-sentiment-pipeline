from fetch_reddit import fetch_and_process_reddit_rss
from fetch_news_rss import fetch_and_process_news_rss
from fetch_data import fetch_and_save_all

def run_pipeline():
    print("⏰ Pipeline (tek seferlik) başlatılıyor...")

    try:
        fetch_and_process_reddit_rss(limit=5)
    except Exception as e:
        print(f"❌ Reddit çekiminde hata: {e}")

    try:
        fetch_and_process_news_rss(limit=5)
    except Exception as e:
        print(f"❌ Haber RSS çekiminde hata: {e}")

    try:
        fetch_and_save_all()
    except Exception as e:
        print(f"❌ Piyasa verisi çekiminde hata: {e}")

    print("✅ Pipeline tamamlandı.")

if __name__ == "__main__":
    run_pipeline()
