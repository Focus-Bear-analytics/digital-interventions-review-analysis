# Import the necessary modules
from app_store_scraper import AppStore
import pandas as pd
import numpy as np

# Initialize the AppStore object for Slack (US App Store)
app = AppStore(country='us', app_name='slack', app_id='618783545')

# Fetch reviews (2000 reviews in total)
app.review(how_many=2000)

# Convert reviews to a DataFrame
reviews_df = pd.DataFrame(np.array(app.reviews), columns=['review'])

# Expand the 'review' column into separate columns
reviews_df = reviews_df.join(pd.DataFrame(reviews_df.pop('review').tolist()))

# Display the first few reviews
print(reviews_df.head())
