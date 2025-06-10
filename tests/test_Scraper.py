from src.scraper import scrape_bank
def test_scraper():
    df = scrape_bank(["com.cbe.mobile"], ["Test Bank"], review_count=1)
    #assert not df.empty