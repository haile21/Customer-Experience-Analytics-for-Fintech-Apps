from pathlib import Path  # Better path handling for Windows

import pandas as pd
from google_play_scraper import Sort, reviews


def scrape_bank(app_ids, app_names, review_count=5000):
    all_reviews = []

    for app_id, bank_name in zip(app_ids, app_names):
        try:
            print(f"Fetching {bank_name} reviews...")
            results, _ = reviews(app_id, lang='en', country='et',
                                 sort=Sort.NEWEST, count=5000)
            seen = set()
            for r in results:
                text = r['content'].strip()
                date = r['at'].strftime('%Y-%m-%d')
                key = (text, date, r['score'])
                if key not in seen:
                    seen.add(key)
                    all_reviews.append({
                        'review_text': text,
                        'rating': r['score'],
                        'date': date,
                        'bank_name': bank_name,
                        'source': 'Google Play'
                    })
        except Exception as ex:
            print(f"Failed to fetch {bank_name}: {ex}")

    return pd.DataFrame(all_reviews)

def save_raw_data(df: pd.DataFrame, output_dir: str = 'data/raw'):
    """Windows-friendly path handling"""
    output_path = Path(output_dir) / 'reviews_raw.csv'
    output_path.parent.mkdir(parents=True, exist_ok=True)  # Create dirs if missing
    df.to_csv(output_path, index=False, encoding='utf-8-sig')  # UTF-8 for Windows Excel
    print(f"Data saved to {output_path}")