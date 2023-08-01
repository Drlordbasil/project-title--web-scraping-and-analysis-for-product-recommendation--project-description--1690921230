import requests
from bs4 import BeautifulSoup
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import plotly.express as px


class Product:
    """
    Represents a product with title, reviews, ratings, and price
    """

    def __init__(self, title, reviews, ratings, price):
        self.title = title
        self.reviews = reviews
        self.ratings = ratings
        self.price = price


def scrape_product_data(url):
    """
    Scrapes the product data from a given URL and returns a Product object
    """

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    product_title = soup.find('h1').text.strip()
    reviews = soup.find_all(class_='review')
    user_reviews = [review.find(class_='text').text.strip() for review in reviews]
    ratings = [float(review.find(class_='rating').text.strip()) for review in reviews]
    price = float(soup.find(class_='price').text.strip('$'))
    return Product(product_title, user_reviews, ratings, price)


def process_data(reviews, ratings):
    """
    Processes the user reviews by cleaning and removing duplicates
    Returns cleaned reviews and ratings
    """

    cleaned_reviews = list(set(reviews))  # Removing duplicate reviews
    return cleaned_reviews, ratings


def perform_sentiment_analysis(cleaned_reviews):
    """
    Performs sentiment analysis on the cleaned reviews
    Returns a list of sentiment scores
    """

    sentiment_scores = []
    sia = SentimentIntensityAnalyzer()
    for review in cleaned_reviews:
        sentiment_scores.append(sia.polarity_scores(review)['compound'])
    return sentiment_scores


def build_recommendation_engine(cleaned_reviews):
    """
    Builds a recommendation engine using cleaned reviews
    Returns the similarity matrix
    """

    cv = CountVectorizer()
    review_matrix = cv.fit_transform(cleaned_reviews)
    similarity_matrix = cosine_similarity(review_matrix)
    return similarity_matrix


def get_recommendations(product_data, similarity_matrix, product_titles):
    """
    Gets the top 5 most similar products based on the similarity matrix
    Returns a list of recommended products
    """

    product_index = [title.lower() for title in product_titles].index(product_data.title.lower())
    similar_products = sorted(list(enumerate(similarity_matrix[product_index])), key=lambda x: x[1], reverse=True)[
                      :5]
    recommendations = [(product_titles[product[0]], product[1]) for product in similar_products]
    return recommendations


def get_user_preferences():
    """
    Gets user preferences or search criteria
    Returns user preferences as a string
    """

    preferences = input("Enter your preferences or search criteria: ")
    return preferences


def display_recommendations(recommendations):
    """
    Displays the list of recommended products
    """

    print("Recommended Products:")
    for product in recommendations:
        print(f"- {product[0]} (Similarity Score: {product[1]})")


def update_data(url, similarity_matrix, product_titles):
    """
    Updates the data by rescraping the web sources, processing data, and updating the similarity matrix
    Returns the updated product data, sentiment scores, and similarity matrix
    """

    new_data = scrape_product_data(url)
    processed_data = process_data(new_data.reviews, new_data.ratings)
    sentiment_scores = perform_sentiment_analysis(processed_data[0])
    similarity_matrix = build_recommendation_engine(processed_data[0])
    return new_data, sentiment_scores, similarity_matrix


def visualize_sentiment_distribution(sentiment_scores):
    """
    Visualizes the sentiment distribution using a histogram
    """

    plt.hist(sentiment_scores, bins=10)
    plt.xlabel('Sentiment Score')
    plt.ylabel('Count')
    plt.title('Sentiment Distribution')
    plt.show()


def visualize_product_ratings(product_titles, ratings):
    """
    Visualizes the product ratings using a bar chart
    """

    fig = px.bar(x=product_titles, y=ratings, labels={'x': 'Products', 'y': 'Ratings'})
    fig.show()


def export_recommendations(recommendations):
    """
    Exports the list of recommended products to a text file
    """

    with open('recommended_products.txt', 'w') as file:
        file.write("Recommended Products:\n")
        for product in recommendations:
            file.write(f"- {product[0]} (Similarity Score: {product[1]})\n")


if __name__ == "__main__":
    url = input("Enter the URL of a product page: ")
    product_data = scrape_product_data(url)
    cleaned_data = process_data(product_data.reviews, product_data.ratings)
    sentiment_scores = perform_sentiment_analysis(cleaned_data[0])
    similarity_matrix = build_recommendation_engine(cleaned_data[0])
    product_titles = [product_data.title]

    recommendations = get_recommendations(product_data, similarity_matrix, product_titles)
    display_recommendations(recommendations)

    while True:
        choice = input("Do you want to update the data? (y/n): ")
        if choice.lower() == 'y':
            product_data, sentiment_scores, similarity_matrix = update_data(url, similarity_matrix, product_titles)
            cleaned_data = process_data(product_data.reviews, product_data.ratings)
            sentiment_scores = perform_sentiment_analysis(cleaned_data[0])
            similarity_matrix = build_recommendation_engine(cleaned_data[0])
            recommendations = get_recommendations(product_data, similarity_matrix, product_titles)
            display_recommendations(recommendations)
        else:
            break

    visualize_sentiment_distribution(sentiment_scores)
    visualize_product_ratings(product_titles, product_data.ratings)
    export_recommendations(recommendations)