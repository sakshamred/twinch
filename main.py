import snscrape.modules.twitter as sntwitter
import requests
import easyocr
from PIL import Image
from io import BytesIO
import json

# --- Setup ---
reader = easyocr.Reader(['en'], gpu=False)  # OCR in English, no GPU
results = []

# --- Step 1: Scrape tweets with images ---
def scrape_with_images(query, limit=20):
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query + " filter:images").get_items()):
        if i >= limit:  # stop after 'limit' tweets
            break
        if tweet.media:
            tweets.append(tweet)
    return tweets

# --- Step 2: Download image and run OCR ---
def extract_text_from_image(url):
    try:
        response = requests.get(url, timeout=10)
        img = Image.open(BytesIO(response.content))
        ocr = reader.readtext(img)
        return " ".join([t[1] for t in ocr])
    except Exception as e:
        return f"[OCR failed: {e}]"

# --- Step 3: Run pipeline ---
tweets = scrape_with_images("your keyword here", limit=10)

for tweet in tweets:
    for media in tweet.media:
        if hasattr(media, 'fullUrl'):
            text = extract_text_from_image(media.fullUrl)
            result = {
                "tweet_url": tweet.url,
                "ocr_text": text
            }
            results.append(result)

# --- Step 4: Save results ---
with open("tweets_ocr.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"✅ Done! Extracted OCR text from {len(results)} images.")
print("Results saved in tweets_ocr.json")

# --- Step 5: Search function ---
def search_in_results(keyword):
    matches = [r for r in results if keyword.lower() in r["ocr_text"].lower()]
    return matches

# Example search
hits = search_in_results("exam")
for h in hits:
    print("\nFound:", h["tweet_url"])
    print("Text:", h["ocr_text"])
