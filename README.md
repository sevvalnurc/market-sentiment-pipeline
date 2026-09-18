# 📊 Market Sentiment Pipeline

Kripto para birimlerine (Bitcoin, Ethereum) yönelik sosyal medya ve haber duygu durumunun 
(sentiment) fiyat hareketleriyle ilişkisini test etmek amacıyla geliştirilmiş, uçtan uca 
otomatik bir veri toplama ve istatistiksel analiz projesi.

## 🎯 Araştırma Sorusu ve Hipotezler

**Araştırma sorusu:** Kripto piyasasında sosyal medya/haber sentiment'i, fiyat hareketlerini 
önceden haber veren bir gösterge olarak işlev görür mü?

Bu soru iki ayrı istatistiksel test ile operasyonelleştirilmiştir:

**Test 1 — Coin türüne göre sentiment farkı (Tek Yönlü ANOVA)**
- H0: Bitcoin, Ethereum ve genel kripto içeriklerine yönelik ortalama sentiment skorları 
  arasında fark yoktur (μ_BTC = μ_ETH = μ_Diğer).
- H1: En az bir grubun ortalama sentiment skoru diğerlerinden farklıdır.
- Anlamlılık düzeyi: α = 0.05

**Test 2 — Sentiment ile fiyat arasındaki gecikmeli ilişki (Pearson Korelasyonu)**
- H0: Sentiment skoru ile t, t+1, t+2, t+3 saat sonraki fiyat arasında doğrusal bir ilişki 
  yoktur (r = 0).
- H1: Sentiment skoru ile ilgili gecikmede fiyat arasında doğrusal bir ilişki vardır (r ≠ 0).
- Anlamlılık düzeyi: α = 0.05

## 🏗️ Mimari
```
Reddit RSS ─┐
            ├─→ VADER Sentiment Analizi ─→ PostgreSQL (Render) ─→ Jupyter Notebook (Analiz)
Haber RSS ──┘                                       ↑
                                                    │
yfinance (BTC/ETH fiyatları) ───────────────────────┘

GitHub Actions (her 15 dakikada bir tetikleme) → Pipeline'ı bulutta otomatik çalıştırır
```
**Veri akışı:**
1. Reddit (`r/CryptoCurrency`) ve finans haber siteleri (CoinDesk, CoinTelegraph, CryptoSlate) 
   RSS akışlarından başlıklar çekilir.
2. Her başlık VADER (Valence Aware Dictionary and sEntiment Reasoner) ile duygu skoruna 
   dönüştürülür.
3. Eşzamanlı olarak `yfinance` üzerinden BTC-USD ve ETH-USD fiyat verileri çekilir.
4. Tüm veriler PostgreSQL (Render) veritabanına kaydedilir.
5. GitHub Actions, bu süreci sunucu bağımsız şekilde her 15 dakikada bir otomatik tetikler.
6. Toplanan veri Jupyter Notebook'ta temizlenir, keşfedilir ve istatistiksel olarak test edilir.

## 🛠️ Kullanılan Teknolojiler

- **Python** — pandas, numpy, scipy
- **VADER Sentiment** — duygu analizi
- **yfinance** — kripto fiyat verisi
- **PostgreSQL** (Render) — veri depolama
- **SQLAlchemy / psycopg2** — veritabanı bağlantısı
- **feedparser** — RSS okuma
- **GitHub Actions** — otomatik, zamanlanmış veri toplama
- **matplotlib / seaborn** — görselleştirme
- **Jupyter Notebook** — analiz ortamı

## 📁 Proje Yapısı
```
├── src/
│   ├── fetch_reddit.py      # Reddit RSS'ten veri çeker
│   ├── fetch_news_rss.py    # Haber sitelerinden veri çeker
│   ├── fetch_data.py        # Fiyat verisi çeker (yfinance)
│   ├── sentiment.py         # VADER ile duygu analizi
│   ├── db_manager.py        # PostgreSQL bağlantı/kayıt işlemleri
│   ├── main.py              # Yerel/sürekli çalışan pipeline (geliştirme amaçlı)
│   ├── run_once.py          # GitHub Actions için tek seferlik çalışan versiyon
│   └── check_db_connection.py     # Veritabanı bağlantı testi (sadece geliştirme amaçlı)
├── notebooks/
│   ├── eda.ipynb                       # Veri temizleme, analiz ve hipotez testi
│   └── sentiment_price_timeline.png    # Analiz sonucu üretilen görsel
├── .github/workflows/
│   └── pipeline.yml           # Otomatik veri toplama (her 15 dakikada bir)
├── requirements.txt
└── README.md
```

## 🧹 Veri Hazırlama

Ham veri üzerinde üç temizleme adımı uygulanmıştır:
1. **Mükerrer kayıtlar** (`text` alanına göre) çıkarılmıştır.
2. Geliştirme sürecinde `sentiment.py` fonksiyonunu test etmek amacıyla üretilen 3 adet 
   sentetik örnek cümle, gerçek veriyle karışmış olarak tespit edilmiş ve veri setinden 
   çıkarılmıştır.
