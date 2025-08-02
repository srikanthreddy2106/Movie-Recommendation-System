import pandas as pd
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix

# Load data
movies = pd.read_csv("C:\movie_recommender.py/movies.csv")
ratings = pd.read_csv("ratings.csv")

# Streamlit App
st.set_page_config(page_title="🎬 Movie Recommender", layout="centered")
st.title("🎬 Movie Recommender System")

# Preprocess user-movie matrix
user_movie_matrix = ratings.pivot_table(index='userId', columns='movieId', values='rating').fillna(0)
movie_id_to_title = dict(zip(movies['movieId'], movies['title']))
title_to_movie_id = dict(zip(movies['title'], movies['movieId']))

# Build similarity matrix
movie_sparse_matrix = csr_matrix(user_movie_matrix.T.values)  # Transpose for movie similarity
similarity = cosine_similarity(movie_sparse_matrix)

# Index mapping
movie_ids = list(user_movie_matrix.columns)
id_to_index = {mid: idx for idx, mid in enumerate(movie_ids)}
index_to_id = {idx: mid for idx, mid in enumerate(movie_ids)}

# User input
selected_movie = st.selectbox("Select a movie you like:", sorted(movies['title'].unique()))

# Recommend function
def recommend_movies(selected_title, top_n=5):
    movie_id = title_to_movie_id.get(selected_title)
    if movie_id not in id_to_index:
        return []
    
    index = id_to_index[movie_id]
    similarity_scores = list(enumerate(similarity[index]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    top_movies = similarity_scores[1:top_n+1]  # skip the selected movie itself

    recommended = []
    for i, score in top_movies:
        mid = index_to_id[i]
        title = movie_id_to_title.get(mid, "Unknown")
        recommended.append((title, round(score, 2)))
    return recommended

# Show recommendations
if selected_movie:
    st.subheader("Top 5 Recommendations:")
    recommendations = recommend_movies(selected_movie)
    for title, score in recommendations:
        st.write(f"**{title}** (Similarity Score: {score})")
