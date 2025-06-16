import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Load API key from environment variable
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def analyze_review(review_content):
    """
    Analyzes a single review using the OpenAI API.
    """
    prompt = f"""
    Analyze the following app store review and extract the following information:
    1.  condition_mentioned: The specific neurodivergent condition mentioned (e.g., "ADHD", "autism"). If none, this should be null.
    2.  sentiment: The sentiment of the review (positive, neutral, or negative).
    3.  assistive_function: A brief description of how the user uses the app as an assistive tool (e.g., "focus aid", "routine management").
    4.  key_issues: A brief summary of the main pain points or praise in the review.

    Return the output as a JSON object.

    Review: "{review_content}"
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": "You are an expert at analyzing app reviews."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def main():
    try:
        with open('reviews.json', 'r', encoding='utf-8') as f:
            reviews = json.load(f)
    except FileNotFoundError:
        print("Error: reviews.json not found.")
        return
    except json.JSONDecodeError:
        print("Error: Could not decode JSON from reviews.json.")
        return

    analyzed_reviews = []
    # First 5 reviews for test run
    for review in reviews[:5]:
        review_text = review.get('content')
        if review_text:
            analysis_result = analyze_review(review_text)
            if analysis_result:
                analyzed_reviews.append(analysis_result)

    with open('analyzed_reviews.json', 'w', encoding='utf-8') as f:
        json.dump(analyzed_reviews, f, indent=4)

    print("Analysis complete. Results saved to analyzed_reviews.json")

if __name__ == "__main__":
    main()
