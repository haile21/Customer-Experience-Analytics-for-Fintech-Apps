import os

import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()

class PostgresDB:
    def __init__(self):
        self.conn = psycopg2.connect(
            user=os.getenv("PG_USER"),
            password=os.getenv("PG_PASSWORD"),
            host=os.getenv("PG_HOST"),
            port=os.getenv("PG_PORT"),
            dbname=os.getenv("PG_DATABASE")
        )

    def create_tables(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS banks (
                    bank_id SERIAL PRIMARY KEY,
                    bank_name VARCHAR(100) NOT NULL UNIQUE
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reviews (
                    review_id SERIAL PRIMARY KEY,
                    bank_id INTEGER REFERENCES banks(bank_id),
                    review_text TEXT,
                    rating INTEGER,
                    review_date DATE,
                    sentiment_score REAL,
                    sentiment_label VARCHAR(20),
                    keywords TEXT
                )
            """)

        self.conn.commit()

    def insert_data(self, df: pd.DataFrame):
        with self.conn.cursor() as cursor:
            bank_ids = {}

            for bank in df['bank'].unique():
                try:
                    cursor.execute(
                        "INSERT INTO banks (bank_name) VALUES (%s) RETURNING bank_id",
                        [bank]
                    )
                    bank_ids[bank] = cursor.fetchone()[0]
                except psycopg2.IntegrityError:
                    self.conn.rollback()
                    cursor.execute("SELECT bank_id FROM banks WHERE bank_name = %s", [bank])
                    bank_ids[bank] = cursor.fetchone()[0]

            for _, row in df.iterrows():
                cursor.execute(
                    """
                    INSERT INTO reviews (
                        bank_id, review_text, rating, review_date,
                        sentiment_score, sentiment_label, keywords
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    [
                        bank_ids[row['bank']],
                        row['review'],
                        row['rating'],
                        row['date'],
                        row['sentiment_score'],
                        row['sentiment_label'],
                        ', '.join(row['keywords']) if isinstance(row['keywords'], list) else row['keywords']
                    ]
                )

            self.conn.commit()

    def close(self):
        self.conn.close()
