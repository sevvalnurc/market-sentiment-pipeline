from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from db_manager import save_sentiment_data

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text: str) -> dict:
    """
    Verilen metnin duygu skorlarını hesaplar.
    """
    scores = analyzer.polarity_scores(text)

    compound = scores['compound']
    if compound >= 0.05:
        sentiment_label = 'Positive'
    elif compound <= -0.05:
        sentiment_label = 'Negative'
    else:
        sentiment_label = 'Neutral'

    return {
        'text': text,
        'compound': compound,
        'sentiment': sentiment_label
    }

if __name__ == "__main__":
    # Not: Bu blok sadece fonksiyonu test etmek içindir, veritabanına yazmaz.
    sample_texts = [
        "Bitcoin is going to the moon! Best investment ever! 🚀",
        "Ethereum market crash is terrible, I lost all my money...",
        "Crypto market trading volume remained flat today."
    ]

    for text in sample_texts:
        result = analyze_sentiment(text)
        print(f"Metin: {result['text']}")
        print(f"Skor: {result['compound']} | Etiket: {result['sentiment']}\n")
