from src.vector_store import vectorstoreBuilder
from src.recommender import AnimeRecommender
from config.config import GROQ_API_KEY, GROQ_MODEL_NAME
from utils.logger import get_logger
from utils.custom_exception import CustomException


logger = get_logger(__name__)

class AnimeRecommendationPipeline:
    def __init__(self, processed_csv:str, persist_directory:str='chroma_db'):
        try:
            logger.info("Initializing Recommendation Pipeline...")

            vector_build = vectorstoreBuilder(csv_path=processed_csv , persist_dir=persist_directory)
             
            retriever = vector_build.load_vectorstore().as_retriever()

            self.recommender = AnimeRecommender(retriever=retriever, api_key=GROQ_API_KEY, model_name=GROQ_MODEL_NAME)
            logger.info("Pipeline initialized successfully.")

        except Exception as e:
            logger.error("Error initializing the pipeline.")
            raise CustomException(e)
        
    def get_recommendations(self, user_query:str):
        try:
            logger.info(f"Received user query: {user_query}")

            recommendations = self.recommender.get_recommendation(query=user_query)

            logger.info("Recommendations generated successfully.")
            return recommendations
        except Exception as e:
            logger.error("Failed to get recommendstion...")
            raise CustomException(e)
