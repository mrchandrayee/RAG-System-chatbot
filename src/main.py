import argparse
import sys
import os
from typing import Optional
from .ingest import DocumentIngester
from .query import QueryEngine

def setup_argparse() -> argparse.ArgumentParser:
    """
    Set up command line argument parsing.
    
    Returns:
        ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        description="Insurance Policy RAG System - Query your insurance documents"
    )
    parser.add_argument(
        "--ingest",
        action="store_true",
        help="Ingest documents from the data directory"
    )
    parser.add_argument(
        "--query",
        type=str,
        help="Query to ask about the insurance policies"
    )
    return parser

def ingest_documents() -> None:
    """
    Run the document ingestion process.
    """
    print("Starting document ingestion process...")
    try:
        ingester = DocumentIngester()
        ingester.ingest()
        print("Document ingestion complete!")
    except Exception as e:
        print(f"Error during ingestion: {str(e)}")
        sys.exit(1)

def query_documents(query: str) -> None:
    """
    Process a query and display the results.
    
    Args:
        query: The question to ask about the insurance policies
    """
    try:
        print(f"Processing query: {query}\n")
        engine = QueryEngine()
        result = engine.query(query)
        
        print("Answer:")
        print("-" * 80)
        print(result["answer"])
        print("-" * 80)
        
        print("\nSources:")
        print(engine.get_sources(result))
    except Exception as e:
        print(f"Error processing query: {str(e)}")
        sys.exit(1)

def interactive_mode() -> None:
    """
    Run the system in interactive mode.
    """
    try:
        engine = QueryEngine()
        
        print("\nInsurance Policy RAG System")
        print("Type 'exit' to quit the program")
        print("-" * 80)
        
        while True:
            try:
                query = input("\nWhat would you like to know about your insurance policies? ").strip()
                
                if query.lower() == "exit":
                    break
                    
                if not query:
                    continue
                    
                result = engine.query(query)
                
                print("\nAnswer:")
                print("-" * 80)
                print(result["answer"])
                print("-" * 80)
                
                print("\nWould you like to see the sources? (y/n)")
                show_sources = input().strip().lower()
                if show_sources == 'y':
                    print("\nSources:")
                    print(engine.get_sources(result))
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {str(e)}")
                continue
    except Exception as e:
        print(f"Error initializing query engine: {str(e)}")
        sys.exit(1)

def main() -> None:
    """
    Main entry point for the application.
    """
    parser = setup_argparse()
    args = parser.parse_args()
    
    if args.ingest:
        ingest_documents()
    elif args.query:
        query_documents(args.query)
    else:
        interactive_mode()

if __name__ == "__main__":
    main()