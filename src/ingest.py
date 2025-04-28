from typing import List, Dict
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DocumentIngester:
    def __init__(self, data_dir: str = "./data", chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize the document ingester.
        
        Args:
            data_dir: Directory containing the documents to process
            chunk_size: Size of text chunks for processing
            chunk_overlap: Overlap between chunks for context preservation
        """
        self.data_dir = data_dir
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        self.embeddings = OpenAIEmbeddings()
        
    def load_documents(self) -> List[Dict]:
        """
        Load documents from the data directory.
        
        Returns:
            List of loaded documents
        """
        documents = []
        
        # Load PDF files
        pdf_loader = DirectoryLoader(
            self.data_dir,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader
        )
        documents.extend(pdf_loader.load())
        
        # Load text files
        text_loader = DirectoryLoader(
            self.data_dir,
            glob="**/*.txt",
            loader_cls=TextLoader
        )
        documents.extend(text_loader.load())
        
        return documents
    
    def process_documents(self, documents: List[Dict]) -> List[Dict]:
        """
        Process documents into chunks.
        
        Args:
            documents: List of documents to process
            
        Returns:
            List of processed document chunks
        """
        chunks = self.text_splitter.split_documents(documents)
        return chunks
    
    def create_vector_store(self, chunks: List[Dict]) -> Chroma:
        """
        Create a vector store from processed document chunks.
        
        Args:
            chunks: List of processed document chunks
            
        Returns:
            Chroma vector store instance
        """
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory="./chroma_db"
        )
        return vector_store
    
    def ingest(self) -> Chroma:
        """
        Run the full ingestion pipeline.
        
        Returns:
            Chroma vector store instance
        """
        print("Loading documents...")
        documents = self.load_documents()
        
        print(f"Processing {len(documents)} documents...")
        chunks = self.process_documents(documents)
        
        print("Creating vector store...")
        vector_store = self.create_vector_store(chunks)
        
        print("Ingestion complete!")
        return vector_store

if __name__ == "__main__":
    ingester = DocumentIngester()
    vector_store = ingester.ingest()