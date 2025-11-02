import streamlit as st
from pipeline.pipeline import AnimeRecommendationPipeline
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Anime Recommender", page_icon=":tv:", layout="wide")
@st.cache_resource
def initialize_pipeline():
    return AnimeRecommendationPipeline(processed_csv="data/anime_updated.csv", persist_directory='chroma_db')

pipeline = initialize_pipeline()

st.title("Anime Recommender System :tv:")
user_query = st.text_input("Enter your anime preferences or description:")
if user_query:
    with st.spinner("Fetching recommendations..."):
        responses = pipeline.get_recommendations(user_query)
        st.markdown("### Recommended Anime:")
        st.write(responses)

        