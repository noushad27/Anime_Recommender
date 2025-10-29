from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import CSVLoader
from langchain_huggingface import HuggingFaceHubEmbeddings

from dotenv import load_dotenv
load_dotenv()

class vectorstoreBuilder:
    def __init__(self, processed_csv:str, persist_directory:str='chroma_db'):
        self.csv_path = processed_csv
        self.persist_directory = persist_directory
        self.embedding = HuggingFaceHubEmbeddings(model_name="all-MiniLM-L6-v2")

    def build_and_save_vectorstore(self):
        loader = CSVLoader(file_path=self.csv_path, encoding='utf-8', metadata_columns=[])

        data = loader.load()

        splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        splitter.split_documents(data)

        db = Chroma.from_documents(CharacterTextSplitter, self.embedding, persist_directory=self.persist_directory)
        db.persist()
        return db
    
    def load_vectorstore(self):
        return Chroma(persist_directory=self.persist_directory, embedding_function=self.embedding)

