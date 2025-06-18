import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Load API key from environment variable
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def analyze_reviews_in_bulk(reviews):
    # Analyzes a batch of reviews using the OpenAI API.
    # Construct a single prompt with reviews
    reviews_text = "\n".join([f'- "{review["content"]}"' for review in reviews])

    prompt = f"""
    Analyze the following app store reviews and extract the specified information for each.
    Return the output as a JSON array, with each object in the array representing a single review's analysis.

    **Instructions:**
    - `condition_mentioned`: If a neurodivergent condition is mentioned, list it. Otherwise, this field must be `null`.
    - `key_issues`: Summarize key issues or praise. If none are explicitly mentioned, briefly state "No specific issues or praise mentioned."
    - `sentiment`: Categorize the sentiment as `positive`, `negative`, `neutral`, or `mixed`.
    - `assistive_function`: A brief description of how the user uses the app as an assistive tool (e.g., "focus aid", "routine management").
 
     Example of the desired JSON output structure for a single review:
     {{
       "condition_mentioned": "ADHD",
       "sentiment": "positive",
       "assistive_function": "Helps with focus and time management.",
       "key_issues": "The user loves the gamification aspect but wishes for more varied sounds."
     }}

    Reviews to analyze:
    {reviews_text}
    """

    try:
        response = client.chat.completions.create(
            model="o3-mini-2025-01-31",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert at analyzing app reviews and returning structured JSON.",
                },
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
        )
        # The model should return a JSON object with a key containing the list of reviews
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def main():
    try:
        with open("reviews.json", "r", encoding="utf-8") as f:
            reviews = json.load(f)
    except FileNotFoundError:
        print("Error: reviews.json not found.")
        return
    except json.JSONDecodeError:
        print("Error: Could not decode JSON from reviews.json.")
        return

    # Process reviews in chunks
    chunk_size = 10  # Process 10 reviews at a time
    all_results = []

    # Limit to the first 20 reviews for testing
    # reviews_to_process = reviews[:20]

    for i in range(0, len(reviews), chunk_size):
        batch = reviews[i : i + chunk_size]
        if not batch:
            continue

        print(f"Processing chunk {i // chunk_size + 1}...")
        analysis_results = analyze_reviews_in_bulk(batch)

        if analysis_results:
            results = analysis_results.get("reviews", [])
            all_results.extend(results)

    # Save all analyzed reviews to the file
    with open("analyzed_reviews.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=4)

    print(
        f"Analysis complete. {len(all_results)} reviews analyzed and saved to analyzed_reviews.json"
    )


if __name__ == "__main__":
    main()
