import json
from app_store_web_scraper import AppStoreEntry
from lingua import Language, LanguageDetectorBuilder

# Configuration
APP_ID = 866450515
COUNTRY = "us"
OUTPUT_FILE = "reviews.json"
REVIEW_LIMIT = 1000
KEYWORDS = ["adhd", "focus", "autism", "autistic"]


def main():
    try:
        app = AppStoreEntry(app_id=APP_ID, country=COUNTRY)
        # Setup language detector to use only english reviews
        detector = (
            LanguageDetectorBuilder.from_languages(Language.ENGLISH)
            .with_preloaded_language_models()
            .build()
        )

        reviews_list = []
        print(
            f"Fetching up to {REVIEW_LIMIT} reviews for app ID {APP_ID} from the {COUNTRY.upper()} App Store..."
        )

        # Fetch reviews with a limit
        for review in app.reviews(limit=REVIEW_LIMIT):
            # Language and keyword filtering
            if detector.detect_language_of(review.content) == Language.ENGLISH and any(
                keyword in review.content.lower() for keyword in KEYWORDS
            ):
                review_dict = {
                    "id": review.id,
                    "date": review.date.isoformat(),
                    "user_name": review.user_name,
                    "rating": review.rating,
                    "title": review.title,
                    "content": review.content,
                }
                reviews_list.append(review_dict)

        # Save the collected reviews to a JSON file
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(reviews_list, f, ensure_ascii=False, indent=4)

        print(f"Successfully scraped {len(reviews_list)} reviews.")
        print(f"Data saved to '{OUTPUT_FILE}'")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
