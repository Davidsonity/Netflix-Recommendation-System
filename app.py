import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import json

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

movies_df = pd.read_csv('movies_df.csv')
movies_sim = np.load('movies_sim.npz')
movies_sim = movies_sim['m']

tv_show = pd.read_csv('tv_show.csv')
tv_sim = np.load('tv_sim.npz')
tv_sim = tv_sim['t']

def recommend(title):
    if title in movies_df['title'].values:
        movies_index = movies_df[movies_df['title'] == title].index.item()
        scores = dict(enumerate(movies_sim[movies_index]))
        sorted_scores = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))

        selected_movies_index = [id for id, scores in sorted_scores.items()]
        selected_movies_score = [scores for id, scores in sorted_scores.items()]

        rec_movies = movies_df.iloc[selected_movies_index]
        rec_movies['similiarity'] = selected_movies_score

        movie_recommendation = rec_movies.reset_index(drop=True)
        return movie_recommendation[1:11]  # Skipping the first row

    elif title in tv_show['title'].values:
        tv_index = tv_show[tv_show['title'] == title].index.item()
        scores = dict(enumerate(tv_sim[tv_index]))
        sorted_scores = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))

        selected_tv_index = [id for id, scores in sorted_scores.items()]
        selected_tv_score = [scores for id, scores in sorted_scores.items()]

        rec_tv = tv_show.iloc[selected_tv_index]
        rec_tv['similiarity'] = selected_tv_score

        tv_recommendation = rec_tv.reset_index(drop=True)
        return tv_recommendation[1:11]  # Skipping the first row

def Table(df):
    fig = go.Figure(data=[go.Table(
        columnorder=[1, 2, 3, 4, 5],
        columnwidth=[20, 20, 20, 30, 50],
        header=dict(values=list(['Type', 'Title', 'Country', 'Genre(s)', 'Description']),
                    line_color='black', font=dict(color='black', family="Gravitas One", size=20), height=40,
                    fill_color='#FF6865',
                    align='center'),
        cells=dict(values=[df.type, df.title, df.country, df.genres, df.description],
                   font=dict(color='black', family="Lato", size=16),
                   fill_color='#FFB3B2',
                   align='left'))
    ])

    fig.update_layout(height=500,
                      width = 900
                      title={'text': "Top 10 Movie Recommendations", 'font': {'size': 22, 'family': 'Gravitas One'}},
                      title_x=0.5
                      )
    return st.plotly_chart(fig, use_container_width=True)


movie_list = sorted(movies_df['title'].tolist() + tv_show['title'].tolist())

####################################################################
#streamlit
##################################################################

st.header('Netflix Movie Recommendation System ')
lottie_coding = load_lottiefile("netflix-logo.json")
st_lottie(
    lottie_coding,
    speed=1,
    reverse=False,
    loop=True,
    quality="low",height=220
)
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names = recommend(selected_movie)
    Table(recommended_movie_names)
