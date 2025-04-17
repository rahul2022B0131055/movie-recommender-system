import streamlit as st
import pickle
import pandas as pd
import requests

# Load data
movies_df = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))


def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=23b7d9ec01923ed0f8b8e12f0cd32c45"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
    except:
        return None


def recommend(movie):
    recommended_movies = []
    recommended_posters = []

    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    for i in movies_list:
        movie_id = movies_df.iloc[i[0]]['movie_id']
        recommended_movies.append(movies_df.iloc[i[0]]['title'])
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters  # Return both lists


# Streamlit UI
st.title('Flicksy')

selected_movie = st.selectbox(
    'Select a movie to get recommendations:',
    movies_df['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie)

    # Create 5 columns for display
    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.text(names[i])
            if posters[i]:  # Handle missing posters
                st.image(posters[i])
            else:
                st.text("Poster not available")
