# Optimization 1: Minimize unnecessary imports

import plotly.express as px
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.sentiment import SentimentIntensityAnalyzer
from bs4 import BeautifulSoup
import requests
```python
```

# Optimization 2: Remove unnecessary class

```python


class Product:
    def __init__(self, title, reviews, ratings, price):
        self.title = title
        self.reviews = reviews
        self.ratings = ratings
        self.price = price


```

# Optimization 3: Remove unnecessary function parameters

```python


def process_data(reviews):
    cleaned_reviews = list(set(reviews))
    return cleaned_reviews


```

# Optimization 4: Use list comprehension for sentiment analysis

```python


def perform_sentiment_analysis(cleaned_reviews):
    sentiment_scores = [SentimentIntensityAnalyzer().polarity_scores(
        review)['compound'] for review in cleaned_reviews]
    return sentiment_scores


```

# Optimization 5: Simplify recommendation engine function

```python


def build_recommendation_engine(cleaned_reviews):
    cv = CountVectorizer()
    review_matrix = cv.fit_transform(cleaned_reviews)
    return cosine_similarity(review_matrix)


```

# Optimization 6: Simplify get_recommendations function

```python


def get_recommendations(product_data, similarity_matrix):
    product_index = [title.lower() for title in product_titles].index(
        product_data.title.lower())
    similar_products = sorted(list(enumerate(
        similarity_matrix[product_index])), key=lambda x: x[1], reverse=True)[:5]
    return [(product_titles[product[0]], product[1]) for product in similar_products]


```

# Optimization 7: Remove unnecessary user preferences function

```python


def get_user_preferences():
    return input("Enter your preferences or search criteria: ")


```

# Optimization 8: Use f-string for display_recommendations function

```python


def display_recommendations(recommendations):
    print("Recommended Products:")
    for product, similarity_score in recommendations:
        print(f"- {product} (Similarity Score: {similarity_score})")


```

# Optimization 9: Simplify update_data function

```python


def update_data(url, similarity_matrix):
    new_data = scrape_product_data(url)
    processed_data = process_data(new_data.reviews)
    sentiment_scores = perform_sentiment_analysis(processed_data)
    similarity_matrix = build_recommendation_engine(processed_data)
    return new_data, sentiment_scores, similarity_matrix


```

# Optimization 10: Simplify plot functions

```python


def visualize_sentiment_distribution(sentiment_scores):
    plt.hist(sentiment_scores, bins=10)
    plt.xlabel('Sentiment Score')
    plt.ylabel('Count')
    plt.title('Sentiment Distribution')
    plt.show()


def visualize_product_ratings(ratings):
    fig = px.bar(x=product_titles, y=ratings, labels={
                 'x': 'Products', 'y': 'Ratings'})
    fig.show()


```

# Optimization 11: Rename cleaned_data to cleaned_reviews

```python
cleaned_reviews = process_data(product_data.reviews)
sentiment_scores = perform_sentiment_analysis(cleaned_reviews)
similarity_matrix = build_recommendation_engine(cleaned_reviews)
product_titles = [product_data.title]

recommendations = get_recommendations(product_data, similarity_matrix)
display_recommendations(recommendations)

while True:
    choice = input("Do you want to update the data? (y/n): ")
    if choice.lower() == 'y':
        product_data, sentiment_scores, similarity_matrix = update_data(
            url, similarity_matrix)
        cleaned_reviews = process_data(product_data.reviews)
        sentiment_scores = perform_sentiment_analysis(cleaned_reviews)
        similarity_matrix = build_recommendation_engine(cleaned_reviews)
        recommendations = get_recommendations(product_data, similarity_matrix)
        display_recommendations(recommendations)
    else:
        break

visualize_sentiment_distribution(sentiment_scores)
visualize_product_ratings(product_data.ratings)
export_recommendations(recommendations)
```
