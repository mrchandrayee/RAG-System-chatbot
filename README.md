# Insurance Policy RAG System

A Retrieval Augmented Generation (RAG) system for answering questions about insurance policies using LangChain.

## Problem Statement (10%)

Insurance policies are complex documents that can be difficult for users to navigate and understand. Traditional search methods often fail to capture the semantic meaning behind user queries and may miss relevant information spread across different sections of policy documents.

This RAG system addresses these challenges by:
- Providing natural language querying of insurance documents
- Using semantic search to find relevant policy sections
- Generating clear, contextual answers with source citations
- Maintaining accuracy through document-grounded responses

LangChain is the ideal framework for this system because it provides:
- Robust document loading and text splitting capabilities
- Vector store integration for semantic search
- LLM chain creation for intelligent response generation
- Built-in support for source attribution

## System Design (10%)

The system implements a three-layer architecture:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│ Document        │────>│ Vector          │────>│ Query           │
│ Ingestion       │     │ Store           │     │ Processing      │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

See [System Design Documentation](docs/system_design.md) for detailed architecture and workflow.

## Code Implementation (60%)

### Project Structure

```
.
├── data/               # Insurance policy documents
├── src/               # Source code
│   ├── ingest.py      # Document ingestion
│   ├── store.py       # Vector store management
│   ├── query.py       # Query processing
│   └── main.py        # Application entry point
├── tests/             # Test files
├── docs/              # Documentation
├── Dockerfile         # Container definition
├── docker-compose.yml # Container orchestration
└── requirements.txt   # Dependencies
```

### Setup Using Docker

1. Clone the repository:
```bash
git clone <repository-url>
cd rag-system
```

2. Create a `.env` file:
```bash
OPENAI_API_KEY=your_api_key_here
```

3. Build and run using Docker Compose:
```bash
# Start the system in interactive mode
docker-compose up

# Ingest documents
docker-compose run --rm rag-system python src/main.py --ingest

# Run a query
docker-compose run --rm rag-system python src/main.py --query "What is my deductible?"
```

### Local Setup (Alternative)

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with your OpenAI API key.

4. Run the application:
```bash
# Interactive mode
python src/main.py

# Ingest documents
python src/main.py --ingest

# Run a query
python src/main.py --query "What is my deductible?"
```

### Running Tests

```bash
# Using Docker
docker-compose run --rm rag-system python -m unittest discover tests

# Local
python -m unittest discover tests
```

## Documentation (20%)

### Key Features

1. Document Processing
   - PDF document support
   - Configurable text chunking
   - Semantic embeddings

2. Vector Storage
   - Persistent storage using Chroma
   - Efficient similarity search
   - Source tracking

3. Query Processing
   - Natural language understanding
   - Context-aware responses
   - Source citations

### Future Improvements

1. Technical Enhancements
   - Multi-document correlation
   - Response confidence scoring
   - Caching layer

2. User Interface
   - Web interface
   - REST API
   - Batch processing

3. Infrastructure
   - Scalable document processing
   - Enhanced error handling
   - Monitoring and logging

## Evaluation Metrics

1. Response Accuracy
   - Correctness of information
   - Relevance to query
   - Source attribution

2. Processing Efficiency
   - Document ingestion speed
   - Query response time
   - Resource utilization

3. System Robustness
   - Error handling
   - Edge case management
   - System stability

## License

[MIT License](LICENSE)

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request