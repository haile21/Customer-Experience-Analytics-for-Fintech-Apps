from pathlib import Path
from datetime import datetime
from typing import List
import logging
import pandas as pd
from google_play_scraper import Sort, reviews

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
# google_play_scraper.reviews() only fetches up to 5000 in one call.
# If you need all reviews, you should loop with continuation_token
def fetch_all_reviews(app_id: str, lang: str = 'en', country: str = 'et',
                      sort: Sort = Sort.NEWEST, max_count: int = None) -> List[dict]:
    """
    Fetch all available reviews for a given app from Google Play.
    Supports pagination using continuation_token.
    """
    all_reviews, continuation_token = [], None
    while True:
        results, continuation_token = reviews(
            app_id,
            lang=lang,
            country=country,
            sort=sort,
            count=200,  # smaller batch to reduce API errors
            continuation_token=continuation_token
        )
        all_reviews.extend(results)

        if not continuation_token or (max_count and len(all_reviews) >= max_count):
            break

    return all_reviews[:max_count] if max_count else all_reviews


def scrape_bank(app_ids: List[str], app_names: List[str], review_count: int = 5000) -> pd.DataFrame:
    """
    Scrape reviews for multiple banking apps and return a cleaned DataFrame.
    Add review ID or user name if available to ensure uniqueness instead of relying only on (text, date, score).
    """
    all_reviews = []

    for app_id, bank_name in zip(app_ids, app_names):
        try:
            logging.info(f"Fetching reviews for {bank_name}...")
            results = fetch_all_reviews(app_id, max_count=review_count)

            seen = set()
            for r in results:
                text = r['content'].strip()
                date = r['at'].strftime('%Y-%m-%d')
                key = (r['reviewId'], r['userName'])  # ensures uniqueness
                if key not in seen:
                    seen.add(key)
                    all_reviews.append({
                        'review_id': r['reviewId'],
                        'user_name': r['userName'],
                        'review_text': text,
                        'rating': r['score'],
                        'date': date,
                        'bank_name': bank_name,
                        'source': 'Google Play'
                    })

        except Exception as ex:
            logging.error(f"Failed to fetch {bank_name}: {ex}")

    return pd.DataFrame(all_reviews)


def save_raw_data(df: pd.DataFrame, output_dir: str = 'data/raw'):
    """
    Save reviews to a timestamped CSV file with Windows-friendly path handling.
    Return early if no data. Helps prevent empty CSVs.
    """
    if df.empty:
        logging.warning("No reviews were scraped. Output file will not be created.")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(output_dir) / f'reviews_raw_{timestamp}.csv'
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    logging.info(f"Data saved to {output_path}")
