from typing import List, Dict
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.schema import Document

class VectorStore:
    def __init__(self, persist_directory: str = "./chroma_db"):
        """
        Initialize the vector store manager.
        
        Args:
            persist_directory: Directory where the vector store is persisted
        """
        self.persist_directory = persist_directory
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = self._load_vector_store()
        
    def _load_vector_store(self) -> Chroma:
        """
        Load or create a new vector store.
        
        Returns:
            Chroma vector store instance
        """
        return Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )
    
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """
        Perform similarity search for a query.
        
        Args:
            query: Search query
            k: Number of documents to retrieve
            
        Returns:
            List of similar documents
        """
        return self.vector_store.similarity_search(query, k=k)
    
    def similarity_search_with_score(
        self, 
        query: str, 
        k: int = 4
    ) -> List[tuple[Document, float]]:
        """
        Perform similarity search with relevance scores.
        
        Args:
            query: Search query
            k: Number of documents to retrieve
            
        Returns:
            List of tuples containing documents and their similarity scores
        """
        return self.vector_store.similarity_search_with_score(query, k=k)
    
    def get_relevant_context(self, query: str, k: int = 4) -> str:
        """
        Get relevant context for a query.
        
        Args:
            query: Search query
            k: Number of documents to retrieve
            
        Returns:
            Concatenated context from relevant documents
        """
        documents = self.similarity_search(query, k=k)
        context = "\n\n".join(doc.page_content for doc in documents)
        return context
    
    def add_documents(self, documents: List[Document]) -> None:
        """
        Add new documents to the vector store.
        
        Args:
            documents: List of documents to add
        """
        self.vector_store.add_documents(documents)
        
    def persist(self) -> None:
        """
        Persist the vector store to disk.
        """
        self.vector_store.persist()
        
if __name__ == "__main__":
    # Example usage
    store = VectorStore()
    results = store.similarity_search("What are the coverage limits?")
    for doc in results:
        print(f"Content: {doc.page_content}\n")