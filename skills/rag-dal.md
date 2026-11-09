---
name: rag-dal
description: "Designs a self-updating Dynamic Acquisition Layer (DAL) for RAG systems -- the autonomous watcher-to-index pipeline (watch, fetch, transform, chunk, embed, index) with per-source chunking strategies and incremental indexing, so the knowledge base stays current without full re-indexes. Use when building autonomous knowledge bases for Retrieval-Augmented Generation."
---

# RAG-DAL — Dynamic Acquisition Layer for RAG Systems

## Overview
RAG-DAL provides the architecture and implementation patterns for building self-updating knowledge bases that power Retrieval-Augmented Generation (RAG) systems. The Dynamic Acquisition Layer (DAL) continuously ingests, processes, and indexes new data sources so the RAG pipeline stays current without manual intervention.

## When to Use
- Designing a RAG system that needs to auto-ingest new content (docs, APIs, web pages).
- Building a knowledge base that evolves over time rather than being a static snapshot.
- Connecting multiple data sources into a unified retrieval pipeline.
- Implementing incremental indexing strategies to avoid full re-indexing.

## How It Works
The DAL sits between data sources and the retrieval engine, acting as an autonomous ingestion pipeline:

```
Data Sources → [DAL: Watch → Fetch → Transform → Chunk → Embed → Index] → Vector DB → Retriever → LLM
```

Core DAL components:
- **Watchers** — Monitor sources for changes (file system events, API polls, webhooks, RSS).
- **Fetchers** — Pull raw content from each source type.
- **Transformers** — Clean, normalize, and enrich content (metadata extraction, deduplication).
- **Chunkers** — Apply chunking strategies tuned to content type.
- **Embedders** — Generate vector embeddings and upsert into the vector database.

## Steps
1. **Map data sources.** Inventory every source that should feed the knowledge base (docs, APIs, databases, websites).
2. **Design watcher strategy.** Polling intervals for static sources, webhooks for real-time, incremental crawl for websites.
3. **Implement fetch + transform pipeline.** Handle auth, rate limits, format conversion, and deduplication.
4. **Configure chunking per source type.** 
   - Code repos: AST-aware splitting.
   - Documentation: heading-aware recursive chunking.
   - Chat/transcripts: turn-based segmentation.
5. **Set up embedding + indexing.** Choose embedding model (text-embedding-3, bge, etc.) and vector DB (Pinecone, Weaviate, Chroma, pgvector).
6. **Implement incremental updates.** Track source hashes/timestamps. Only re-index changed content.
7. **Add monitoring.** Track ingestion lag, chunk counts, embedding latency, and stale content alerts.

## Common Pitfalls
- **Full re-indexing instead of incremental.** Expensive and slow. Always design for delta updates from day one.
- **One-size-fits-all chunking.** Code, prose, and chat transcripts need different chunking strategies.
- **No deduplication.** Re-ingesting the same content creates duplicate embeddings, polluting retrieval quality.
- **Ignoring rate limits.** Aggressive polling can get you blocked. Respect source API limits.

## Inputs

- `sources` (list) -- inventory of every data source to ingest: docs, APIs, databases, websites
- `watcher_strategy` -- polling intervals for static sources, webhooks for real-time, incremental crawl for websites
- `chunking_strategy` per source type -- code repos: AST-aware splitting; docs: heading-aware recursive chunking; chat/transcripts: turn-based segmentation
- `embedding_model` (e.g. text-embedding-3, bge) and `vector_db` (Pinecone, Weaviate, Chroma, pgvector)

## Outputs

- A DAL implementation plan following the 7-step pipeline: map sources -> watcher strategy -> fetch/transform (auth, rate limits, dedupe) -> per-source chunking -> embedding/indexing -> incremental updates via source hashes/timestamps -> monitoring (ingestion lag, chunk counts, stale-content alerts)

## Example

Auto-ingest a product-docs site into the RAG knowledge base: watchers poll the docs site nightly; heading-aware recursive chunking; content hashes tracked per page; only changed pages are re-embedded and upserted into pgvector; an ingestion-lag dashboard alerts when content goes stale.

## Errors & edge cases

- **Full re-indexing instead of incremental** -- expensive and slow; always track source hashes/timestamps and update deltas only.
- **One-size-fits-all chunking** -- code, prose, and transcripts need different strategies or retrieval quality degrades.
- **No deduplication** -- re-ingesting the same content creates duplicate embeddings that pollute retrieval; dedupe on content hash at ingest.
- **Rate-limit violations** -- aggressive polling gets you blocked; respect each source's API limits.
