import os
import psycopg2
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    """Veritabanı bağlantısı oluşturur."""
    return psycopg2.connect(DATABASE_URL)

def create_tables():
    """Gerekli tabloları veritabanında oluşturur."""
    commands = (
        """
        CREATE TABLE IF NOT EXISTS market_data (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMPTZ NOT NULL,
            symbol VARCHAR(10) NOT NULL,
            price NUMERIC NOT NULL,
            volume NUMERIC NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS sentiment_data (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMPTZ NOT NULL,
            source VARCHAR(20) NOT NULL,
            text TEXT NOT NULL,
            compound_score NUMERIC NOT NULL,
            sentiment_label VARCHAR(10) NOT NULL
        )
        """
    )
    
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        for command in commands:
            cur.execute(command)
            
        cur.close()
        conn.commit()
        print("✅ Tablolar başarıyla oluşturuldu/kontrol edildi!")
    except Exception as e:
        print(f"❌ Veritabanı hatası: {e}")
    finally:
        if conn is not None:
            conn.close()

def save_market_data(df, symbol):
    """Pandas DataFrame içindeki piyasa verilerini PostgreSQL'e kaydeder."""
    try:
        engine = create_engine(DATABASE_URL)
        
        df_to_save = df.reset_index()
        df_to_save['symbol'] = symbol
        
        df_to_save = df_to_save.rename(columns={
            'Datetime': 'timestamp',
            'Date': 'timestamp',
            'Close': 'price',
            'Volume': 'volume'
        })
        
        df_to_save = df_to_save[['timestamp', 'symbol', 'price', 'volume']]
        
        df_to_save.to_sql('market_data', engine, if_exists='append', index=False)
        print(f"✅ {len(df_to_save)} adet {symbol} verisi veritabanına kaydedildi!")
        
    except Exception as e:
        print(f"❌ Veri kaydetme hatası: {e}")
def save_sentiment_data(source, text, compound_score, sentiment_label):
    conn = get_connection()
    if conn is None:
        return
    
    try:
        cur = conn.cursor()
        
        # 1. Kontrol: Bu metin zaten kaydedilmiş mi?
        check_query = "SELECT COUNT(*) FROM sentiment_data WHERE text = %s;"
        cur.execute(check_query, (text,))
        exists = cur.fetchone()[0]
        
        if exists > 0:
            # Zaten varsa kaydetmeden çıkıyoruz
            cur.close()
            conn.close()
            return

        # 2. Kayıt: Eğer yoksa yeni veriyi ekliyoruz
        insert_query = """
    INSERT INTO sentiment_data (timestamp, source, text, compound_score, sentiment_label)
    VALUES (NOW(), %s, %s, %s, %s);
        """
        cur.execute(insert_query, (source, text, compound_score, sentiment_label))
        conn.commit()
        print(f"✅ Yeni sentiment verisi kaydedildi ({sentiment_label}): {text[:30]}...")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Veri kaydetme hatası: {e}")

def update_schema():
    conn = get_connection()
    if conn is None:
        return
    
    try:
        cur = conn.cursor()
        # source sütun genişliğini 20'den 100'e çıkarıyoruz
        alter_query = "ALTER TABLE sentiment_data ALTER COLUMN source TYPE VARCHAR(100);"
        cur.execute(alter_query)
        conn.commit()
        print("✅ Tablo şeması güncellendi: 'source' sütun boyutu 100 olarak ayarlandı!")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Şema güncelleme hatası: {e}")
if __name__ == "__main__":
    create_tables()
    update_schema()