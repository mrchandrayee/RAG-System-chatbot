import unittest
from unittest.mock import Mock, patch
import os
import sys

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ingest import DocumentIngester
from src.store import VectorStore
from src.query import QueryEngine

class TestRAGSystem(unittest.TestCase):
    @patch('langchain.document_loaders.DirectoryLoader')
    def test_document_ingestion(self, mock_loader):
        # Mock document loading
        mock_loader.return_value.load.return_value = [
            Mock(page_content="Test insurance policy content")
        ]
        
        ingester = DocumentIngester()
        documents = ingester.load_documents()
        
        self.assertEqual(len(documents), 1)
        mock_loader.assert_called_once()
    
    @patch('langchain.vectorstores.Chroma')
    def test_vector_store_operations(self, mock_chroma):
        # Mock vector store operations
        mock_chroma.return_value.similarity_search.return_value = [
            Mock(page_content="Relevant test content")
        ]
        
        store = VectorStore()
        results = store.similarity_search("test query")
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].page_content, "Relevant test content")
    
    @patch('src.query.QueryEngine._create_qa_chain')
    def test_query_processing(self, mock_qa_chain):
        # Mock QA chain response
        mock_response = {
            "result": "Test answer",
            "source_documents": [
                Mock(
                    page_content="Source content",
                    metadata={"source": "test.pdf"}
                )
            ]
        }
        mock_qa_chain.return_value.return_value = mock_response
        
        engine = QueryEngine()
        result = engine.query("test question")
        
        self.assertEqual(result["answer"], "Test answer")
        self.assertEqual(len(result["sources"]), 1)
        self.assertEqual(result["sources"][0]["content"], "Source content")
    
    def test_invalid_query_handling(self):
        with patch('src.query.QueryEngine._create_qa_chain') as mock_qa_chain:
            # Mock QA chain to simulate error
            mock_qa_chain.side_effect = Exception("Test error")
            
            engine = QueryEngine()
            with self.assertRaises(Exception):
                engine.query("")

def main():
    unittest.main()

if __name__ == "__main__":
    main()