3. Fiyat verisinde bağlantı testine ait `TEST` sembolüne sahip 2 kayıt çıkarılmıştır.

Temizleme sonrası: **611 sentiment kaydı**, **317 fiyat kaydı**.

## 🔬 Varsayım Kontrolleri

ANOVA testinin uygulanabilirliği için varsayımlar kontrol edilmiştir:

- **Normallik (Shapiro-Wilk):** Bitcoin (p=0.0002) ve Diğer/Genel Crypto (p<0.0001) 
  gruplarında normallik varsayımı ihlal edilmiştir; Ethereum (p=0.204) bu varsayımı 
  karşılamaktadır. Sentiment skorlarının sıfırda (nötr) yoğunlaşması bu ihlalin olası 
  nedenidir.
- **Varyans Homojenliği (Levene):** p=0.198 ile varyanslar homojen bulunmuş, bu varsayım 
  karşılanmıştır.

Normallik ihlaline rağmen, örneklem büyüklüğünün yeterince büyük olması (n=611, en küçük 
grup n=39) nedeniyle Merkezi Limit Teoremi gereği ANOVA'nın bu ihlale karşı büyük ölçüde 
sağlam (robust) kaldığı kabul edilmiştir. Bulgular yine de bu sınırlama göz önünde 
bulundurularak yorumlanmalıdır.

## 📈 Bulgular

![Sentiment ve Fiyat Zaman Serisi](notebooks/sentiment_price_timeline.png)

**Test 1 sonucu — Coin bazında sentiment farkı:**  
F(2, 608) = 4.65, p = 0.0099 → **p < α, H0 reddedilmiştir.**  
Coin türüne göre sentiment skorları arasında istatistiksel olarak anlamlı bir fark 
bulunmuştur. Bitcoin'e yönelik içerikler (ortalama -0.063), Ethereum (+0.009) ve genel 
kripto içeriklerine (+0.038) kıyasla görece daha negatif seyretmiştir. ANOVA yalnızca 
gruplar arasında en az bir farkın varlığını gösterir; hangi ikili grup(lar) arasında 
anlamlı fark olduğunu belirlemek için bu çalışmada post-hoc test uygulanmamıştır.

**Test 2 sonucu — Sentiment-fiyat gecikmeli ilişkisi:**  
Sentiment ve fiyatın saatlik olarak örtüştüğü, 10-17 Eylül 2026 tarihlerini kapsayan 
pencerede BTC için 39, ETH için 20 saatlik eşleşen gözlem üzerinden 0-3 saatlik gecikmelerle 
test yapılmıştır. Tüm gecikmelerde p > α bulunmuştur (BTC: p = 0.30-0.80; ETH: p = 0.21-0.72) 
→ **H0 reddedilememiştir.** Bu örneklemde sentiment ile fiyat arasında istatistiksel olarak 
anlamlı bir doğrusal ilişki tespit edilememiştir.

*Not: Bu test toplam 8 kez (2 coin × 4 gecikme) tekrarlanmıştır; çoklu karşılaştırma 
düzeltmesi (örn. Bonferroni) uygulanmamıştır. Hiçbir sonuç anlamlı çıkmadığı için bu durum 
mevcut bulguyu değiştirmemekle birlikte, metodolojik bir sınırlama olarak belirtilmelidir.*

## ⚠️ Sınırlamalar

- Örneklem büyüklüğü (özellikle saatlik eşleşen veri: ETH için n=20) ve gözlem periyodu 
  (1 hafta) sınırlıdır; bulgular genellenebilir değildir.
- ANOVA'nın normallik varsayımı iki grupta ihlal edilmiştir (bkz. Varsayım Kontrolleri).
- Sentiment kaynakları (Reddit, İngilizce haber siteleri) kripto topluluğunun sınırlı bir 
  kesimini temsil etmektedir.
- Korelasyon testlerinde çoklu karşılaştırma düzeltmesi uygulanmamıştır.
- GitHub Actions'ın ücretsiz katmanındaki zamanlama gecikmeleri, veri toplama sıklığını 
  zaman zaman etkilemiştir.

Bu proje bir **kanıt niteliğinde (proof of concept)** çalışmadır; daha uzun bir gözlem 
periyodu, daha büyük örneklem ve post-hoc/çoklu karşılaştırma düzeltmeleriyle sonuçların 
doğrulanması önerilir.

## 🚀 Kurulum ve Çalıştırma

```bash
git clone https://github.com/sevvalnurc/market-sentiment-pipeline.git
cd market-sentiment-pipeline
pip install -r requirements.txt
```

`.env` dosyası oluşturup kendi PostgreSQL bağlantı adresinizi ekleyin:
DATABASE_URL=postgresql://kullanici:sifre@host/veritabani


Pipeline'ı bir kez çalıştırmak için:
```bash
cd src
python run_once.py
```

Analizi incelemek için `notebooks/eda.ipynb`'yi Jupyter'de açın.

## 👤 Geliştiren

**Şevval Nur** — [@sevvalnurc](https://github.com/sevvalnurc)
