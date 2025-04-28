from setuptools import setup, find_packages

setup(
    name="rag-system",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "langchain>=0.1.0",
        "langchain-community>=0.0.16",
        "langchain-openai>=0.0.5",
        "python-dotenv>=1.0.0",
        "openai>=1.3.0",
        "chromadb>=0.4.18",
        "pypdf>=3.17.1",
        "tiktoken>=0.5.1",
        "numpy>=1.24.3",
        "pandas>=2.0.3",
        "unstructured>=0.12.0",
    ],
    python_requires=">=3.9",
    description="A RAG system for querying insurance policy documents",
    author="RAG System Team",
    author_email="example@example.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.9",
    ],
)