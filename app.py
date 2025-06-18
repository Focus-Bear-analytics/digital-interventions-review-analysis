import json
from flask import Flask, render_template, request

app = Flask(__name__)

def load_reviews():
    with open('analyzed_reviews.json', 'r') as f:
        return json.load(f)

@app.route('/')
def index():
    reviews = load_reviews()

    condition = request.args.get('condition')
    sentiment = request.args.get('sentiment')

    if condition:
        if condition == "__none__":
            reviews = [r for r in reviews if not r.get('condition_mentioned')]
        else:
            reviews = [r for r in reviews if r.get('condition_mentioned') and condition.lower() == r.get('condition_mentioned').lower()]
    
    if sentiment:
        reviews = [r for r in reviews if r.get('sentiment') and r.get('sentiment').lower() == sentiment.lower()]

    # Get unique conditions for the filter dropdown
    all_conditions = sorted(list(set(r['condition_mentioned'] for r in load_reviews() if r.get('condition_mentioned'))))

    return render_template('index.html', reviews=reviews, all_conditions=all_conditions, selected_condition=condition, selected_sentiment=sentiment)

if __name__ == '__main__':
    app.run(debug=True)
