import streamlit as st
from movie_api.services import make_request_with_retry
import os

st.title("Détails des Films via TMDB")

movie_id = st.text_input("Entrez un ID de film", "550")

if st.button("Rechercher"):
    details = make_request_with_retry(
        f"https://api.themoviedb.org/3/movie/{movie_id}",   
        params={"api_key": os.getenv("TMDB_API_KEY")}
    )
st.write("Titre: " + details.get("title", "N/A"))
st.write("Date de sortie: " + details.get("release_date", "N/A"))
genres = details.get("genres", [])
if genres:
    st.write("Genres:")
    for genre in genres:
        st.write("- " + genre.get("name", "N/A"))
else:
    st.write("Genres: Non disponibles")
st.write("Popularité: " + str(details.get("popularity", "N/A")))
st.write("Note moyenne: " + str(details.get("vote_average", "N/A")))
with st.expander("Voir tous les détails"):
    st.json(details)