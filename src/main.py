import time
import schedule
from fetch_reddit import fetch_and_process_reddit_rss
from fetch_news_rss import fetch_and_process_news_rss
from fetch_data import fetch_and_save_all

def run_pipeline():
    print("\n⏰ Pipeline başlatılıyor... (Canlı Veri Çekme)")
    
    # 1. Reddit verilerini çek ve kaydet
    try:
        fetch_and_process_reddit_rss(limit=5)
    except Exception as e:
        print(f"❌ Reddit çekiminde hata: {e}")
        
    # 2. Haber RSS verilerini çek ve kaydet
    try:
        fetch_and_process_news_rss(limit=5)
    except Exception as e:
        print(f"❌ Haber RSS çekiminde hata: {e}")

    # 3. Piyasa fiyat verilerini çek ve kaydet
    try:
        fetch_and_save_all()
    except Exception as e:
        print(f"❌ Piyasa verisi çekiminde hata: {e}")
        
    print("✅ Bu döngü tamamlandı. Bir sonraki çalışma bekleniyor...\n")

# Betik ilk çalıştığında hemen bir kere çalışsın
run_pipeline()

# Her 5 dakikada bir 'run_pipeline' fonksiyonunu çalıştır
schedule.every(5).minutes.do(run_pipeline)

print("🚀 Otomatik Sentiment Pipeline Çalışıyor! (Durdurmak için Ctrl+C)")

# Sonsuz döngü: Zamanlayıcıyı sürekli kontrol eder
while True:
    schedule.run_pending()
    time.sleep(1)