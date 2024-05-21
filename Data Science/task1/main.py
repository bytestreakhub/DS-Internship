import pandas as pd
from surprise import Reader, Dataset, SVD
from surprise.model_selection import cross_validate

# Load the datasets
movies_df = pd.read_csv('movies.csv')
ratings_df = pd.read_csv('ratings.csv')

# Display the data
print(movies_df.head())
print(ratings_df.head())

# Prepare the data for the Surprise library
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(ratings_df[['userId', 'movieId', 'rating']], reader)

# Use the SVD algorithm
svd = SVD()

# Evaluate the algorithm using cross-validation
cross_validate(svd, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)

# Train the algorithm on the entire dataset
trainset = data.build_full_trainset()
svd.fit(trainset)

# Function to get movie recommendations
def get_recommendations(user_id, num_recommendations=5):
    # Get a list of all movie IDs
    all_movie_ids = movies_df['movieId'].tolist()
    
    # Get the list of movies the user has already rated
    rated_movie_ids = ratings_df[ratings_df['userId'] == user_id]['movieId'].tolist()
    
    # Predict ratings for all movies the user hasn't rated yet
    predictions = [svd.predict(user_id, movie_id) for movie_id in all_movie_ids if movie_id not in rated_movie_ids]
    
    # Sort the predictions by estimated rating
    predictions.sort(key=lambda x: x.est, reverse=True)
    
    # Get the top recommendations
    top_recommendations = predictions[:num_recommendations]
    
    # Get the movie titles for the top recommendations
    top_movie_ids = [pred.iid for pred in top_recommendations]
    recommended_movies = movies_df[movies_df['movieId'].isin(top_movie_ids)]
    
    return recommended_movies

# Example: Get recommendations for user with ID 1
recommended_movies = get_recommendations(1)
print("Recommended movies for user 1:")
print(recommended_movies)
