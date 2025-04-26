# 🔍 Intent-Based E-Commerce Search API

## Project Overview
The Intent-Based E-Commerce Search API is a next-generation product search platform that goes beyond simple keyword matching to understand the true intent behind user queries, providing highly relevant product recommendations.

## 🌟 Key Features

### 1. Intelligent Search with NLP
- **Named Entity Recognition (NER)**: Automatically identifies product categories, brands, price ranges, and other attributes from natural language queries
- **Intent Classification**: Understands whether a user is searching, comparing, or seeking information
- **Semantic Search**: Uses transformer models to find products based on meaning, not just exact keyword matches

### 2. Hybrid Search Approach
- **Vector Embedding Search**: Finds semantically similar products using Pinecone vector database
- **Fuzzy Text Search**: Falls back to PostgreSQL text search when vector search yields no results
- **Multi-word Query Optimization**: Handles complex multi-word queries by breaking them down into meaningful components

### 3. API Design
- **Modern RESTful API**: Built with FastAPI for high performance and automatic documentation
- **Query Optimization**: GET endpoints for search with intelligent parameter handling
- **Flexible Response Format**: Structured JSON responses with relevant metadata

### 4. Advanced Monitoring
- **Prometheus Metrics**: Real-time performance monitoring
- **Loki for Log Aggregation**: Centralized logging with structured data
- **Grafana Dashboards**: Visualize API performance, search quality, and user behavior
- **OpenTelemetry Integration**: Distributed tracing for performance optimization

## 🏗️ Architecture

```
┌─────────────┐     ┌────────────────┐     ┌───────────────┐
│ User Query  │────▶│  NLP Pipeline  │────▶│ Search Engine │
└─────────────┘     └────────────────┘     └───────┬───────┘
                                                   │
                                                   ▼
┌─────────────┐     ┌────────────────┐     ┌───────────────┐
│   Client    │◀────│  FastAPI       │◀────│  Databases    │
└─────────────┘     └────────────────┘     └───────────────┘
```

## 💡 Technical Implementation

### NLP Pipeline
- Entity extraction with custom NER models
- Brand and category mapping through enhanced dictionaries
- Vector embeddings using SentenceTransformers

### Search Backend
- Primary: Pinecone vector database for semantic search
- Fallback: PostgreSQL with fuzzy search capabilities
- Filtering by extracted entities (brand, category, price)

### Database
- PostgreSQL with SQLModel ORM
- Well-structured product schema with detailed metadata

### Monitoring Stack
- Prometheus, Grafana, and Loki in Docker containers
- Custom metrics for search quality and performance
- Error tracking and visualization

## 🚀 Future Enhancements
1. Personalized search results based on user history
2. A/B testing framework for search algorithm improvements
3. Real-time inventory and price updates
4. Enhanced cross-selling recommendations

## 📊 Performance Metrics
- **Query Processing Time**: <100ms for most queries
- **Relevancy Score**: 85%+ precision on test dataset
- **Scalability**: Designed to handle 1000+ queries per second

## 📚 Technical Stack
- **Backend**: Python, FastAPI
- **NLP**: Transformers, SentenceTransformers
- **Databases**: PostgreSQL, Pinecone
- **Monitoring**: Prometheus, Grafana, Loki
- **Infrastructure**: Docker, Docker Compose

## 🧪 Demo Queries
Try these example queries to see the power of intent recognition:

- "Show me Apple laptops under $2000"
- "I need a gaming PC with good graphics"
- "What's the best phone for photography?"
- "Compare Dell and HP monitors"

---

*Developed for the Hackathon 2025*
