from typing import Dict, Optional
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from .store import VectorStore

class QueryEngine:
    def __init__(self, temperature: float = 0.0):
        """
        Initialize the query engine.
        
        Args:
            temperature: Temperature setting for the LLM
        """
        self.store = VectorStore()
        self.llm = ChatOpenAI(temperature=temperature)
        self.qa_chain = self._create_qa_chain()
        
    def _create_qa_chain(self) -> RetrievalQA:
        """
        Create the question-answering chain.
        
        Returns:
            RetrievalQA chain
        """
        prompt_template = """
        You are an insurance expert assistant. Use the following pieces of context to answer the question at the end.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        Always provide the source of your information from the context.
        
        Context: {context}
        
        Question: {question}
        
        Answer: Let me help you with that information from the insurance policy documents.
        """
        
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.store.vector_store.as_retriever(),
            chain_type_kwargs={
                "prompt": PROMPT
            },
            return_source_documents=True
        )
        
        return chain
    
    def query(self, question: str) -> Dict:
        """
        Process a question and generate a response.
        
        Args:
            question: The question to answer
            
        Returns:
            Dictionary containing the answer and source documents
        """
        response = self.qa_chain({"query": question})
        
        return {
            "answer": response["result"],
            "sources": [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata
                }
                for doc in response["source_documents"]
            ]
        }
    
    def get_sources(self, result: Dict) -> str:
        """
        Format source information from the query result.
        
        Args:
            result: Query result dictionary
            
        Returns:
            Formatted source information
        """
        sources = []
        for idx, source in enumerate(result["sources"], 1):
            source_text = f"""
            Source {idx}:
            Content: {source['content']}
            Metadata: {source['metadata']}
            """
            sources.append(source_text)
        
        return "\n".join(sources)

if __name__ == "__main__":
    # Example usage
    engine = QueryEngine()
    result = engine.query("What is the deductible for emergency room visits?")
    print(f"Answer: {result['answer']}\n")
    print("Sources:")
    print(engine.get_sources(result))