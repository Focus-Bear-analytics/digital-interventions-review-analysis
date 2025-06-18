
# App Store Scraping

Scraping apps from Apple App Store, filtering for keywords


## Badges


[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)



## Usage/Examples

Scraping reviews for a particular a single app specified by appId.
Notes:
* can change number of characters displayed in review (currently set to 200)
* can change specifc app being scraped (through app_id input)
```python
import requests

def fetch_reviews(app_id, country='au'):
    url = f"https://itunes.apple.com/{country}/rss/customerreviews/id={app_id}/json"
    response = requests.get(url)
    if response.status_code != 200:
        print("No data or invalid app ID")
        return

    data = response.json()
    reviews = data.get('feed', {}).get('entry', [])[1:]  # Skip metadata
    for review in reviews:
        print(f"Title: {review['title']['label']}")
        print(f"Rating: {review['im:rating']['label']}")
        print(f"Content: {review['content']['label'][:200]}...\n")

# Example app - Tap 2 Distract
fetch_reviews(app_id='6447653942')

```
Output:
```
Title: Best App Ever
Rating: 5
Content: I might be a little biased, but this could be one of the best apps out there that provides anywhere, anytime distraction. The team have worked hard to make this a reality to assist kids with needle ph...

Title: Therapeutic
Rating: 5
Content: Just downloaded this app and couldn’t be happier! Wish I only had this sooner, definitely recommend to all 😊...

Title: This app has been so helpful
Rating: 5
Content: The best for blood tests and needles! Recommend!...
```
Scraping app descriptions based on keywords. Notes:
* Can change keyword list (add/remove for more specifc/broad search)
* Can change number of chars for description (currently set to 500)

```python
import requests

def search_app_store_by_keywords(keywords, country='au'):
    seen_app_ids = set()
    
    for keyword in keywords:
        print(f"Searching for: '{keyword}'")
        url = "https://itunes.apple.com/search"
        params = {
            'term': keyword,
            'country': country,
            'entity': 'software'
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"Error fetching results for '{keyword}' (status code: {response.status_code})")
            continue

        results = response.json().get('results', [])

        for app in results:
            app_id = app.get('trackId')
            if app_id in seen_app_ids:
                continue  # skip duplicates
            seen_app_ids.add(app_id)

            print(f"Name: {app.get('trackName')}")
            print(f"App ID: {app_id}")
            print(f"Description: {app.get('description', 'No description')[:500]}...")
            print(f"URL: {app.get('trackViewUrl')}")
            print("-" * 40)

# List of keywords
keywords = [
    "distraction", "addiction", "motivation", "self-control",
    "smartphone distraction", "smartphone addiction", "smartphone motivation", "smartphone self-control",
    "laptop distraction", "laptop addiction", "laptop motivation", "laptop self-control",
    "internet distraction", "internet addiction", "internet motivation", "internet self-control"
]

search_app_store_by_keywords(keywords)
```
Output:
```
Searching for: 'distraction'
Name: Tap 2 Distract
App ID: 6447653942
Description: Tap 2 Distract uses the tool of distraction to encourage play for children during stressful or uncomfortable situations. Designed to give children a sense of control by using positive engagement, Tap 2 Distract is all about having access to anytime, anywhere distraction. 

When a child feels traumatised, uncertain or vulnerable, it is essential to reassure them and their families that through proven distraction techniques, anxiety filed situations can become less of a challenge and more of an ac...
URL: https://apps.apple.com/au/app/tap-2-distract/id6447653942?uo=4
----------------------------------------
Name: Baby Bubbles Babble
App ID: 842788895
Description: When my daughter was about one year old, she loved  bubble popping games. Unfortunately, most of them are insanely expensive, have annoying ads that she accidentally activates, or have complicated setting screens that she gets trapped in.

So, as a first birthday present for her, I developed Baby Bubbles Free. The first 100% free bubble popping game for babies and toddlers that also has NO ADS and NO INTERFACE. Just plain, simple, happy bubble popping fun.

Besides being free, ad free, and havin...
URL: https://apps.apple.com/au/app/baby-bubbles-babble/id842788895?uo=4
----------------------------------------
...
```
## Improvements

Improvements for increasing number of apps scraped:
* Consider modifying scraping algorithm to scrape apps from the 'You Might Also Like' section when an app is found by a particular keyword 
* Explore 'appium' for more robust scraping

## Notes:
* Python app store scraper does not work (py_google_play_instruction.md)
* Scraping from actual Apple App Store gave null data (may be result of Apple's privacy laws etc)   



