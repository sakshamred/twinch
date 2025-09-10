import snscrape.modules.twitter as sntwitter
import requests
from PIL import Image
import easyocr
#import pytesseract if easyocr doesnt work sometime it breaks and not compatible with similar python versions :) 
reader = easyocr.Reader(['en'], gpu=False)

for tweet in sntwitter.TwitterSearchScraper('filter:images keyword_here').get_items():
    if tweet.media:
        for m in tweet.media:
            if hasattr(m, 'fullUrl'):
                img_url = m.fullUrl
                img_data = requests.get(img_url).content
                img = Image.open(BytesIO(img_data))
                ocr = reader.readtext(img)
                text = " ".join([t[1] for t in ocr]).lower()
                if 'your_search_term' in text:
                    print(tweet.url, text)

